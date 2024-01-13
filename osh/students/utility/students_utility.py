from bs4 import BeautifulSoup
from flask import request
from osh.database.db_students import (
    db_add_students,
    db_add_student,
    db_get_student_by_id,
    db_get_student_info,
    db_delete_student_and_info,
    db_get_students_for_group,
    db_update_student_notes1,
    db_update_student_notes2,
    db_mark_student_absent,
    db_mark_student_present,
    db_get_group_by_id,
    db_get_absent_students
)


def add_students_to_group(group_id, html_content):
    soup = BeautifulSoup(html_content, 'html.parser')

    student_names = [h3.text.strip() for h3 in soup.find_all('h3')]

    for name in student_names:
        db_add_students(name, group_id=group_id)


def add_student_to_group(full_name, group_id):
    name, surname = full_name.split(maxsplit=1)

    db_add_student(
        name=f"{name} {surname}",
        group_id=group_id,
    )


def get_student_id_and_info(student_id):
    student = db_get_student_by_id(student_id)
    info = db_get_student_info(student_id)

    return student, info


def delete_student_and_info(student_id):
    db_delete_student_and_info(student_id)


def update_notes_for_group(group_id):
    students = db_get_students_for_group(group_id)

    for student in students:
        update_student_notes(student["id"])


# Обновляем заметки для каждого поля (рефактор)
def update_student_notes(student_id):
    notes_lesson1_key = f'notes_lesson1_{student_id}'
    notes_lesson2_key = f'notes_lesson2_{student_id}'

    notes_lesson1 = request.form.get(notes_lesson1_key)
    notes_lesson2 = request.form.get(notes_lesson2_key)

    db_update_student_notes1(student_id, notes_lesson1=notes_lesson1)
    db_update_student_notes2(student_id, notes_lesson2=notes_lesson2)


def mark_student_absent(student_id):
    db_mark_student_absent(student_id)


def create_absent_list_for_group(group_id):
    group = db_get_group_by_id(group_id)
    absent_students = db_get_absent_students(group_id)

    return absent_students, group


def reset_absent_list_for_group(group_id):
    students = db_get_students_for_group(group_id)

    for student in students:
        db_mark_student_present(student['id'])
