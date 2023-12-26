from bs4 import BeautifulSoup
from osh.database.database import add_student


def parse_and_add_students(group_id, html_content):
    soup = BeautifulSoup(html_content, 'html.parser')

    student_names = [h3.text.strip() for h3 in soup.find_all('h3')]

    for name in student_names:
        add_student(name, group_id=group_id)
