from flask import Blueprint, render_template, request
from osh.utility import generate_telegram_link, generate_whatsapp_link

num_bp = Blueprint('numbers', __name__,
                   static_folder='static',
                   template_folder='templates'
                   )


@num_bp.route('/', methods=['GET', 'POST'])
def generate_number():
    telegram_link = None
    whatsapp_link = None
    if request.method == 'POST':
        phone_number = request.form['phone_number']
        telegram_link = generate_telegram_link(phone_number)
        whatsapp_link = generate_whatsapp_link(phone_number)
    return render_template('numbers.html',
                           telegram_link=telegram_link,
                           whatsapp_link=whatsapp_link
                           )
