from flask import Blueprint, render_template, redirect, url_for, abort, request
from osh.students.students_utility import parse_and_add_students
from osh.database.database import (
    get_student_by_id,
    get_student_info,
    update_student_notes1,
    update_student_notes2,
    mark_student_absent,
    mark_student_present,
    delete_student_and_info,
    get_group_by_id,
    get_absent_students,
    get_students_for_group,
    add_new_student
)

students_bp = Blueprint('students', __name__,
                        static_folder='static',
                        template_folder='templates'
                        )


@students_bp.route('/<int:group_id>/add_students', methods=['POST'])
def add_students(group_id):
    students_html = request.form.get('studentsHtml')
    parse_and_add_students(group_id, students_html)

    return redirect(url_for('groups.view_group', group_id=group_id))


@students_bp.route('/<int:group_id>/add_new_student', methods=['POST'])
def add_student(group_id):
    full_name = request.form.get('newStudent')

    name, surname = full_name.split(maxsplit=1)

    add_new_student(
        name=f"{name} {surname}",
        group_id=group_id,
    )

    return redirect(url_for('groups.view_group', group_id=group_id))


@students_bp.route('/<int:group_id>/students/<int:student_id>', methods=['GET'])
def view_student(group_id, student_id):
    student = get_student_by_id(student_id)
    if student:
        info = get_student_info(student_id)

        return render_template('student_view.html',
                               student=student,
                               info=info,
                               group_id=group_id)
    else:
        abort(404)


@students_bp.route('/groups/<int:group_id>/delete_student/<int:student_id>',
                   methods=['POST'])
def delete_student(group_id, student_id):
    delete_student_and_info(student_id)

    return redirect(url_for('groups.view_group', group_id=group_id))


# @students_bp.route('/groups/<int:group_id>/students/<int:student_id>/update_notes_lesson1',
#                    methods=['POST'])
# def update_notes1(group_id, student_id):
#     notes_lesson1 = request.form.get('notes_lesson1')
#     update_student_notes1(student_id, notes_lesson1=notes_lesson1)
#
#     return redirect(url_for('groups.view_group', group_id=group_id))
#
#
# @students_bp.route('/groups/<int:group_id>/students/<int:student_id>/update_notes_lesson2',
#                    methods=['POST'])
# def update_notes2(group_id, student_id):
#     notes_lesson2 = request.form.get('notes_lesson2')
#     update_student_notes2(student_id, notes_lesson2=notes_lesson2)
#
#     return redirect(url_for('groups.view_group', group_id=group_id))


@students_bp.route('/groups/<int:group_id>/update_all_notes', methods=['POST'])
def update_all_notes(group_id):
    students = get_students_for_group(group_id)

    for student in students:
        notes_lesson1_key = f'notes_lesson1_{student["id"]}'
        notes_lesson2_key = f'notes_lesson2_{student["id"]}'

        notes_lesson1 = request.form.get(notes_lesson1_key)
        notes_lesson2 = request.form.get(notes_lesson2_key)

        update_student_notes1(student["id"], notes_lesson1=notes_lesson1)
        update_student_notes2(student["id"], notes_lesson2=notes_lesson2)

    return redirect(url_for('groups.view_group', group_id=group_id))


@students_bp.route('/mark_absent/<int:group_id>/<int:student_id>', methods=['POST'])
def mark_absent(group_id, student_id):
    mark_student_absent(student_id)

    return redirect(url_for('groups.view_group', group_id=group_id))


@students_bp.route('/create_absent_list/<int:group_id>', methods=['POST'])
def create_absent_list(group_id):
    group = get_group_by_id(group_id)
    if group:
        absent_students = get_absent_students(group_id)

        return render_template('student_absent.html',
                               absent_students=absent_students,
                               group_id=group_id,
                               group=group)
    else:
        abort(404)


@students_bp.route('/reset_absent/<int:group_id>', methods=['POST'])
def reset_absent_list(group_id):
    group = get_group_by_id(group_id)
    if group:
        students = get_students_for_group(group_id)
        for student in students:
            mark_student_present(student['id'])

        return redirect(url_for('groups.view_group', group_id=group_id))
    else:
        abort(404)
