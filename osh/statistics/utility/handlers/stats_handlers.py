def get_groups_for_month(groups, selected_month):
    return sorted(
        [group for group in groups if group['month'] == selected_month],
        key=lambda x: x['start_date']
    )


def calculate_total_payment(groups_for_month):
    total_payment = sum(group['payment'] for group in groups_for_month)

    return total_payment
