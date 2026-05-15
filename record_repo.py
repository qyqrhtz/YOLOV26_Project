from db import get_conn

def insert_record(record: dict):
    conn = get_conn()
    cursor = conn.cursor()

    sql = """
    INSERT INTO detection_record
    (source_image, result_image, target_count, result_json)
    VALUES (%s, %s, %s, %s)
    """

    cursor.execute(sql, (
        record["source_image"],
        record["result_image"],
        record["target_count"],
        record["result_json"]
    ))

    conn.commit()
    cursor.close()
    conn.close()


def get_all_records():
    conn = get_conn()
    cursor = conn.cursor()

    sql = "SELECT * FROM detection_record ORDER BY id DESC"
    cursor.execute(sql)

    rows = cursor.fetchall()
    print(rows)
    print(type(rows))
    results = []
    for row in rows:
        record = {
            "id": row[0],
            "source_image": row[1],
            "result_image": row[2],
            "target_count": row[3],
            "result_json": row[4],
            "created_at": str(row[5])
        }
        results.append(record)
    cursor.close()
    conn.close()

    return results

def delete_record_by_id(record_id: int):
    conn = get_conn()
    cursor = conn.cursor()

    sql = "DELETE FROM detection_record WHERE id = %s"
    cursor.execute(sql, (record_id,))

    conn.commit()
    cursor.close()
    conn.close()