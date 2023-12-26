from osh.groups.groups_utility import get_current_month, get_current_week, filter_groups
from osh.database.database import get_all_groups
from osh.groups.groups import groups_bp
from osh.students.students import students_bp
from osh.feedback.feedback import feedback_bp
from osh.numbers.numbers import num_bp
from flask import Flask, render_template
from dotenv import load_dotenv
import os


load_dotenv()

secret_key = os.getenv('SECRET_KEY')

app = Flask(__name__, static_folder='static', template_folder='templates')
app.secret_key = secret_key

app.register_blueprint(groups_bp, url_prefix='/groups')
app.register_blueprint(students_bp, url_prefix='/students')
app.register_blueprint(feedback_bp, url_prefix='/feedback')
app.register_blueprint(num_bp, url_prefix='/numbers')


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@app.context_processor
def inject_groups():
    groups = get_all_groups()
    current_month = get_current_month()
    current_week = get_current_week()
    current_week_groups = filter_groups(groups, current_week, current_month)

    return dict(groups=groups, current_week_groups=current_week_groups)


@app.errorhandler(404)
def not_found_error(error):
    return render_template('error.html',
                           error_code=404,
                           error_message="Страница не найдена"
                           ), 404


if __name__ == '__main__':
    app.run()
