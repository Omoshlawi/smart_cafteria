import enum
import hashlib
import inspect
import re as regex
import typing
from datetime import datetime, date
from decimal import Decimal

from core.exceptions import ObjectDoesNotExistError, MultipleObjectsError, InvalidArgumentsError
from .manager import Manager
from .sqlite import SqliteDb

VALID_EMAIL = regex.compile("[a-z | A-Z |0-9|\.]+@[A-Z|a-z\.]+")


class BaseAbstractField:
    def __init__(self):
        self._value = None
        self._valid = False
        self._default = None
        self._pk = False
        self._type = None
        self._null = False
        self._index = False
        self._fk = False
        self._unique = False

    @property
    def valid(self) -> bool:
        return self._valid

    @property
    def fk(self):
        return self._fk

    @property
    def null(self) -> bool:
        return self._null

    @property
    def pk(self) -> bool:
        return self._pk

    @property
    def default(self):
        return self._default

    def reset(self):
        self._valid = False
        self._value = None

    @property
    def value(self):
        if self._valid:
            return self._value
        else:
            return None

    @property
    def index(self):
        return self._index

    def validate(self, value) -> bool:
        raise NotImplementedError()

    def setValue(self, value):
        self._valid = self.validate(value)
        self._value = value

    def __str__(self):
        if self._valid:
            return str(self._value)
        else:
            return str(None)

    def __repr__(self):
        return str(self)

    @property
    def type(self):
        return self._type

    def getSqlType(self, field_name) -> str:
        raise NotImplementedError()


class OnRelationShipModified(enum.Enum):
    DELETE_CASCADE = 'ON DELETE CASCADE'
    DELETE_DO_NOTHING = "ON DELETE DO NOTHING"


class AbstractField(BaseAbstractField):
    def __init__(self, default=None, null=False, unique=False, index=False, primary_key=False):
        super().__init__()
        self._null = null
        self._unique = unique
        self._index = index
        self._default = default
        self._pk = primary_key
        if self._default is not None:
            self.setValue(default)

    def validate(self, value) -> bool:
        return super(AbstractField, self).validate(value)

    def getSqlType(self, field_name) -> str:
        return super(AbstractField, self).getSqlType(field_name)


class DateTimeField(AbstractField):
    def __init__(self, default=None, null=False, index=False, auto_now=False, auto_now_add=False):
        super().__init__(default=default, null=null, unique=False, index=index, primary_key=False)
        self._type = 'DATETIME'
        self._auto_now = auto_now
        self._auto_now_add = auto_now_add

    def setValue(self, value):
        self._valid = self.validate(value)
        self._value = str(value)

    def validate(self, value) -> bool:
        if isinstance(value, datetime):
            return True
        elif isinstance(value, str):
            try:
                datetime.fromisoformat(value)
                return True
            except Exception as e:
                return False
        else:
            return False

    def getSqlType(self, field_name) -> str:
        d = f"'{self._default}'"
        return f"{field_name} {self._type} {'NULL' if self._null else 'NOT NULL'} " \
               f"{f'DEFAULT {d}' if self._default is not None and not self._auto_now_add and not self._auto_now else ''}" \
               f" {'DEFAULT CURRENT_TIMESTAMP' if self._auto_now_add else ''}"


class DateField(DateTimeField):
    def __init__(self, default=None, null=False, index=False):
        if isinstance(default, datetime):
            d = default.date()
            super().__init__(d, null, index)
        else:
            super().__init__(default, null, index)
        self._type = 'DATE'

    def setValue(self, value):
        self._valid = self.validate(value)
        if isinstance(value, datetime):
            self._value = str(value.date())
        else:
            self._value = str(value)

    def validate(self, value) -> bool:
        if isinstance(value, date):
            return True
        elif isinstance(value, str):
            try:
                date.fromisoformat(value)
                return True
            except Exception as e:
                return False
        else:
            return False

    def getSqlType(self, field_name) -> str:
        d = f"'{self._default}'"
        return f"{field_name} {self._type} {'NULL' if self._null else 'NOT NULL'} " \
               f"{f'DEFAULT {d}' if self._default is not None and not self._auto_now_add and not self._auto_now else ''}" \
               f" {'DEFAULT CURRENT_DATE' if self._auto_now_add else ''}"


class RelationShipField(BaseAbstractField):
    def __init__(
            self,
            cls,
            on_delete: OnRelationShipModified,
            related_name: str = None
    ):
        super(RelationShipField, self).__init__()
        self._cls = cls
        self._on_delete = on_delete
        self.related_name = related_name
        self._type = "INTEGER"

    def validate(self, value) -> bool:
        return isinstance(value, int) and value > -1

    def getSqKey(self, field_name) -> str:
        if self.fk:
            return f"FOREIGN KEY ({field_name}) REFERENCES {self._cls()._meta.table_name} ({self._cls().getPk()}) {self._on_delete.value}"
        else:
            ''

    def getSqlType(self, field_name) -> str:
        return f"{field_name} {self._type} {'PRIMARY KEY' if self.pk else ''} " \
               f"{'UNIQUE' if self._unique else ''}"


class OneToOneField(RelationShipField):
    def __init__(self, cls, on_delete: OnRelationShipModified, related_name: str = None):
        super().__init__(cls, on_delete, related_name)
        self._pk = False
        self._fk = True
        self._unique = True


class ForeignKeyField(RelationShipField):
    """
    Foreign keys must be adedd after all other fields else it thrown a syntax error
    """

    def __init__(self, cls, on_delete: OnRelationShipModified, related_name: str = None):
        super().__init__(cls, on_delete, related_name)
        self._pk = False
        self._fk = True


class CharacterField(AbstractField):
    def __init__(self, max_length: int, default=None, null=False, unique=False, index=False, primary_key=False):
        super().__init__(default=default, null=null, unique=unique, index=index, primary_key=primary_key)
        self._max_length = max_length
        self._type = f'VARCHAR ({self._max_length})'
        if self._default is not None:
            self.setValue(default)

    def validate(self, value) -> bool:
        return isinstance(value, str) and len(value) <= self._max_length

    def getSqlType(self, field_name) -> str:
        return f"{field_name} {self._type} {self._getSqlPrimaryKey()} {self._getSqlNull()}" \
               f" {self._getSqlDefault()} {self._getSqlUnique()}"

    def _getSqlNull(self):
        # TODO examine all situations to put null
        return f"{'NULL' if self._null and not (self._pk or self._unique) else 'NOT NULL'}"

    def _getSqlDefault(self):
        field = f"'{self._default}'"
        return f'DEFAULT {field}' if self._default is not None and self._valid and not self._pk else ''

    def _getSqlUnique(self):
        return 'UNIQUE' if self._unique and not self._pk else ''

    def _getSqlPrimaryKey(self):
        return f'PRIMARY KEY' if self._pk else ''


class EmailField(CharacterField):
    def validate(self, value) -> bool:
        return super(EmailField, self).validate(value) and (True if VALID_EMAIL.fullmatch(value) else False)


class BooleanField(AbstractField):
    def __init__(self, default=None, null=False, unique=False, index=False):
        super().__init__(default, null, unique, index, primary_key=False)
        self._type = "BOOL"

    @property
    def value(self):
        if self._valid and self._value:
            return 1
        elif self._valid and not self._value:
            return 0
        else:
            return None

    def __str__(self):
        if self._valid:
            return str(self.value == 1)
        else:
            return str(None)

    def setValue(self, value):
        if isinstance(value, bool):
            self._value = 1 if value else 0
        else:
            self._value = value
        self._valid = self.validate(value)

    def getSqlType(self, field_name) -> str:
        return f"{field_name} {self._type} {'NULL' if self._null else 'NOT NULL'}" \
               f" {'DEFAULT 1' if self._valid and self.default == True else ''}" \
               f"{'DEFAULT 0' if self._valid and self.default == False else ''}"

    def validate(self, value) -> bool:
        return isinstance(value, bool)


class PasswordField(CharacterField):
    def __init__(self, max_length: int, index=False):
        super().__init__(max_length, default=None, null=False, unique=False, index=index, primary_key=False)
        self._db_len = 128
        self._type = f'VARCHAR ({self._db_len})'

    def setValue(self, value):
        self._value = hashlib.sha256(str(value).encode()).hexdigest()
        self._valid = isinstance(value, str) and len(value) <= self._max_length

    def setHash(self, hash_):
        self._value = hash_
        self._valid = isinstance(hash_, str) and len(hash_) == 64


class TextField(AbstractField):
    def __init__(self, default=None, null=False):
        super().__init__(default=default, null=null, unique=False, index=False, primary_key=False)
        self._type = "TEXT"

    def getSqlType(self, field_name) -> str:
        return f"{field_name} {self._type} {f'DEFAULT {self._default}' if self._default is not None else ''}" \
               f"{'NULL' if self._null else 'NOT NULL'}"

    def validate(self, value) -> bool:
        return isinstance(value, str) or isinstance(value, float)

    def setValue(self, value):
        self._valid = self.validate(value)
        self._value = str(value)


class DecimalField(AbstractField):
    def __init__(self, max_digits, decimal_places, default=None, null=False, unique=False, index=False,
                 primary_key=False):
        self._max_digits = max_digits
        super().__init__(default, null, unique, index, primary_key)
        self._decimal_places = decimal_places
        self._type = f'DECIMAL ({max_digits}, {decimal_places})'

    @property
    def maxDigits(self):
        return self._max_digits

    @property
    def decimalPlaces(self):
        return self._decimal_places

    def validate(self, value) -> bool:
        return (isinstance(value, int) or isinstance(value, float) or isinstance(value, Decimal)) and len(
            str(value)) <= self._max_digits

    def getSqlType(self, field_name) -> str:
        return f"{field_name} {self._type} {f'DEFAULT {self._default}' if self._default is not None else ''}" \
               f" {'UNIQUE' if self._unique and not self._pk else ''} " \
               f"{'NULL' if self._null and not self._pk else 'NOT NULL'}"


class PositiveIntegerField(AbstractField):
    def __init__(self, default=None, null=False, primary_key=False, auto_increment=False, index=False, unique=False):
        super().__init__(default=default, null=null, unique=unique, index=index, primary_key=primary_key)
        self._auto_increment = auto_increment
        self._type = 'INTEGER'

    def validate(self, value) -> bool:
        return isinstance(value, int) and value >= 0

    def getSqlType(self, field_name) -> str:
        return f"{field_name} {self._type} CHECK(\"{field_name}\">=0) {'NULL' if self._null and not self._pk else 'NOT NULL'}" \
               f"{' PRIMARY KEY ' if self._pk else ' '}" \
               f"{'AUTOINCREMENT' if self._auto_increment and self._pk else ''}" \
               f" {'UNIQUE' if self._unique and not self._pk and not self._null else ''}"

    def getSqKey(self, field_name) -> str:
        return ''


class Model(Manager):
    def __init__(self, **kwargs):
        super().__init__()
        self._validate_kwargs(kwargs)
        self._meta = Model.Meta(self)
        # update the class attrs with the provided ones
        for key, value in self.get_class_attrs():
            try:
                if isinstance(value, BooleanField):
                    value.setValue(kwargs[key] == 1)
                elif isinstance(value, PasswordField):
                    if len(str(kwargs[key])) == 64:
                        value.setHash(kwargs[key])
                    else:
                        value.setValue(kwargs[key])
                else:
                    value.setValue(kwargs[key])
            except KeyError:
                # set the unprovided to default
                value.setValue(getattr(value, "_default"))
            except AttributeError as e:
                raise e
        # TODO CHECK SCHEMA
        db = SqliteDb.getDatabase()
        db.schemaChanged(self)
        db.close()

    def getPk(self):
        for field in self.get_filed_name():
            f = getattr(self, field)
            if f.pk:
                return field

    def getIndexFields(self):
        return [field for field in self.get_filed_name() if getattr(self, field).index]

    def getMultiFieldsIndex(self) -> typing.List[str]:
        return []

    def getValidMultiFieldIndex(self):
        try:
            for col in self.getMultiFieldsIndex():
                getattr(self, col)
        except AttributeError as e:
            raise e

    def _validate_kwargs(self, kwargs):
        try:
            for key in kwargs:
                getattr(self, key)
        except AttributeError as e:
            raise e

    def _get_inst_attrs(self):
        return [attr for attr in self.__dict__ if not attr.startswith("_")]
        # return Model.__dict__

    @classmethod
    def get_class_attrs(cls) -> typing.Tuple[typing.Tuple[str, typing.Any]]:
        attributes = inspect.getmembers(cls, lambda a: not (inspect.isroutine(a)) and not (inspect.isclass(a)))
        attributes = [attr for attr in attributes if not attr[0].startswith("_")]
        return tuple(attributes)

    def get_filed_name(self) -> typing.Tuple:
        return tuple([field[0] for field in self.get_class_attrs()])

    def get_valid_fields(self) -> typing.Tuple:
        return tuple([f for f in self.get_filed_name() if getattr(self, f).valid])

    @classmethod
    def create(cls, **kwargs):
        # TODO STILL MESSY,DOESNT RETURN THE CREATED WELL AS I WANT
        db = SqliteDb.getDatabase()
        model = cls(**kwargs)
        db.insert(model)
        _model = cls.get(**kwargs)
        db.close()
        return _model
        # return db.schemaChanged(self)

    class Meta:
        table_name: str = ""
        fields = []

        def __init__(self, model):
            if not self.table_name:
                self.table_name = model.__class__.__name__

    def save(self) -> 'Model':
        if getattr(self, self.getPk()).valid:
            # performs update
            db = SqliteDb.getDatabase()
            db.update(self)
            model = self
            db.close()
        else:
            kwargs = {key: getattr(self, key).value for key in self.get_valid_fields()}
            model = self.create(**kwargs)
            setattr(self, self.getPk(), getattr(model, model.getPk()))
            return self

    @classmethod
    def get(cls, **kwargs):
        """
        :param kwargs: Attributes for the target record to fetch from the database, the values must be unique
        across all table records
        :return:
        :raises: ObjectDoesNotExistError if no such record in the table
        :raises : MultipleObjectsError if there are multiple objects matching query
        :raises: InvalidArgumentsError when given wrong arguments
        """
        # TODO USE FILTER HERE AND CHECK LENGTH TO DECIDE ERROR TO THROW FOR CODE RE USABILITY
        if not kwargs:
            raise InvalidArgumentsError("Yo must provide at least one keyword argument, none was provided")
        db = SqliteDb.getDatabase()
        try:
            data = db.getRecord(cls(**kwargs), kwargs)
            db.close()
            return cls(**data)
        except ObjectDoesNotExistError as e:
            raise e
        except MultipleObjectsError as e:
            raise e

    def delete(self):
        db = SqliteDb.getDatabase()
        db.delete(self)
        db.close()

    @classmethod
    def all(cls):
        db = SqliteDb.getDatabase()
        records = db.getRecords(cls())
        db.close()
        for rec in records:
            yield cls(**rec)
        # return map(lambda x: cls(**x), records)

    @classmethod
    def filter(cls, **kwargs):
        db = SqliteDb.getDatabase()
        records = db.filterRecord(cls(**kwargs), kwargs)
        db.close()
        # print(records)
        return map(lambda x: cls(**x), records)

    def toJson(self):
        return {field: getattr(self, field).value for field in self.get_filed_name()}
