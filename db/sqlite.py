import sqlite3
import typing
from sqlite3 import Error, Connection

from settings import SQLITE_DATABASE
from utils.utilities import get_sql_fields

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


def alter_table(conn: Connection, model):
    # TODO Implement my sl
    altered = False
    sql = """
    ALTER 
    """
    try:
        c = conn.cursor()
        c.execute(sql)
        altered = True
    except Error as e:
        print(e)
    return altered


def create_table(conn: Connection, model) -> bool:
    created = False
    sql = f"""
            CREATE TABLE IF NOT EXISTS  {model._meta.table_name} (
                {get_sql_fields(model)}
            );
    """
    try:
        c = conn.cursor()
        c.execute(sql)
        created = True
    except Error as e:
        print(e)
    return created


def insert(conn: Connection, model):
    """
    INSERT INTO User (username, password, first_name, last_name, email) VALUES (
    "ous", "ous", "ous", "ous", "ous");
    :param conn:
    :param model:
    :return:
    """
    fields = model.get_valid_fields()
    values = tuple(getattr(model, f).value for f in fields)
    print(dict(zip(fields, values)))
    # print(values)
    sql = f"""INSERT INTO {model._meta.table_name} (
        {", ".join(fields)}
    ) VALUES ( {'?, ' * (len(fields)-1)}? );
    """
    # print(sql)
    # print(values)
    data = None
    try:
        c = conn.cursor()
        c.execute(sql, values)
        data = c.fetchall()
        c.close()
        conn.close()
    except Error as e:
        print(e)
    return data


def drop_table(conn: Connection, model):
    dropped = False
    sql = f"""
    DROP TABLE IF EXISTS {model._meta.table_name}
    """
    try:
        c = conn.cursor()
        c.execute(sql)
        dropped = True
    except Error as e:
        print(e)
    return dropped


def getSchema(conn: Connection, table) -> typing.List[typing.Tuple]:
    """
    Sample scheema returns
        CID, NAME, TYPE, NOT NULL, DEFAULT VALUE, PK
    [
        (0, '_id', 'INTEGER', 0, None, 1),
        (1, 'email', 'VARCHAR (20)', 1, None, 0),
        (2, 'first_name', 'VARCHAR (20)', 1, None, 0),
        (8, 'username', 'VARCHAR (20)', 1, None, 0)
    ]

    :param conn:
    :param table:
    :return:
    """
    table_schema = []
    sql = f"""
    PRAGMA table_info({table});
    """
    try:
        c = conn.cursor()
        table_schema = c.execute(sql).fetchall()
    except Error as e:
        print(e)
    return table_schema


def fieldExist(table_schema, field):
    pass
