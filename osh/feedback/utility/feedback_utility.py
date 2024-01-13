from random import choice
from flask import render_template, request, session
from osh.feedback.utility.questions_db import questions
from osh.feedback.utility.handlers.question_logic import get_next_question


def feedback_for_anyone(current_question, student_name, parent_name, answers):
    if current_question == 'Имя ученика':
        student_name = request.form.get('student_name', '')
        session['student_name'] = student_name
        current_question = 'Имя родителя'
    elif current_question == 'Имя родителя':
        parent_name = request.form.get('parent_name', '')
        session['parent_name'] = parent_name
        current_question = 'Количество посещенных занятий'
    else:
        selected_option = request.form.get(current_question)

        if current_question in questions:
            current_question_info = questions[current_question]

            selected_answers = current_question_info['answers'].get(
                selected_option, [])

            if selected_answers:
                selected_answer = choice(selected_answers)
                answers.append(selected_answer)

                follow_up_question = current_question_info.get(
                    'follow_up', {}).get(selected_option)
                if follow_up_question:
                    current_question = follow_up_question
                elif current_question_info.get('result', False):
                    return render_template('feedback_result.html',
                                           result=answers,
                                           student_name=student_name,
                                           parent_name=parent_name
                                           )
            else:
                current_question = get_next_question(questions, current_question)

    return current_question, student_name, parent_name, answers
