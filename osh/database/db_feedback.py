from osh.database.database import execute_query


def db_get_student_by_id(student_id):
    query = 'SELECT * FROM students WHERE id=(%s)'
    return execute_query(query, [student_id])


def db_update_student_info(student_id, info):
    query = 'UPDATE students_info SET info=%s WHERE student_id=%s'
    data = (info, student_id)
    execute_query(query, data, commit=True)


def db_save_feedback_to_database(student_id, feedback_data):
    query = "INSERT INTO students_info (student_id, info) VALUES (%s, %s)"
    data = (student_id, feedback_data)
    execute_query(query, data, commit=True)
