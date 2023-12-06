from flask import Flask, render_template, request, session, redirect, url_for
from converter.utils import generate_telegram_link
from converter.questions import questions
from converter.question_logic import get_next_question
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
    answers = session.get('answers', [])
    current_question = session.get('current_question', 'Количество посещенных занятий')

    if request.method == 'POST':
        selected_option = request.form.get(current_question)
        if current_question in questions:
            current_question_info = questions[current_question]
            answers.append((current_question, current_question_info['answers'].get(selected_option, '')))

            # Определение следующего вопроса
            follow_up_question = current_question_info.get('follow_up', {}).get(selected_option)
            if follow_up_question:
                current_question = follow_up_question
            else:
                current_question = get_next_question(questions, current_question)

        session['current_question'] = current_question

    session['answers'] = answers

    return render_template('feedback.html', current_question=current_question, questions=questions,
                           answers=answers)


@app.route('/restart', methods=['POST'])
def restart():
    session.pop('answers', None)
    session.pop('current_question', None)

    # Не забыть установить начальный вопрос здесь
    session['current_question'] = 'Количество посещенных занятий'

    return redirect(url_for('feedback'))


if __name__ == '__main__':
    app.run(debug=True)
