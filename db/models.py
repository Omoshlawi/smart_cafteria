import re as regex
import typing

from .manager import Manager
from .sqlite import getDatabase, tableExists, create_table

VALID_EMAIL = regex.compile("[a-z | A-Z |0-9|\.]+@[A-Z|a-z\.]+")


class Model(Manager):

    def __init__(self, **kwargs):
        super().__init__()
        self._meta = Model.Meta(self)
        for key, value in self._get_class_attrs():
            try:
                value.setValue(kwargs[key])
                # print(key, value.__dict__)
            except KeyError:
                pass
        """for attr in kwargs:
            try:
                cls = type(getattr(self, attr))
                val = cls(default=kwargs[attr])
                print(val)
                setattr(self, attr, val)
            except ValueError as e:
                raise e"""

    def create(self, **kwargs):
        pass

    class Meta:
        table_name: str = ""
        fields = []

        def __init__(self, model):
            if not self.table_name:
                self.table_name = model.__class__.__name__

    def save(self, commit=True) -> 'Model':
        if commit:
            pass
        else:
            pass

    def get(self, **kwargs):
        pass

    def delete(self):
        pass

    def all(self) -> typing.List['Model']:
        print(self._meta.table_name)
        return []

    def filter(self, **kwargs):
        for field in kwargs:
            pass

    def is_db_upto_date(self) -> bool:
        up_to_date = False
        """
        Checks if database schemer is up to date
        :return: boolean
        """
        conn = getDatabase()
        if conn:
            if tableExists(conn, self._meta.table_name):
                pass
            else:
                sql = f"""CREATE TABLE IF NOT EXISTS  {self._meta.table_name} (
                            """
                create_table(conn, sql)
        else:
            pass
            #  TODO ADD CODE TO CORRECT CONFLICTING DB SCHEMER
        return up_to_date

    def _get_inst_attrs(self):
        return [attr for attr in self.__dict__ if not attr.startswith("_")]
        # return Model.__dict__

    def _get_class_attrs(self) -> typing.Tuple[typing.Tuple[str, typing.Any]]:
        raise NotImplementedError()

    def get_filed_name(self) -> typing.Tuple:
        return tuple([field[0] for field in self._get_class_attrs()])


class AbstractField:
    def __init__(self, default=None):
        self._valid = False
        self._value = None
        if default != None:
            self.setValue(default)

    def validate(self) -> bool:
        raise NotImplementedError()

    def setValue(self, value):
        self._value = value
        self._valid = self.validate()

    def getSqlType(self) -> str:
        raise NotImplementedError()

    def __str__(self):
        if self._valid:
            return str(self._value)
        else:
            return str(None)

    def __repr__(self):
        return str(self)


class CharacterField(AbstractField):
    def __init__(self, max_length: int, unique=False, default=None):
        self._max_length = max_length
        super().__init__(default)
        self._unique = unique

    def validate(self) -> bool:
        return isinstance(self._value, str) and len(self._value) <= self._max_length

    def getSqlType(self) -> str:
        return f"VARCHAR ({self._max_length})"


class EmailField(CharacterField):
    def validate(self) -> bool:
        return super(EmailField, self).validate() and (True if VALID_EMAIL.fullmatch(self._value) else False)


class BooleanField(AbstractField):
    def getSqlType(self) -> str:
        return "INT"

    def validate(self) -> bool:
        return isinstance(self._value, bool)
