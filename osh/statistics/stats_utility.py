from flask import request

from osh.database.database import db_get_all_groups
from osh.groups.utility.handlers.calendar import get_current_month, translate_month_name


def prepare_stats_data():
    groups = db_get_all_groups()

    current_month = get_current_month()

    selected_month = request.args.get('selected_month')
    selected_month = selected_month or current_month

    translated_month = translate_month_name(selected_month)

    groups_for_month = sorted(
        [group for group in groups if group['month'] == selected_month],
        key=lambda x: x['start_date']
    )

    # Количество групп в месяце
    total_groups = len(groups_for_month)

    # Итоговая оплата за месяц
    total_payment = sum(
        3250 if 'PRO' in group['name'] or 'START' in group['name']
        else 6000 for group in groups_for_month)

    return {
        'groups_for_month': groups_for_month,
        'current_month': translated_month,
        'groups': groups,
        'total_groups': total_groups,
        'total_payment': total_payment
    }
