import pymysql

def get_conn():
    conn = pymysql.connect(
        host="localhost",
        port=3306,
        user="root",
        password="123456",
        database="yolo_db",
        charset="utf8mb4"
    )
    return conn