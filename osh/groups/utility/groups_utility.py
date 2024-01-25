from osh.database.sections.db_groups import (
    db_add_group,
    db_get_all_groups,
    db_get_active_groups,
    db_get_group_by_id,
    db_get_students_for_group,
    db_update_group_status,
    db_delete_group_by_id,
    db_clear_database
)
from osh.groups.utility.handlers.functions import (
    get_week_groups,
    get_selected_month,
    get_translated_month,
    get_current_week_and_month,
    get_groups_for_current_week,
    get_groups_for_current_month
)
from osh.groups.utility.handlers.calendar import (
    calculate_week_in_month,
    calculate_month,
    get_current_day,
    get_current_week,
    get_current_month
)


def create_new_group(request):
    skill = request.form.get('skill')
    time = request.form.get('time')

    if time == "custom":
        custom_time = request.form.get('custom_time')
        if not custom_time:
            return None
        time = custom_time

    day_of_week = request.form.get('day')
    link = request.form.get('link')
    start_date = request.form.get('start_date')

    week = calculate_week_in_month(start_date)
    month = calculate_month(start_date)

    if skill in ('START', 'PRO'):
        payment = 3250
    else:
        payment = 7500

    group_name = f"{skill} {time} {day_of_week}"
    db_add_group(group_name, link, start_date, week, month, payment)

    return group_name


def get_group_data(request):
    groups = db_get_all_groups()
    active_groups = db_get_active_groups()
    current_week, current_month = get_current_week_and_month()

    current_week_groups = get_groups_for_current_week(groups, current_week, current_month)

    selected_month = get_selected_month(request, current_month)
    translated_month = get_translated_month(selected_month)

    filtered_groups = get_groups_for_current_month(groups, selected_month)
    week_groups = get_week_groups(filtered_groups)

    active = request.args.get('active')

    current_day = get_current_day()

    return {
        'current_week_groups': current_week_groups,
        'week_groups': week_groups,
        'current_month': translated_month,
        'groups': active_groups if active else groups,
        'active_groups': active_groups,
        'active': active,
        'current_day': current_day
    }


def get_group_and_students(group_id):
    group = db_get_group_by_id(group_id)
    students = db_get_students_for_group(group_id)

    return group, students


def update_group_status_toggle(group_id):
    group = db_get_group_by_id(group_id)
    current_status = group['status']
    new_status = 'Finished' if current_status == 'Active' else 'Active'
    db_update_group_status(group_id, new_status)


def delete_group_by_id(group_id):
    db_delete_group_by_id(group_id)


def clear_all_data_from_db():
    groups = db_get_all_groups()
    for group in groups:
        db_clear_database(group['id'])


def inject_groups_utility():
    active_groups = db_get_active_groups()
    current_month = get_current_month()
    current_week = get_current_week()

    current_week_groups = get_groups_for_current_week(
        active_groups, current_week, current_month)

    return dict(current_week_groups=current_week_groups, active_groups=active_groups)
