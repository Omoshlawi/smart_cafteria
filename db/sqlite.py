import sqlite3
from sqlite3 import Error, Connection

from settings import SQLITE_DATABASE

CURRENT_SQL_TIME = "SELECT datetime('now', 'localtime');"


# def getType(field)->str:
#     if isinstance(field, str)


def getDatabase() -> Connection:
    conn: Connection = None
    try:
        conn = sqlite3.connect(SQLITE_DATABASE)
        print(f"{sqlite3.version=}")
    except Error as e:
        print(f"{e=}")
    return conn


def create_table(conn: Connection, create_table_sql) -> bool:
    created = False
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
        created = True
    except Error as e:
        print(e)
    finally:
        conn.close()
    return created


def tableExists(conn: Connection, table: str) -> bool:
    exists = False
    sql = f"SELECT {table} FROM sql_master WHERE type='table' AND name='{table}"
    try:
        c = conn.cursor()
        c.execute(sql).fetchall()
        exists = True
    except Error as e:
        pass
    finally:
        conn.close()
    return exists


def getScheema(conn: Connection, table):
    pass
