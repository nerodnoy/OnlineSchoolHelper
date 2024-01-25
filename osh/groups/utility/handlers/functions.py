from osh.groups.utility.handlers.calendar import (
    get_current_week,
    get_current_month,
    translate_month_name
)


def get_current_week_and_month():
    current_week = get_current_week()
    current_month = get_current_month()
    return current_week, current_month


def get_selected_month(request, current_month):
    selected_month = request.args.get('selected_month')
    return selected_month or current_month


def get_translated_month(selected_month):
    return translate_month_name(selected_month)


def get_groups_for_current_week(groups, week, month):
    return [group for group in groups if group['week'] == week and group['month'] == month]


def get_groups_for_current_month(groups, selected_month):
    return [group for group in groups if group['month'] == selected_month]


def get_week_groups(filtered_groups):
    return {f'Неделя {i}': [group for group in filtered_groups
                            if group['week'] == i] for i in range(1, 6)}
