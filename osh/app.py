from osh.database.database import create_tables
from osh.groups.utility.groups_utility import inject_groups_utility
from osh.groups.groups import groups_bp
from osh.students.students import students_bp
from osh.feedback.feedback import feedback_bp
from osh.statistics.stats import stats_bp
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
app.register_blueprint(stats_bp, url_prefix='/stats')

create_tables()


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@app.context_processor
def inject_groups():
    return inject_groups_utility()


@app.errorhandler(404)
def not_found_error(error):
    return render_template('error.html',
                           error_code=404,
                           error_message="Страница не найдена"
                           ), 404


if __name__ == '__main__':
    app.run()
