from flask import request

from osh.database.sections.db_groups import db_get_all_groups
from osh.database.sections.db_stats import db_add_stats, db_get_total_stats
from osh.groups.utility.handlers.calendar import (
    get_current_month,
    translate_month_name
)
from osh.statistics.utility.handlers.stats_handlers import (
    get_groups_for_month,
    calculate_total_payment
)


def get_stats_per_month():
    groups = db_get_all_groups()

    current_month = get_current_month()

    selected_month = request.args.get('selected_month') or current_month

    translated_month = translate_month_name(selected_month)

    groups_for_month = get_groups_for_month(groups, selected_month)

    total_groups = len(groups_for_month)

    total_payment = calculate_total_payment(groups_for_month)

    # Добавляем статистику в базу данных для будущего использования
    db_add_stats(selected_month, total_groups, total_payment)

    return {
        'groups_for_month': groups_for_month,
        'current_month': translated_month,
        'groups': groups,
        'total_groups': total_groups,
        'total_payment': total_payment
    }


def get_total_stats():
    data_list = db_get_total_stats()

    # Преобразование месяцев и сортировка по id_month
    total_stats_data = [
        {
            'month': translate_month_name(data['month']),
            'total_groups': data['total_groups'],
            'total_payment': data['total_payment'],
        }
        for data in sorted(data_list, key=lambda x: x['id_month'])
    ]

    return total_stats_data
