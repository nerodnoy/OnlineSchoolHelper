from flask import Flask, render_template, request
from dotenv import load_dotenv
import os

load_dotenv()

secret_key = os.getenv('SECRET_KEY')
app = Flask(__name__)


def generate_telegram_link(phone_number):
    cleaned_phone_number = ''.join(
        char for char in phone_number if char.isnumeric() or char == '+'
    )

    if not cleaned_phone_number.startswith('+'):
        cleaned_phone_number = '+' + cleaned_phone_number

    telegram_link = f"t.me/{cleaned_phone_number}"
    return telegram_link


@app.route('/', methods=['GET', 'POST'])
def index():
    telegram_link = None
    if request.method == 'POST':
        phone_number = request.form['phone_number']
        telegram_link = generate_telegram_link(phone_number)
    return render_template('index.html', telegram_link=telegram_link)


if __name__ == '__main__':
    app.run(debug=True)
