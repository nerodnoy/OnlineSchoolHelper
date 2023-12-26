from flask import Blueprint, render_template, request, redirect, url_for, abort
from osh.database.database import add_group, get_all_groups, clear_database, \
    get_students_for_group, get_group_by_id, delete_group_by_id
from osh.utility import calculate_week_in_month

groups_bp = Blueprint('groups', __name__,
                      static_folder='static',
                      template_folder='templates'
                      )


@groups_bp.route('/create', methods=['GET', 'POST'])
def create_group():
    if request.method == 'POST':
        skill = request.form.get('skill')
        time = request.form.get('time')
        day = request.form.get('day')
        link = request.form.get('link')
        start_date = request.form.get('start_date')

        week_number = calculate_week_in_month(start_date)

        group_name = f"{skill} {time} {day}"
        add_group(group_name, link, week_number)

        return redirect(url_for('groups.list_groups'))

    return render_template('group_create.html')


@groups_bp.route('/', methods=['GET'])
def list_groups():
    groups = get_all_groups()

    week_groups = {f'Week_{i}': [group for group in groups if group['week_number'] == i] for i in range(1, 6)}

    return render_template('group_list.html', week_groups=week_groups)


@groups_bp.route('/<int:group_id>/', methods=['GET'])
def view_group(group_id):
    group = get_group_by_id(group_id)
    if group:
        students = get_students_for_group(group_id)

        return render_template('group_view.html',
                               group=group,
                               students=students,
                               group_id=group_id)
    else:
        abort(404)


@groups_bp.route('/<int:group_id>/delete', methods=['POST'])
def delete_group(group_id):
    delete_group_by_id(group_id)

    return redirect(url_for('groups.list_groups'))


@groups_bp.route('/clear_database', methods=['POST'])
def clear_all_data():
    groups = get_all_groups()
    for group in groups:
        clear_database(group['id'])

    return redirect(url_for('groups.list_groups'))
