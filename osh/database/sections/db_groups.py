from osh.database.database import execute_query


def db_add_group(group_name, link=None, start_date=None,
                 week=None, month=None, payment=0, status='Active'):
    query = '''
        INSERT INTO groups (
            name,
            link,
            start_date,
            week,
            month,
            payment,
            status
        ) VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING id
    '''
    data = (group_name, link, start_date, week, month, payment, status)
    result = execute_query(query, data, commit=True)
    return result['id'] if result else None


def db_get_all_groups():
    query = 'SELECT * FROM groups ORDER BY id'
    return execute_query(query, fetchall=True)


def db_get_students_for_group(group_id):
    query = 'SELECT * FROM students WHERE group_id=(%s) ORDER BY name'
    return execute_query(query, [group_id], fetchall=True)


def db_get_active_groups():
    query = 'SELECT * FROM groups WHERE status = %s ORDER BY id'
    return execute_query(query, ('Active',), fetchall=True)


def db_update_group_status(group_id, new_status):
    query = 'UPDATE groups SET status = %s WHERE id = %s'
    data = (new_status, group_id)
    execute_query(query, data, commit=True)


def db_get_group_by_id(group_id):
    query = 'SELECT * FROM groups WHERE id=(%s)'
    return execute_query(query, [group_id])


def db_delete_group_by_id(group_id):
    query_delete_group = 'DELETE FROM groups WHERE id=(%s)'
    execute_query(query_delete_group, [group_id], commit=True)


def db_clear_database(group_id):
    query_info = 'DELETE FROM students_info WHERE group_id = %s'
    execute_query(query_info, (group_id,), commit=True)
    query_delete_students = 'DELETE FROM students WHERE group_id = %s'
    execute_query(query_delete_students, (group_id,), commit=True)
    query_delete_group = 'DELETE FROM groups WHERE id = %s'
    execute_query(query_delete_group, (group_id,), commit=True)
