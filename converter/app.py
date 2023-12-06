from flask import Flask, render_template, request
from converter.utils import generate_telegram_link
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


if __name__ == '__main__':
    app.run(debug=True)
