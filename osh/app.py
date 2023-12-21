from dotenv import load_dotenv
from osh.groups import groups_bp
from osh.students import students_bp
from osh.feedback import feedback_bp
from osh.messenger import link_bp
from flask import Flask, render_template
import os

load_dotenv()

secret_key = os.getenv('SECRET_KEY')

app = Flask(__name__)
app.secret_key = secret_key

app.register_blueprint(groups_bp, url_prefix='/groups')
app.register_blueprint(students_bp, url_prefix='/students')
app.register_blueprint(feedback_bp, url_prefix='/feedback')
app.register_blueprint(link_bp, url_prefix='/link')


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run()
