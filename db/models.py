import hashlib
import re as regex
import typing

from .manager import Manager
from .sqlite import SqliteDb

VALID_EMAIL = regex.compile("[a-z | A-Z |0-9|\.]+@[A-Z|a-z\.]+")


class AbstractField:
    def __init__(self, default=None, null=False):
        self._valid = False
        self._value = None
        self._null = null
        if default != None:
            self.setValue(default)

    @property
    def value(self):
        return self._value

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
    def __init__(self, max_length: int, unique=False, default=None, null=False):
        self._max_length = max_length
        super().__init__(default, null)
        self._unique = unique

    def validate(self) -> bool:
        return isinstance(self._value, str) and len(self._value) <= self._max_length

    def getSqlType(self) -> str:
        return f"VARCHAR ({self._max_length}) {'NULL' if self._null else 'NOT NULL'}"


class EmailField(CharacterField):
    def validate(self) -> bool:
        return super(EmailField, self).validate() and (True if VALID_EMAIL.fullmatch(self._value) else False)


class BooleanField(AbstractField):
    def getSqlType(self) -> str:
        return f"INT {'NULL' if self._null else 'NOT NULL'} {'DEFAULT 1' if self._value == True and self._valid == True else 'DEFAULT 0'}"

    def validate(self) -> bool:
        return isinstance(self._value, bool)


class PasswordField(CharacterField):
    def validate(self) -> bool:
        self._max_length = 128
        return isinstance(self._value, str) and len(self._value) == 64

    def setValue(self, value):
        self._value = hashlib.sha256(str(value).encode()).hexdigest()
        self._valid = self.validate()

    # def


class PositiveIntegerField(AbstractField):
    def __init__(self, default=None, null=False, primary_key=False, auto_increment=False):
        super().__init__(default, null)
        self._primary_key = primary_key
        self._auto_increment = auto_increment

    def validate(self) -> bool:
        return isinstance(self._value, int) and self._value >= 0

    def getSqlType(self) -> str:
        return f"INTEGER {'NULL' if self._null and not self._primary_key else 'NOT NULL'}{' PRIMARY KEY ' if self._primary_key else ' '}{'AUTOINCREMENT' if self._auto_increment and self._primary_key else ''}"


class Model(Manager):
    id_ = PositiveIntegerField(primary_key=True, auto_increment=True)

    def __init__(self, **kwargs):
        super().__init__()
        self._validate_kwargs(kwargs)
        self._meta = Model.Meta(self)
        for key, value in self._get_class_attrs():
            try:
                value.setValue(kwargs[key])
                # print(key, value.__dict__)
            except KeyError:
                pass
            except AttributeError as e:
                raise e

    def _validate_kwargs(self, kwags):
        try:
            for key in kwags:
                getattr(self, key)
        except AttributeError as e:
            raise e

    def _get_inst_attrs(self):
        return [attr for attr in self.__dict__ if not attr.startswith("_")]
        # return Model.__dict__

    def _get_class_attrs(self) -> typing.Tuple[typing.Tuple[str, typing.Any]]:
        raise NotImplementedError()

    def get_filed_name(self) -> typing.Tuple:
        return tuple([field[0] for field in self._get_class_attrs()])

    def get_valid_fields(self) -> typing.Tuple:
        return tuple([f for f in self.get_filed_name() if getattr(self, f)._valid])

    @classmethod
    def create(cls, **kwargs):
        db = SqliteDb.getDatabase()
        model = cls(**kwargs)
        db.insert(model)
        return model
        # return db.schemaChanged(self)

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
