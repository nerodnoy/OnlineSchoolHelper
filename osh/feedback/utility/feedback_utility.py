from flask import session

from osh.database.database import (
    db_get_student_by_id,
    db_save_feedback_to_database,
    db_update_student_info
)


def get_student_by_id(student_id):
    student = db_get_student_by_id(student_id)

    return student


def save_feedback_to_database(student_id, feedback_data):
    db_save_feedback_to_database(student_id, feedback_data)


def restart_utility():
    session.pop('answers', None)
    session.pop('current_question', None)
    session.pop('result', None)

    session['current_question'] = 'Имя ученика'


def reset_feedback_utility(student_id, first_question):
    db_update_student_info(student_id, info='')

    session['current_question'] = first_question
    session['answers'] = []
