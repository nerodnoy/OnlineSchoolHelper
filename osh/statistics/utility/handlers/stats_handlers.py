def get_groups_for_month(groups, selected_month):
    return sorted(
        [group for group in groups if group['month'] == selected_month],
        key=lambda x: x['start_date']
    )


def calculate_total_payment(groups_for_month):
    return sum(
        3250 if 'PRO' in group['name'] or 'START' in group['name']
        else 6000 for group in groups_for_month
    )
