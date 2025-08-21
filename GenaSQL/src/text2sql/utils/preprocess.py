import spacy


def extract_named_entities(text: str) -> dict:
    """
    Extract named entities from text using spaCy
    """
    # Load spaCy model - you can choose different models based on your needs
    # en_core_web_sm is smaller/faster, en_core_web_lg is more accurate but larger
    nlp = spacy.load("en_core_web_sm")

    # Process the text
    doc = nlp(text)

    # Extract named entities
    named_entities = {}
    for entity in doc.ents:
        entity_type = entity.label_
        entity_text = entity.text

        # Initialize the list for this entity type if it doesn't exist
        if entity_type not in named_entities:
            named_entities[entity_type] = []

        # Add this entity to the list
        named_entities[entity_type].append(entity_text)

    return named_entities


def replace_entities_with_tokens(question: str) -> str:
    """
    Replace named entities with special tokens based on their type
    If entity is not a named entity but matches enumeration values, replace with column name
    """
    skeleton_question = question
    named_entities = extract_named_entities(question)
    # Replace named entities with special tokens
    for entity_type, entities in named_entities.items():
        for entity in entities:
            # Use <TYPE> format for entity replacement
            skeleton_question = skeleton_question.replace(entity, f"<{entity_type.lower()}>")

    return skeleton_question
