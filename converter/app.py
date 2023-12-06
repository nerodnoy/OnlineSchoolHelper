from flask import Flask, render_template, request, session, redirect, url_for
from converter.utils import generate_telegram_link
from converter.questions import questions
from dotenv import load_dotenv
import os

load_dotenv()

secret_key = os.getenv('SECRET_KEY')
app = Flask(__name__)
app.secret_key = secret_key


@app.route('/', methods=['GET', 'POST'])
def index():
    telegram_link = None
    if request.method == 'POST':
        phone_number = request.form['phone_number']
        telegram_link = generate_telegram_link(phone_number)
    return render_template('index.html', telegram_link=telegram_link)


@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
    answers = session.get('answers', {})
    current_question_index = session.get('current_question_index', 0)

    if request.method == 'POST':
        if current_question_index < len(questions):
            current_question = questions[current_question_index]
            selected_option = request.form.get(current_question['question'])
            if 'answers' in current_question:
                answers[current_question['question']] = current_question['answers'].get(selected_option, '')

            # Обновляем текущий вопрос
            current_question_index += 1
            session['current_question_index'] = current_question_index

    session['answers'] = answers

    return render_template('feedback.html', questions=questions, answers=answers,
                           current_question_index=current_question_index)


@app.route('/restart', methods=['POST'])
def restart():
    session.pop('answers', None)
    session.pop('current_question_index', None)

    # Установка начального индекса вопроса
    session['current_question_index'] = 0

    return redirect(url_for('feedback'))


if __name__ == '__main__':
    app.run(debug=True)
