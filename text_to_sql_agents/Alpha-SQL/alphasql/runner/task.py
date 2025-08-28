from pydantic import BaseModel
from typing import Optional, Dict, Any

class Task(BaseModel):
    """
    A NL2SQL task.

    Attributes:
        question_id: The id of the question.
        db_id: The id of the database.
        question: The question to answer.
        evidence: The evidence to answer the question.
        sql: The SQL query to answer the question, if it is known or completed.
        difficulty: The difficulty of the question, if it is known.
        schema_context: The schema context for the question.
    """
    question_id: int
    db_id: str
    question: str
    evidence: str
    sql: Optional[str] = None
    difficulty: Optional[str] = None
    schema_context: Optional[str] = None
    table_schema_dict: Optional[Dict[str, Any]] = None