import psycopg2
from psycopg2.extras import RealDictCursor
import os

DATABASE_URL = os.getenv('DATABASE_URL')


def execute_query(query, data=None, commit=False, fetchall=False):
    with psycopg2.connect(DATABASE_URL) as connection:
        with connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(query, data)

            if commit:
                connection.commit()
                return

            if fetchall:
                result = cursor.fetchall()
            else:
                result = cursor.fetchone()

        return result


def create_table():
    with psycopg2.connect(DATABASE_URL) as connection:
        cursor = connection.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS groups
                          (id SERIAL PRIMARY KEY,
                           name TEXT NOT NULL,
                           link TEXT)''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS students
                          (id SERIAL PRIMARY KEY,
                           name VARCHAR(255) NOT NULL,
                           notes_lesson1 TEXT,
                           notes_lesson2 TEXT,
                           present BOOLEAN,
                           group_id INTEGER REFERENCES groups(id) ON DELETE CASCADE)''')


def add_group(group_name, link=None):
    query = 'INSERT INTO groups (name, link) VALUES (%s, %s) RETURNING id'
    data = (group_name, link)
    result = execute_query(query, data, commit=True)
    return result['id'] if result else None


def get_all_groups():
    query = 'SELECT * FROM groups ORDER BY id'
    return execute_query(query, fetchall=True)


def get_group_by_name(group_name):
    query = 'SELECT * FROM groups WHERE name=(%s)'
    return execute_query(query, [group_name])


def delete_group(group_name):
    query = 'DELETE FROM groups WHERE name=(%s)'
    execute_query(query, [group_name], commit=True)


def clear_database():
    query = 'DELETE FROM groups'
    execute_query(query, commit=True)


def add_student(name, notes_lesson1=None, notes_lesson2=None, present=True, group_id=None):
    query = 'INSERT INTO students (name, notes_lesson1, notes_lesson2, present, group_id) VALUES (%s, %s, %s, %s, %s)'
    data = (name, notes_lesson1 or '', notes_lesson2 or '', present, group_id)
    execute_query(query, data, commit=True)


def get_students_for_group(group_id):
    query = 'SELECT * FROM students WHERE group_id=(%s) ORDER BY name'
    return execute_query(query, [group_id], fetchall=True)


def delete_student(student_id):
    query = 'DELETE FROM students WHERE id=(%s)'
    execute_query(query, [student_id], commit=True)


def update_student_notes1(student_id, notes_lesson1):
    query = 'UPDATE students SET notes_lesson1=%s WHERE id=%s'
    data = (notes_lesson1, student_id)
    execute_query(query, data, commit=True)


def update_student_notes2(student_id, notes_lesson2):
    query = 'UPDATE students SET notes_lesson2=%s WHERE id=%s'
    data = (notes_lesson2, student_id)
    execute_query(query, data, commit=True)


def mark_student_absent(student_id):
    query = 'UPDATE students SET present=false WHERE id=(%s)'
    execute_query(query, [student_id], commit=True)


def get_absent_students(group_id):
    query = 'SELECT * FROM students WHERE group_id=(%s) AND present=false ORDER BY name'
    return execute_query(query, [group_id], fetchall=True)


def get_student_by_id(student_id):
    query = 'SELECT * FROM students WHERE id=(%s)'
    return execute_query(query, [student_id])