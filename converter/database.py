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
                           name TEXT NOT NULL)''')


def add_group(group_name):
    query = 'INSERT INTO groups (name) VALUES (%s)'
    data = (group_name,)
    execute_query(query, data, commit=True)


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