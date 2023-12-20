def get_next_question(questions, current_question):
    if current_question in questions:
        return current_question

    # Если текущий вопрос не найден, ищем первый вопрос в словаре
    for question in questions:
        return question

    return None