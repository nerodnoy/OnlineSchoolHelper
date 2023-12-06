questions = {
    'Количество посещенных занятий': {
        'options': ['2', '3'],
        'answers': {
            '2': '____ посетил 2 занятия',
            '3': '____ посетил все три занятия наших мини-курсов'
        },
        'follow_up': {
            '2': 'Какое занятие он пропустил?',
            '3': 'Принимал активное участие?'
        }
    },
    'Принимал активное участие?': {
        'options': ['Да', 'Нет'],
        'answers': {
            'Да': 'и принимал активное участие',
            'Нет': ''
        },
        'follow_up': {
            'Да': 'СЛЕДУЮЩИЙ ВОПРОС ДЛЯ ДА',
            'Нет': 'СЛЕДУЮЩИЙ ВОПРОС ДЛЯ НЕТ'
        }
    },
    'Какое занятие он пропустил?': {
        'options': ['Второе', 'Третье'],
        'answers': {
            'Второе': 'и, к сожалению, пропустил второе.',
            'Третье': 'и, к сожалению, третье занятие пропустил.'
        },
        'follow_up': {
            'Второе': 'СЛЕДУЮЩИЙ ВОПРОС ДЛЯ ВТОРОЕ',
            'Третье': 'СЛЕДУЮЩИЙ ВОПРОС ДЛЯ ТРЕТЬЕ'
        }
    }
    # Добавляем другие вопросы по мере необходимости
}