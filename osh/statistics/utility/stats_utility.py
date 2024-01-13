from flask import request

from osh.database.db_groups import db_get_all_groups
from osh.groups.utility.handlers.calendar import get_current_month, translate_month_name
from osh.statistics.utility.handlers.stats_handlers import get_groups_for_month, calculate_total_payment


def prepare_stats_data():
    groups = db_get_all_groups()

    current_month = get_current_month()

    selected_month = request.args.get('selected_month')
    selected_month = selected_month or current_month

    translated_month = translate_month_name(selected_month)

    groups_for_month = get_groups_for_month(groups, selected_month)

    total_groups = len(groups_for_month)

    total_payment = calculate_total_payment(groups_for_month)

    return {
        'groups_for_month': groups_for_month,
        'current_month': translated_month,
        'groups': groups,
        'total_groups': total_groups,
        'total_payment': total_payment
    }
