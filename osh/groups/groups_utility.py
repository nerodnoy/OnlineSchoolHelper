from datetime import datetime


def get_current_month():
    return datetime.now().strftime('%B')


def get_current_week():
    today = datetime.now()
    first_day_of_month = today.replace(day=1)
    current_week_in_month = (today - first_day_of_month).days // 7 + 1
    return current_week_in_month


def calculate_week_in_month(start_date):
    start_date_obj = datetime.strptime(start_date, '%Y-%m-%d')
    week = (start_date_obj.day - 1) // 7 + 1

    return week


def calculate_month(start_date):
    start_date_obj = datetime.strptime(start_date, '%Y-%m-%d')
    month = start_date_obj.strftime('%B')

    return month


def translate_month_name(month_name):
    month_translation = {
        'January': 'Январь',
        'February': 'Февраль',
        'March': 'Март',
        'April': 'Апрель',
        'May': 'Май',
        'June': 'Июнь',
        'July': 'Июль',
        'August': 'Август',
        'September': 'Сентябрь',
        'October': 'Октябрь',
        'November': 'Ноябрь',
        'December': 'Декабрь'
    }

    return month_translation.get(month_name, month_name)


def filter_groups(groups, week, month):
    return [group for group in groups if group['week'] == week and group['month'] == month]
