import concurrent.futures
from typing import Dict, List, Optional, Tuple

from text2sql.data.query_parser import get_table_mapping
from text2sql.data.schema_filtering import parse_m_schema
from text2sql.data.schema_manager import SchemaManager
from text2sql.engine.generation.generators import BaseGenerator, GenerationResult
from text2sql.evaluation.metrics import execution_match

# System and user prompts for query comparison
SYSTEM_PROMPT = """You are an expert in SQLite query analysis.

You will be given a database schema, a question, and two SQL query candidates (A and B) along with their execution results (first 10 rows).
Your task is to compare these candidates and determine which one produces the most correct and reasonable result based on the given schema, question, and hint.

Return only one letter either `"A"` or `"B"`."""

USER_PROMPT_TEMPLATE = """### Database Schema
{schema_description}

### Question
{user_question}

### Hint
{evidence}

### Candidate A
#### SQL:
{candidate_a}
#### Execution Result:
{candidate_a_result}

### Candidate B
#### SQL:
{candidate_b}
#### Execution Result:
{candidate_b_result}

**Which candidate produces the most correct and reasonable result, A or B?**"""

# Constants
MAX_RESULT_LENGTH = 5000
MAX_WORKERS = 4


def merge_table_mapping(correct_table_mapping: Dict, wrong_table_mapping: Dict) -> Dict:
    """
    Merge two table mappings, combining their values.

    Args:
        correct_table_mapping: The first table mapping
        wrong_table_mapping: The second table mapping

    Returns:
        A merged table mapping
    """
    for table in correct_table_mapping:
        if table not in wrong_table_mapping:
            wrong_table_mapping[table] = correct_table_mapping[table]
        else:
            wrong_table_mapping[table] = list(set(wrong_table_mapping[table]) | set(correct_table_mapping[table]))
    return wrong_table_mapping


def get_votes(predictions: List[Dict]) -> Dict:
    """
    Count votes for each unique prediction based on execution results.

    Args:
        predictions: List of prediction dictionaries with 'sql' and 'results' keys

    Returns:
        Dictionary mapping SQL queries to their vote counts and other values
    """
    prediction_votes = {}
    for values in predictions:
        prediction = values["sql"]
        found_match = False
        for compared_prediction, compared_values in prediction_votes.items():
            if execution_match(compared_values["results"], values["results"]):
                found_match = True
                prediction_votes[compared_prediction]["vote_count"] += 1
                break
        if not found_match:
            prediction_votes[prediction] = {"vote_count": 1, **values}
    return prediction_votes


def truncate_results(results: str, max_length: int = MAX_RESULT_LENGTH) -> str:
    """
    Truncate results if they exceed the maximum length.

    Args:
        results: The results string to truncate
        max_length: Maximum length before truncation

    Returns:
        Truncated results string
    """
    if len(results) > max_length:
        print("Truncating output")
        return f"{results[:max_length]}... OUTPUT TRUNCATED BECAUSE OF LENGTH"
    return results


def get_comparison_messages(pred_a: Dict, pred_b: Dict, row: Dict) -> List[Dict]:
    """
    Generate messages for comparing two SQL query candidates.

    Args:
        pred_a: First prediction dictionary
        pred_b: Second prediction dictionary
        row: Data row containing schema and query information

    Returns:
        List of message dictionaries for the GCPGenerator
    """
    cand_a_results = truncate_results(str(pred_a["results"][:10]))
    cand_b_results = truncate_results(str(pred_b["results"][:10]))

    query_message = USER_PROMPT_TEMPLATE.format(
        schema_description=row["min_m_schema"],
        user_question=row["nl_en_query"],
        evidence=row["evidence"],
        candidate_a=pred_a["sql"],
        candidate_a_result=cand_a_results,
        candidate_b=pred_b["sql"],
        candidate_b_result=cand_b_results,
    )

    return [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": query_message},
    ]


def process_prediction_pair(
    pair: Tuple[int, int],
    predictions: List[Dict],
    schema_manager: SchemaManager,
    db_id: str,
    nl_en_query: str,
    evidence: str,
    generator: BaseGenerator,
) -> Optional[Tuple[int, int, GenerationResult | None]]:
    """
    Process a pair of predictions to determine which one to vote for.

    Args:
        pair: Tuple of prediction indices to compare
        predictions: List of prediction dictionaries
        schema_manager: Schema manager instance
        db_id: Database ID
        nl_en_query: Natural language query
        evidence: Evidence for the query
        generator: GCP Generator instance for query comparison

    Returns:
        Tuple of (prediction_index, vote_count) or None if no vote
    """
    idx, inner_idx = pair
    if idx == inner_idx:
        return None

    if execution_match(predictions[idx]["results"], predictions[inner_idx]["results"]):
        return (idx, 1, None)

    # Get table mappings for both predictions
    try:
        outer_table_mapping = get_table_mapping(schema_manager.get_schema_mapping(db_id), predictions[idx]["sql"])[
            "table_map"
        ]
        inner_table_mapping = get_table_mapping(
            schema_manager.get_schema_mapping(db_id), predictions[inner_idx]["sql"]
        )["table_map"]
    except Exception:
        # case where parsing fails e.g. LLM output not SQL
        return None

    # Merge table mappings and parse schema
    table_mapping = merge_table_mapping(outer_table_mapping, inner_table_mapping)
    min_m_schema = parse_m_schema(
        schema_manager.get_full_schema(db_id, "m_schema"),
        table_mapping,
        force_keep_all=True,
    )

    # Generate comparison messages
    messages = get_comparison_messages(
        predictions[idx],
        predictions[inner_idx],
        {
            "min_m_schema": min_m_schema,
            "nl_en_query": nl_en_query,
            "evidence": evidence,
        },
    )
    # Add the instruction to return only A or B
    messages[-1]["content"] += "\nReturn only the letter A or B, do not output any other text"

    # Use GCPGenerator to get the vote
    result_object: GenerationResult = generator.generate(messages, temperature=0)
    vote = result_object.text.strip()

    if vote.lower() == "a":
        return (idx, 1, result_object)
    if vote.lower() == "b":
        return (inner_idx, 1, result_object)
    print("Invalid vote:", vote)
    return None


def chase_voting(
    predictions: List[Dict],
    schema_manager: SchemaManager,
    db_id: str,
    question: str,
    evidence: str,
    generator: BaseGenerator,
) -> Tuple[Dict[int, int], list[GenerationResult]]:
    """
    Perform chase voting on predictions using parallel processing.

    Args:
        predictions: List of prediction dictionaries
        schema_manager: Schema manager instance
        db_id: Database ID
        question: Natural language query
        evidence: Evidence for the query
        generator: GCP Generator instance for query comparison

    Returns:
        Dictionary mapping prediction indices to vote counts
    """
    prediction_votes = {}

    # Create all pairs of prediction indices
    pairs = [(i, j) for i in range(len(predictions)) for j in range(len(predictions))]

    # Process pairs in parallel
    with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        results = executor.map(
            lambda pair: process_prediction_pair(
                pair,
                predictions,
                schema_manager,
                db_id,
                question,
                evidence,
                generator,
            ),
            pairs,
        )

    # Aggregate votes
    generation_results: list[GenerationResult] = []
    for result in results:
        if result is not None:
            pred_idx, vote, gen_result = result
            prediction_votes[pred_idx] = prediction_votes.get(pred_idx, 0) + vote
            if gen_result is not None:
                generation_results.append(gen_result)

    return prediction_votes, generation_results


def select_best_candidate(
    predictions: List[Dict],
    chase: bool = False,
    schema_manager: SchemaManager | None = None,
    db_id: str | None = None,
    question: str | None = None,
    evidence: str | None = None,
    generator: BaseGenerator | None = None,
) -> Tuple[str, list[GenerationResult]]:
    """
    Select the best prediction based on voting.

    Args:
        predictions: List of prediction dictionaries
        chase: Whether to perform chase voting
        schema_manager: Schema manager instance
        db_id: Database ID
        question: Natural language query
        evidence: Evidence for the query
        generator: GCP Generator instance for query comparison

    Returns:
        The best SQL query as a string
    """

    """
    SAMPLE PREDICTION:
    {
        "sql": "SELECT * FROM schools",
        "valid": true,
        "repaired": false,
        "rewritten": false,
        "inference_time_secs": 1.7527539730072021,
        "results": [
          {
            "MailStreet": "14429 South Downey Avenue"
          }
        ]
    }
    """

    if chase and schema_manager is None:
        raise ValueError("schema_manager is required for chase voting")
    if chase and (db_id is None or question is None or evidence is None):
        raise ValueError("db_id, nl_en_query, and evidence are required for chase voting")
    if chase and generator is None:
        raise ValueError("generator is required for chase voting")

    predicted_valids = [item for item in predictions if item["valid"]]

    if not predicted_valids:
        if len(predictions) > 0:
            return predictions[0]["sql"], []
        else:
            return "SELECT 1", []

    prediction_votes = get_votes(predicted_valids)
    max_vote_sql, values = max(prediction_votes.items(), key=lambda x: x[1]["vote_count"])

    if not chase:
        return max_vote_sql, []

    max_vote = values["vote_count"]

    # Determine if chase voting is needed
    should_chase = (
        max_vote == 1
        or (max_vote == 2 and sum([True for val in prediction_votes.values() if val["vote_count"] == 2]) > 1)
        or (max_vote == 3 and sum([True for val in prediction_votes.values() if val["vote_count"] == 2]) >= 1)
    )

    if should_chase:
        chase_votes, chase_generations = chase_voting(
            predicted_valids,
            schema_manager,
            db_id,
            question,
            evidence,
            generator,
        )

        # Handle empty chase_votes
        if not chase_votes:
            return max_vote_sql, chase_generations

        chase_idx, _chase_max_vote = max(chase_votes.items(), key=lambda x: x[1])
        chase_sql = predicted_valids[chase_idx]["sql"]

        return chase_sql, chase_generations
    else:
        return max_vote_sql, []
