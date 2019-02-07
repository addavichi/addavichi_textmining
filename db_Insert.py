import pymysql.cursors

def db_setting():
    conn = pymysql.connect(host='davichiar1.cafe24.com', port=3306, user='davichiar1', passwd='a1b1c1**', db='davichiar1', charset='utf8')
    conn.query("set character_set_connection=utf8;")
    conn.query("set character_set_server=utf8;")
    conn.query("set character_set_client=utf8;")
    conn.query("set character_set_results=utf8;")
    conn.query("set character_set_database=utf8;")
    return conn

def db_search(conn, check):
    result = []
    try:
        with conn.cursor() as cursor:
            sql = 'SELECT * FROM search WHERE nameCheck = %s'
            cursor.execute(sql, (check))
            result = cursor.fetchall()

            print(result[0])
    except:
        pass

    finally:
        return result
        
def db_update(conn, name, check):
    try:
        with conn.cursor() as cursor:
            sql = "UPDATE search SET nameCheck = %s WHERE name = %s"
            cursor.execute(sql, (check, name))
    except:
        pass

def db_update2(conn, id, add):
    try:
        with conn.cursor() as cursor:
            sql = "UPDATE CONTEXT SET ADD_TEXT = %s WHERE ID = %s"
            cursor.execute(sql, (add, id))
    except:
        pass

def db_update3(conn, id, active):
    try:
        with conn.cursor() as cursor:
            sql = "UPDATE CONTEXT SET ACTIVE_TEXT = %s WHERE ID = %s"
            cursor.execute(sql, (active, id))
    except:
        pass

def db_insert(conn, id, title, link, imglink, context1, date, nicname, add, active, text):
    try:
        with conn.cursor() as cursor:
            sql = "INSERT INTO CONTEXT VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            cursor.execute(sql, (id, title, link, imglink, context1, date, nicname, add, active, text))
    except:
        pass

def db_insert2(conn, id, sumnum, addnum, actnum, addper, actper):
    try:
        with conn.cursor() as cursor:
            sql = "INSERT INTO PERCENTIY VALUES (%s, %s, %s, %s, %s, %s)"
            cursor.execute(sql, (id, sumnum, addnum, actnum, addper, actper))
    except:
        pass

def db_insert3(conn, text):
    try:
        with conn.cursor() as cursor:
            sql = "UPDATE CONTEXT SET TEXT = %s"
            cursor.execute(sql, (text))
    except:
        pass

def db_delete1(conn):
    try:
        with conn.cursor() as cursor:
            sql = "DELETE FROM CONTEXT"
            cursor.execute(sql)
    except:
        pass

def db_delete2(conn):
    try:
        with conn.cursor() as cursor:
            sql = "DELETE FROM search WHERE nameCheck = (%s)"
            cursor.execute(sql, ("1"))
    except:
        pass

def db_delete3(conn):
    try:
        with conn.cursor() as cursor:
            sql = "DELETE FROM PERCENTIY"
            cursor.execute(sql)
    except:
        pass

def db_delete4(conn):
    try:
        with conn.cursor() as cursor:
            sql = "DELETE FROM KEYWORD"
            cursor.execute(sql)
    except:
        pass