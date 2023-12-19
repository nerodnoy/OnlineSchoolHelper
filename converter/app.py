from flask import Flask, render_template, request, session, redirect, url_for, abort, jsonify
from converter.utils import generate_telegram_link, generate_whatsapp_link
from converter.database import create_table, add_group, get_all_groups, delete_group, get_group_by_name, clear_database, \
    get_students_for_group, delete_student, update_student_notes1, update_student_notes2, \
    get_absent_students, mark_student_absent
from converter.students import parse_and_add_students
from converter.questions import questions
from converter.question_logic import get_next_question
from dotenv import load_dotenv
import random
import os

load_dotenv()

secret_key = os.getenv('SECRET_KEY')
app = Flask(__name__)
app.secret_key = secret_key

create_table()


@app.route('/', methods=['GET', 'POST'])
def index():
    telegram_link = None
    whatsapp_link = None
    if request.method == 'POST':
        phone_number = request.form['phone_number']
        telegram_link = generate_telegram_link(phone_number)
        whatsapp_link = generate_whatsapp_link(phone_number)
    return render_template('index.html',
                           telegram_link=telegram_link,
                           whatsapp_link=whatsapp_link
                           )


@app.route('/feedback', methods=['GET', 'POST'])
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

                # Проверяем, что список ответов не пуст
                selected_answers = current_question_info['answers'].get(
                    selected_option, [])
                if selected_answers:

                    # Выбираем случайный вариант ответа
                    selected_answer = random.choice(selected_answers)
                    answers.append(selected_answer)

                    # Определение следующего вопроса
                    follow_up_question = current_question_info.get(
                        'follow_up', {}).get(selected_option)
                    if follow_up_question:
                        current_question = follow_up_question
                    elif current_question_info.get('result', False):

                        # Если это конечный результат, завершаем опрос
                        return render_template('result.html',
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


@app.route('/restart', methods=['POST'])
def restart():
    session.pop('answers', None)
    session.pop('current_question', None)
    session.pop('result', None)

    # Не забыть установить начальный вопрос здесь
    session['current_question'] = 'Имя ученика'

    return redirect(url_for('feedback'))


# @app.errorhandler(Exception)
# def handle_error(e):
#     return render_template('error.html', error=str(e))


@app.route('/groups/create', methods=['GET', 'POST'])
def create_group():
    if request.method == 'POST':
        skill = request.form.get('skill')
        time = request.form.get('time')
        day = request.form.get('day')
        link = request.form.get('link')

        group_name = f"{skill} {time} {day}"
        add_group(group_name, link)
        return redirect(url_for('list_groups'))

    return render_template('create_group.html')


@app.route('/groups/', methods=['GET'])
def list_groups():
    groups = get_all_groups()
    return render_template('list_groups.html', groups=groups)


@app.route('/groups/<group_name>/', methods=['GET'])
def view_group(group_name):
    group = get_group_by_name(group_name)
    if group:
        group_id = group['id']  # Получаем ID группы
        students = get_students_for_group(group_id)
        return render_template('view_group.html', group=group, students=students)
    else:
        abort(404)


@app.route('/groups/<group_name>/delete', methods=['POST'])
def delete_group_route(group_name):
    delete_group(group_name)
    return redirect(url_for('list_groups'))


@app.route('/clear_database', methods=['POST'])
def clear_all_data():
    clear_database()
    return redirect(url_for('list_groups'))


@app.route('/groups/<group_name>/add_students', methods=['POST'])
def add_students(group_name):
    students_html = request.form.get('studentsHtml')
    parse_and_add_students(group_name, students_html)
    return redirect(url_for('view_group', group_name=group_name))


@app.route('/groups/<group_name>/delete_student/<int:student_id>', methods=['POST'])
def delete_student_route(group_name, student_id):
    delete_student(student_id)
    return redirect(url_for('view_group', group_name=group_name))


@app.route('/groups/<group_name>/students/<int:student_id>/update_notes_lesson1', methods=['POST'])
def update_notes1(group_name, student_id):
    notes_lesson1 = request.form.get('notes_lesson1')
    update_student_notes1(student_id, notes_lesson1=notes_lesson1)
    return redirect(url_for('view_group', group_name=group_name))


@app.route('/groups/<group_name>/students/<int:student_id>/update_notes_lesson2', methods=['POST'])
def update_notes2(group_name, student_id):
    notes_lesson2 = request.form.get('notes_lesson2')
    update_student_notes2(student_id, notes_lesson2=notes_lesson2)
    return redirect(url_for('view_group', group_name=group_name))


@app.route('/mark_absent/<group_name>/<student_id>', methods=['POST'])
def mark_absent(group_name, student_id):
    mark_student_absent(student_id)
    return redirect(url_for('view_group', group_name=group_name))


@app.route('/prepare_absent_list/<group_name>', methods=['POST'])
def prepare_absent_list(group_name):
    group = get_group_by_name(group_name)
    if group:
        group_id = group['id']
        absent_students = get_absent_students(group_id)
        return render_template('absent_list.html', absent_students=absent_students, group_name=group_name, group=group)
    else:
        # Обработка случая, если группа не найдена
        return render_template('error.html', message='Group not found')


if __name__ == '__main__':
    app.run()
