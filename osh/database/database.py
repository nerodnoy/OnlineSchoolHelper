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
