def validate_question(question):
    """
    Validate the user's question before sending it to the RAG pipeline.
    Returns:
        (cleaned_question, None) if valid
        (None, error_message) if invalid
    """

    if question is None:
        return None, "Question is required."

    if not isinstance(question, str):
        return None, "Question must be a string."

    question = question.strip()

    if question == "":
        return None, "Question cannot be empty."

    if len(question) < 3:
        return None, "Question must be at least 3 characters long."

    return question, None