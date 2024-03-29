from osh.feedback.utility.handlers.question_logic import get_next_question
from osh.feedback.utility.questions_db import questions
import random
from flask import (
    Blueprint,
    render_template,
    request,
    session,
    redirect,
    url_for
)
from osh.feedback.utility.feedback_utility import (
    get_student_by_id,
    save_feedback_to_database,
    reset_feedback_utility,
    restart_utility
)

feedback_bp = Blueprint('feedback', __name__,
                        static_folder='static',
                        template_folder='templates'
                        )


@feedback_bp.route('/', methods=['GET', 'POST'])
def feedback():
    answers = session.get('answers', [])
    current_question = session.get('current_question', 'Имя ученика')
    student_name = session.get('student_name', '')
    parent_name = session.get('parent_name', '')

    if request.method == 'POST':
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
                    selected_answer = random.choice(selected_answers)
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

    session['current_question'] = current_question
    session['answers'] = answers

    return render_template('feedback.html',
                           current_question=current_question,
                           questions=questions,
                           answers=answers,
                           student_name=student_name,
                           parent_name=parent_name
                           )


@feedback_bp.route('/restart', methods=['POST'])
def restart():
    restart_utility()

    return redirect(url_for('feedback.feedback'))


@feedback_bp.route('/students/<int:student_id>/create_feedback', methods=['GET', 'POST'])
def create_feedback(student_id):
    student = get_student_by_id(student_id)
    answers = session.get('answers', [])

    first_question = 'Количество посещенных занятий'

    current_question = session.get('current_question', first_question)

    if 'current_student' in session and session['current_student'] != student_id:
        session.pop('current_question', None)
        session.pop('answers', None)
        current_question = first_question

    session['current_student'] = student_id

    if request.method == 'POST':
        selected_option = request.form.get(current_question)
        if current_question in questions:
            current_question_info = questions[current_question]

            selected_answers = current_question_info['answers'].get(selected_option, [])

            if selected_answers:
                selected_answer = random.choice(selected_answers)
                answers.append(selected_answer)

                follow_up_question = current_question_info.get(
                    'follow_up', {}).get(selected_option)
                if follow_up_question:
                    current_question = follow_up_question
                elif current_question_info.get('result', False):
                    feedback_data = ', '.join(answers)
                    save_feedback_to_database(student_id, feedback_data)

                    return render_template('student_result.html',
                                           result=answers,
                                           student_name=student['name'],
                                           student=student
                                           )
            else:
                current_question = get_next_question(questions, current_question)

    session['current_question'] = current_question
    session['answers'] = answers

    return render_template('student_feedback.html',
                           current_question=current_question,
                           questions=questions,
                           answers=answers,
                           student_name=student['name'],
                           student=student
                           )


@feedback_bp.route('/students/<int:student_id>/reset_feedback', methods=['POST'])
def reset_feedback(student_id):
    # Первый вопрос пишем тут
    first_question = 'Количество посещенных занятий'
    reset_feedback_utility(student_id, first_question)

    return redirect(url_for('feedback.create_feedback', student_id=student_id))
