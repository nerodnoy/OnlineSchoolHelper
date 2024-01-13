from flask import Blueprint, render_template
from osh.numbers.utility.numbers_utility import generate_number_links

num_bp = Blueprint('numbers', __name__,
                   static_folder='static',
                   template_folder='templates'
                   )


@num_bp.route('/', methods=['GET', 'POST'])
def generate_number():
    number_links = generate_number_links()
    return render_template('numbers.html', **number_links)
