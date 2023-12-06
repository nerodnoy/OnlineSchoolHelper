def generate_telegram_link(phone_number):
    cleaned_phone_number = ''.join(
        char for char in phone_number if char.isnumeric() or char == '+'
    )

    if not cleaned_phone_number.startswith('+'):
        cleaned_phone_number = '+' + cleaned_phone_number

    telegram_link = f"t.me/{cleaned_phone_number}"
    return telegram_link
