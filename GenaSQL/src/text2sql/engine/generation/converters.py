def convert_messages_to_bedrock_format(model: str, messages: list[dict]) -> tuple[list[dict] | None, list[list[dict]]]:
    """convert 'standard' conversational prompt messages (openai, huggingface) to nested bedrock format"""
    assert messages[0]["role"] == "system"
    system_content: str = messages[0]["content"]
    system_message: list[dict] = [{"text": system_content}]
    messages = messages[1:]
    # mistral, titan models do not use system prompt
    if model.startswith("mistral") or model.startswith("amazon"):
        messages[0]["content"] = system_content + messages[0]["content"]
        system_message = None
    # convert into bedrock format with content value as dict with key text
    bedrock_messages = []
    for msg in messages:
        bedrock_messages.append({"role": msg["role"], "content": [{"text": msg["content"]}]})

    return system_message, bedrock_messages