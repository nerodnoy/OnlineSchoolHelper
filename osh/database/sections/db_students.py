from osh.database.database import execute_query


def db_add_students(name, notes_lesson1=None, notes_lesson2=None, present=True, group_id=None):
    query = '''
        INSERT INTO students (
        name, notes_lesson1, notes_lesson2, present, group_id
        ) VALUES (%s, %s, %s, %s, %s) RETURNING id
        '''
    data = (name, notes_lesson1 or '', notes_lesson2 or '', present, group_id)
    execute_query(query, data, commit=True)


def db_get_group_by_id(group_id):
    query = 'SELECT * FROM groups WHERE id=(%s)'
    return execute_query(query, [group_id])


def db_get_students_for_group(group_id):
    query = 'SELECT * FROM students WHERE group_id=(%s) ORDER BY name'
    return execute_query(query, [group_id], fetchall=True)


def db_add_student(
        name, notes_lesson1=None, notes_lesson2=None, present=True, group_id=None):
    query = '''
        INSERT INTO students (
        name, notes_lesson1, notes_lesson2, present, group_id
        ) VALUES (%s, %s, %s, %s, %s) RETURNING id
        '''
    data = (name, notes_lesson1 or '', notes_lesson2 or '', present, group_id)
    execute_query(query, data, commit=True)


def db_get_student_by_id(student_id):
    query = 'SELECT * FROM students WHERE id=(%s)'
    return execute_query(query, [student_id])


def db_get_student_info(student_id):
    query = '''
        SELECT si.info FROM students_info si
        WHERE si.student_id = %s ORDER BY id DESC LIMIT 1
     '''
    data = (student_id,)
    result = execute_query(query, data)
    return result['info'] if result else None


def db_delete_student_and_info(student_id):
    query_info = 'DELETE FROM students_info WHERE student_id = %s'
    execute_query(query_info, [student_id], commit=True)
    query_student = 'DELETE FROM students WHERE id = %s'
    execute_query(query_student, [student_id], commit=True)


def db_update_student_notes1(student_id, notes_lesson1):
    query = 'UPDATE students SET notes_lesson1=%s WHERE id=%s'
    data = (notes_lesson1, student_id)
    execute_query(query, data, commit=True)


def db_update_student_notes2(student_id, notes_lesson2):
    query = 'UPDATE students SET notes_lesson2=%s WHERE id=%s'
    data = (notes_lesson2, student_id)
    execute_query(query, data, commit=True)


def db_mark_student_absent(student_id):
    query = 'UPDATE students SET present=false WHERE id=(%s)'
    execute_query(query, [student_id], commit=True)


def db_mark_student_present(student_id):
    query = 'UPDATE students SET present=True WHERE id=(%s)'
    execute_query(query, [student_id], commit=True)


def db_get_absent_students(group_id):
    query = 'SELECT * FROM students WHERE group_id=(%s) AND present=false ORDER BY name'
    return execute_query(query, [group_id], fetchall=True)


# C этим работаем
def add_student_info(student_id, info):
    query = 'INSERT INTO students_info (student_id, info) VALUES (%s, %s)'
    data = (student_id, info)
    execute_query(query, data, commit=True)


def db_update_student_info(student_id, info):
    query = 'UPDATE students_info SET info=%s WHERE student_id=%s'
    data = (info, student_id)
    execute_query(query, data, commit=True)


def db_save_feedback_to_database(student_id, feedback_data):
    query = "INSERT INTO students_info (student_id, info) VALUES (%s, %s)"
    data = (student_id, feedback_data)
    execute_query(query, data, commit=True)
