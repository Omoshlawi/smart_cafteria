import os
import sqlite3
import typing
from sqlite3 import Error, Connection

from core.exceptions import ObjectDoesNotExistError, MultipleObjectsError
from settings import SQLITE_DATABASE

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

    def fullBackUp(self, path: str):
        # TODO full back up on diSK
        """
        BACKUP DATABASE <databasename>
        TO DISK = '<filepath>';
        :return:
        """
        name = '<dbName>.bak'
        sql = f"""
        BACKUP DATABASE <dbName>
            TO DISK = '{os.path.join(path, name)}';
        """
        try:
            raise NotImplementedError()
            # c = self._connection.cursor()
            # c.execute(sql)
            # c.close()
        except Error as e:
            raise e

    def deferentialBackUp(self, path: str):
        # TODO deferential back up on diSK
        """
        Tip: A differential back up reduces the back up time (since only the changes are backed up).
        BACKUP DATABASE <databasename>
        TO DISK = 'filepath'
        WITH DIFFERENTIAL;
        :return:
        """
        name = '<dbName>.bak'
        sql = f"""
            BACKUP DATABASE testDB
            TO DISK = '{os.path.join(path, name)}'
            WITH DIFFERENTIAL;
                """
        try:
            raise NotImplementedError()
            # c = self._connection.cursor()
            # c.execute(sql)
            # c.close()
        except Error as e:
            raise e

    def alterTable(self, model):
        """
        Alter table column for:
            SQL Server / MS Access::
                ALTER TABLE table_name
                ALTER COLUMN column_name datatype;
            My SQL / Oracle (prior version 10G):
                ALTER TABLE table_name
                MODIFY COLUMN column_name datatype;
            Oracle 10G and later:
                ALTER TABLE table_name
                MODIFY column_name datatype;



        :param model:
        :return:
        """
        # TODO Implement my sl
        altered = False
        sql = f"""
        ALTER TABLE {model._meta.table_name}
        """
        try:
            c = self._connection.cursor()
            c.execute(sql)
            altered = True
        except Error as e:
            raise e
        return altered

    def createTable(self, model):
        """

        :param model:
        :return:
        """
        sql = f"""
                CREATE TABLE IF NOT EXISTS  {model._meta.table_name} (
                    {self.get_sql_fields(model)}
                );
        """
        # print(sql)
        try:
            c = self._connection.cursor()
            c.execute(sql)
            c.close()
        except Error as e:
            raise e

    def createTableFromAnother(self, modelNew, modelTarget):
        """
        A copy of an existing table can also be created using CREATE TABLE.
        The new table gets the same column definitions. All columns or specific
        columns can be selected.
        If you create a new table using an existing table, the new table will
        be filled with the existing values from the old table.

        :param modelNew:
        :param modelTarget:
        :return:

        :example
        CREATE TABLE newTable AS
        SELECT customername, contactname
        FROM customers;

        :syntax
        CREATE TABLE new_table_name AS
        SELECT column1, column2,...
        FROM existing_table_name
        WHERE ....;
        """
        raise NotImplementedError()

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
        fields.remove(model.getPk())
        values = [getattr(model, f).value for f in fields]
        values.append(getattr(model, model.getPk()).value)
        sql = f"""
        UPDATE {model._meta.table_name} SET {'=?, '.join(fields)}=? WHERE {model.getPk()}=?;
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
                changed = True
                if changed:
                    # TODO SHOULD RETURN THE FIELDS THAT CHANGES ARE DETECTED IN
                    return True
        else:
            self.createTable(model)
        return False

    def delete(self, model):
        sql = f"""
        DELETE FROM {model._meta.table_name} WHERE {model.getPk()}=?
        """
        try:
            c = self._connection.cursor()
            c.execute(sql, (getattr(model, model.getPk()).value,))
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

    def getRecord(self, model, search_fields):
        all_fields = model.get_filed_name()
        fields = tuple(search_fields.keys())
        values = tuple(getattr(model, f).value for f in fields)
        sql = f"""
        SELECT {', '.join(all_fields)} FROM {model._meta.table_name} WHERE {'=? AND '.join(fields)}=?;
        """
        # print(dict(zip(fields, values)))
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

    def filterRecord(self, model, filter_fields: dict) -> typing.List[typing.Dict]:
        all_fields = model.get_filed_name()
        fields = tuple(filter_fields.keys())
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

    def createIndex(self, model):
        indexed = model.getIndexFields()
        for i in indexed:
            sql = f"""
            CREATE INDEX idx_{i} ON {model._meta.table_name} ({i});
            """
            try:
                c = self._connection.cursor()
                c.execute(sql)
                c.close()
            except Error as e:
                raise e

    def createMultiColumnIndex(self, model):
        index = model.getValidMultiFieldIndex()
        name = "_".join(index)
        sql = f"""
        CREATE INDEX idx_{name} ON {model._meta.table_name} ({", ".join(index)});
        """
        try:
            c = self._connection.cursor()
            c.execute(sql)
            c.close()
        except Error as e:
            raise e

    def getIndexes(self, model):
        sql = f"""
        SHOW INDEXES IN {model._meta.table_name}
        """
        try:
            c = self._connection.cursor()
            c.execute(sql)
            c.close()
        except Error as e:
            raise e

    @staticmethod
    def get_sql_fields(model):
        sql_fields = [getattr(model, field).getSqlType(field) for field in model.get_filed_name()]
        related_fields = [
            getattr(model, field).getSqKey(field) for field in model.get_filed_name()
            if getattr(model, field).fk or getattr(model, field).pk and getattr(model, field).getSqKey(field)
        ]

        sql_fields.extend(related_fields)
        return ", \n".join(sql_fields)
