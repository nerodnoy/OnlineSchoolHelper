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


def create_tables():
    query_groups = """
        CREATE TABLE IF NOT EXISTS groups (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            link TEXT,
            start_date DATE,
            week INTEGER NOT NULL,
            month TEXT NOT NULL,
            payment INTEGER,
            status VARCHAR(50) DEFAULT 'Active' NOT NULL
        );
    """

    query_students = """
        CREATE TABLE IF NOT EXISTS students (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            notes_lesson1 TEXT,
            notes_lesson2 TEXT,
            present BOOLEAN,
            group_id INTEGER REFERENCES groups(id) ON DELETE CASCADE
        );
    """

    query_students_info = """
        CREATE TABLE IF NOT EXISTS students_info (
            id SERIAL PRIMARY KEY,
            student_id INTEGER REFERENCES students(id) ON DELETE CASCADE,
            group_id INTEGER REFERENCES groups(id) ON DELETE CASCADE,
            info TEXT
        );
    """

    query_stats = """
        CREATE TABLE IF NOT EXISTS stats (
            id SERIAL PRIMARY KEY,
            id_month INTEGER,
            month TEXT REFERENCES groups(month),
            total_groups INTEGER,
            total_payment INTEGER
        );
    """

    execute_query(query_groups, commit=True)
    execute_query(query_students, commit=True)
    execute_query(query_students_info, commit=True)
    execute_query(query_stats, commit=True)
