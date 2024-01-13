from flask import request
from osh.numbers.utility.handlers.generators import (
    generate_telegram_link,
    generate_whatsapp_link
)


def generate_number_links():
    telegram_link = None
    whatsapp_link = None
    if request.method == 'POST':
        phone_number = request.form['phone_number']
        telegram_link = generate_telegram_link(phone_number)
        whatsapp_link = generate_whatsapp_link(phone_number)
    return {'telegram_link': telegram_link, 'whatsapp_link': whatsapp_link}


