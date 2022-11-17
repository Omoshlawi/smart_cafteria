import os
import sqlite3
from sqlite3 import Error, Connection

from settings import SQLITE_DATABASE


def getDatabase() -> Connection:
    conn: Connection = None
    if os.path.exists(SQLITE_DATABASE):
        try:
            conn = sqlite3.connect(SQLITE_DATABASE)
            print(f"{getDatabase.__module__}, {sqlite3.version=}")
        except Error as e:
            print(f"{getDatabase().__module__}, {e=}")
    return conn


def create_table(conn: Connection, create_table_sql) -> bool:
    created = False
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
        created = True
    except Error as e:
        print(e)
    return created


def getTables(conn:Connection):
    tables = None
    TABLES_SQL = """
            SHOW TABLES;
        """
    try:
        c = conn.cursor()
        c.execute(TABLES_SQL)
    except Error as e:
        print(e)




def getScheema(conn:Connection, table):
    pass

