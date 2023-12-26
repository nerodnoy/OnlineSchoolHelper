from datetime import datetime
from bs4 import BeautifulSoup
from osh.database.database import add_student


def parse_and_add_students(group_id, html_content):
    soup = BeautifulSoup(html_content, 'html.parser')

    student_names = [h3.text.strip() for h3 in soup.find_all('h3')]

    for name in student_names:
        add_student(name, group_id=group_id)


def calculate_week_in_month(start_date):
    start_date_obj = datetime.strptime(start_date, '%Y-%m-%d')
    week_number = (start_date_obj.day - 1) // 7 + 1

    return week_number


def generate_telegram_link(phone_number):
    cleaned_phone_number = ''.join(
        char for char in phone_number if char.isnumeric() or char == '+'
    )

    if not cleaned_phone_number.startswith('+'):
        cleaned_phone_number = '+' + cleaned_phone_number

    telegram_link = f"t.me/{cleaned_phone_number}"
    return telegram_link


def generate_whatsapp_link(phone_number):
    cleaned_phone_number = ''.join(
        char for char in phone_number if char.isnumeric() or char == '+'
    )

    if not cleaned_phone_number.startswith('+'):
        cleaned_phone_number = '+' + cleaned_phone_number

    whatsapp_link = f"wa.me/{cleaned_phone_number}"
    return whatsapp_link


def get_next_question(questions, current_question):
    if current_question in questions:
        return current_question

    for question in questions:
        return question

    return None
