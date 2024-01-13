def get_next_question(questions, current_question):
    if current_question in questions:
        return current_question

    for question in questions:
        return question

    return None
