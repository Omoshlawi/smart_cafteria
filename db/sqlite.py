import sqlite3
import typing
from sqlite3 import Error, Connection

from core.exceptions import ObjectDoesNotExistError, MultipleObjectsError
from settings import SQLITE_DATABASE
from utils.utilities import get_sql_fields

CURRENT_SQL_TIME = "SELECT datetime('now', 'localtime');"


# def getType(field)->str:
#     if isinstance(field, str)

class SqliteDb:
    def __init__(self, conn: Connection):
        self._connection = conn

    def close(self):
        self._connection.close()

    @classmethod
    def getDatabase(cls, db=SQLITE_DATABASE):
        try:
            conn = sqlite3.connect(db)
            return cls(conn)
        except Error as e:
            raise e

    def getRecord(self, model):
        all_fields = model.get_filed_name()
        fields = model.get_valid_fields()
        values = tuple(getattr(model, f).value for f in fields)
        sql = f"""
        SELECT {', '.join(all_fields)} FROM {model._meta.table_name} WHERE {'=? AND '.join(fields)}=?;
        """
        if self._hasMultiple(model):
            raise MultipleObjectsError()
        try:
            c = self._connection.cursor()
            c.execute(sql, values)
            row = c.fetchone()
            c.close()
            if row:
                return dict(zip(all_fields, row))
            else:
                raise ObjectDoesNotExistError()
        except Error as e:
            raise e

    def _hasMultiple(self, model) -> bool:
        all_fields = model.get_filed_name()
        fields = model.get_valid_fields()
        values = tuple(getattr(model, f).value for f in fields)
        sql = f"""
                SELECT {', '.join(all_fields)} FROM {model._meta.table_name} WHERE {'=? AND '.join(fields)}=?;
                """
        try:
            c = self._connection.cursor()
            c.execute(sql, values)
            rows = c.fetchall()
            c.close()
            return len(rows) > 1
        except Error as e:
            raise e

    def alterTable(self, model):
        # TODO Implement my sl
        altered = False
        sql = """
        ALTER 
        """
        try:
            c = self._connection.cursor()
            c.execute(sql)
            altered = True
        except Error as e:
            raise e
        return altered

    def createTable(self, model):
        sql = f"""
                CREATE TABLE IF NOT EXISTS  {model._meta.table_name} (
                    {get_sql_fields(model)}
                );
        """
        try:
            c = self._connection.cursor()
            c.execute(sql)
            c.close()
        except Error as e:
            raise e

    def insert(self, model):
        """
        INSERT INTO User (username, password, first_name, last_name, email) VALUES (
        "ous", "ous", "ous", "ous", "ous");
        :param model:
        :return:
        """
        fields = model.get_valid_fields()
        values = tuple(getattr(model, f).value for f in fields)
        # print(dict(zip(fields, values)))
        sql = f"""INSERT INTO {model._meta.table_name} (
            {", ".join(fields)}
        ) VALUES ( {'?, ' * (len(fields) - 1)}? );
        """
        try:
            c = self._connection.cursor()
            c.execute(sql, values)
            self._connection.commit()
            c.close()
        except Error as e:
            raise e

    def update(self, model):
        fields = list(model.get_valid_fields())
        fields.remove('id_')
        values = [getattr(model, f).value for f in fields]
        values.append(model.id_.value)
        sql = f"""
        UPDATE {model._meta.table_name} SET {'=?, '.join(fields)}=? WHERE id_=?;
        """
        try:
            c = self._connection.cursor()
            c.execute(sql, values)
            self._connection.commit()
            c.close()
        except Error as e:
            raise e

    def dropTable(self, model):
        sql = f"""
        DROP TABLE IF EXISTS {model._meta.table_name}
        """
        try:
            c = self._connection.cursor()
            c.execute(sql)
            c.close()
        except Error as e:
            raise e

    def getSchema(self, model) -> typing.List[typing.Tuple]:
        """
        Sample schema returns
            CID, NAME, TYPE, NOT NULL, DEFAULT VALUE, PK
        [
            (0, '_id', 'INTEGER', 0, None, 1),
            (1, 'email', 'VARCHAR (20)', 1, None, 0),
            (2, 'first_name', 'VARCHAR (20)', 1, None, 0),
            (8, 'username', 'VARCHAR (20)', 1, None, 0)
        ]

        :param model:
        :return:
        """
        sql = f"""
        PRAGMA table_info({model._meta.table_name});
        """
        try:
            c = self._connection.cursor()
            table_schema = c.execute(sql).fetchall()
            c.close()
            return table_schema
        except Error as e:
            raise e

    def tableExists(self, model) -> bool:
        try:
            if self.getSchema(model):
                return True
            return False
        except Error as e:
            return False

    def schemaChanged(self, model):
        if self.tableExists(model):
            schema = self.getSchema(model)
            for field in schema:
                _, name, type_, null, default, pk = field
                changed = f"{type_} {'NOT NULL' if null else 'NULL'} " \
                          f"{f'DEFAULT {default}' if default else ''}" \
                          f"".strip() != getattr(self, name).getSqlType().strip() and name != 'id_'
                if changed:
                    # TODO SHOULD RETURN THE FIELDS THAT CHANGES ARE DETECTED IN
                    return True
        else:
            self.createTable(model)
        return False

    def delete(self, model):
        sql = f"""
        DELETE FROM {model._meta.table_name} WHERE id_=?
        """
        try:
            c = self._connection.cursor()
            c.execute(sql, (model.id_.value,))
            self._connection.commit()
            c.close()
        except Error as e:
            raise e

    def getRecords(self, model) -> typing.List[typing.Dict]:
        """
        :param model:
        :return:
        """
        all_fields = model.get_filed_name()
        sql = f"""
                SELECT {', '.join(all_fields)} FROM {model._meta.table_name};
                """
        try:
            c = self._connection.cursor()
            c.execute(sql)
            rows = c.fetchall()
            c.close()
            return [dict(zip(all_fields, row)) for row in rows]
        except Error as e:
            raise e

    def filterRecord(self, model) -> typing.List[typing.Dict]:
        all_fields = model.get_filed_name()
        fields = model.get_valid_fields()
        values = tuple(getattr(model, f).value for f in fields)
        sql = f"""
        SELECT {', '.join(all_fields)} FROM {model._meta.table_name} WHERE {'=? AND '.join(fields)}=?;
        """
        # print(sql)
        try:
            c = self._connection.cursor()
            c.execute(sql, values)
            rows = c.fetchall()
            c.close()
            return [dict(zip(all_fields, row)) for row in rows]
        except Error as e:
            raise e