from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    abort
)
from osh.database.database import (
    add_group,
    get_all_groups,
    clear_database,
    get_students_for_group,
    get_group_by_id,
    delete_group_by_id,
    get_active_groups,
    update_group_status
)
from osh.groups.groups_utility import (
    calculate_week_in_month,
    calculate_month,
    get_current_month,
    translate_month_name,
    get_current_week,
    filter_groups,
    get_current_day
)

groups_bp = Blueprint('groups', __name__,
                      static_folder='static',
                      template_folder='templates'
                      )


@groups_bp.route('/create', methods=['GET', 'POST'])
def create_group():
    if request.method == 'POST':
        skill = request.form.get('skill')
        time = request.form.get('time')

        if time == "custom":
            custom_time = request.form.get('custom_time')
            if not custom_time:
                return redirect(url_for('groups.create_group'))
            time = custom_time

        day_of_week = request.form.get('day')
        link = request.form.get('link')
        start_date = request.form.get('start_date')

        week = calculate_week_in_month(start_date)
        month = calculate_month(start_date)

        # Определение платы в зависимости от уровня
        if skill in ('START', 'PRO'):
            payment = 3250
        else:
            payment = 6000

        group_name = f"{skill} {time} {day_of_week}"
        add_group(group_name, link, start_date, week, month, payment)

        return redirect(url_for('groups.list_groups'))

    current_day = get_current_day()

    return render_template('group_create.html', current_day=current_day)


@groups_bp.route('/', methods=['GET'])
def list_groups():
    groups = get_all_groups()

    active_groups = get_active_groups()

    current_month = get_current_month()
    current_week = get_current_week()

    # Это для drop-down menu
    current_week_groups = filter_groups(groups, current_week, current_month)

    selected_month = request.args.get('selected_month')
    selected_month = selected_month or current_month

    translated_month = translate_month_name(selected_month)

    filtered_groups = [group for group in groups if group['month'] == selected_month]

    week_groups = {f'Неделя {i}': [
        group for group in filtered_groups if group['week'] == i] for i in range(1, 6)}

    active = request.args.get('active')

    current_day = get_current_day()

    return render_template('group_list.html',
                           current_week_groups=current_week_groups,
                           week_groups=week_groups,
                           current_month=translated_month,
                           groups=active_groups if active else groups,
                           active_groups=active_groups,
                           active=active,
                           current_day=current_day
                           )


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


@groups_bp.route('/<int:group_id>/update_status', methods=['POST'])
def update_group_status_route(group_id):
    group = get_group_by_id(group_id)

    current_status = group['status']
    new_status = 'Finished' if current_status == 'Active' else 'Active'

    update_group_status(group_id, new_status)

    return redirect(url_for('groups.view_group', group_id=group_id))


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
