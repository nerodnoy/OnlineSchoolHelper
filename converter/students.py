from bs4 import BeautifulSoup
from converter.database import add_student, get_group_by_name


def parse_and_add_students(group_name, html_content):
    soup = BeautifulSoup(html_content, 'html.parser')

    # Находим все элементы <h3>, которые содержат имена учеников
    student_names = [h3.text.strip() for h3 in soup.find_all('h3')]

    # Добавляем каждое имя ученика в базу данных с указанием группы
    for name in student_names:
        group = get_group_by_name(group_name)
        if group:
            group_id = group['id']
            add_student(name, group_id=group_id)
