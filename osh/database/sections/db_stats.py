from osh.database.database import execute_query


def db_add_stats(month, total_groups, total_payment):
    query = """
        INSERT INTO stats (id_month, month, total_groups, total_payment)
        VALUES (
            (SELECT COALESCE(MAX(id_month), 0) + 1 FROM stats),
            %s, %s, %s
        )
        ON CONFLICT (id_month) DO UPDATE
        SET total_groups = EXCLUDED.total_groups,
            total_payment = EXCLUDED.total_payment
    """
    data = (month, total_groups, total_payment)
    execute_query(query, data, commit=True)
    data = (month, total_groups, total_payment)
    execute_query(query, data, commit=True)


def db_get_total_stats():
    query = """
        SELECT id_month, month, total_groups, total_payment
        FROM stats
        ORDER BY id_month;
    """
    return execute_query(query, fetchall=True)
