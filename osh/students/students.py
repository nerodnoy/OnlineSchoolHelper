from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    request
)
from osh.students.students_utility import (
    add_student_to_group,
    add_students_to_group,
    get_student_id_and_info,
    delete_student_and_info,
    update_notes_for_group,
    mark_student_absent,
    create_absent_list_for_group,
    reset_absent_list_for_group
)


students_bp = Blueprint('students', __name__,
                        static_folder='static',
                        template_folder='templates'
                        )


@students_bp.route('/<int:group_id>/add_students', methods=['POST'])
def add_students(group_id):
    students_html = request.form.get('studentsHtml')

    add_students_to_group(group_id, students_html)

    return redirect(url_for('groups.view_group', group_id=group_id))


@students_bp.route('/<int:group_id>/add_new_student', methods=['POST'])
def add_student(group_id):
    full_name = request.form.get('newStudent')

    add_student_to_group(full_name, group_id)

    return redirect(url_for('groups.view_group', group_id=group_id))


@students_bp.route('/<int:group_id>/students/<int:student_id>', methods=['GET'])
def view_student(group_id, student_id):
    student, info = get_student_id_and_info(student_id)

    return render_template('student_view.html',
                           student=student,
                           info=info,
                           group_id=group_id)


@students_bp.route('/groups/<int:group_id>/delete_student/<int:student_id>',
                   methods=['POST'])
def delete_student(group_id, student_id):
    delete_student_and_info(student_id)

    return redirect(url_for('groups.view_group', group_id=group_id))


@students_bp.route('/groups/<int:group_id>/update_all_notes', methods=['POST'])
def update_notes(group_id):
    update_notes_for_group(group_id)

    return redirect(url_for('groups.view_group', group_id=group_id))


@students_bp.route('/mark_absent/<int:group_id>/<int:student_id>', methods=['POST'])
def mark_absent(group_id, student_id):
    mark_student_absent(student_id)

    return redirect(url_for('groups.view_group', group_id=group_id))


@students_bp.route('/create_absent_list/<int:group_id>', methods=['POST'])
def create_absent_list(group_id):
    absent_students, group = create_absent_list_for_group(group_id)

    return render_template('student_absent.html',
                           absent_students=absent_students,
                           group_id=group_id,
                           group=group)


@students_bp.route('/reset_absent/<int:group_id>', methods=['POST'])
def reset_absent_list(group_id):
    reset_absent_list_for_group(group_id)

    return redirect(url_for('groups.view_group', group_id=group_id))
