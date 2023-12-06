from flask import Flask, render_template, request, session
from converter.utils import generate_telegram_link
from converter.questions import questions
from dotenv import load_dotenv
import os

load_dotenv()

secret_key = os.getenv('SECRET_KEY')
app = Flask(__name__)
app.secret_key = secret_key  # Установка секретного ключа Flask


@app.route('/', methods=['GET', 'POST'])
def index():
    telegram_link = None
    if request.method == 'POST':
        phone_number = request.form['phone_number']
        telegram_link = generate_telegram_link(phone_number)
    return render_template('index.html', telegram_link=telegram_link)


@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
    if request.method == 'POST':
        answers = {}
        for question in questions:
            selected_option = request.form.get(question['question'])
            answers[question['question']] = question['answers'].get(selected_option, '')

        # Сохраняем ответы в сессии
        session['answers'] = answers

    # Передаем ответы в feedback.html для отображения
    return render_template('feedback.html', questions=questions, answers=session.get('answers', {}))


if __name__ == '__main__':
    app.run(debug=True)
