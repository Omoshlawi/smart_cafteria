import enum
import hashlib
import re as regex
import typing
from datetime import datetime

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
        return self.default

    @property
    def value(self):
        return self._value

    @property
    def index(self):
        return self._index

    def validate(self) -> bool:
        raise NotImplementedError()

    def setValue(self, value):
        self._value = value
        self._valid = self.validate()

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

    def validate(self) -> bool:
        return super(AbstractField, self).validate()

    def getSqlType(self, field_name) -> str:
        return super(AbstractField, self).getSqlType(field_name)


class DateTimeField(AbstractField):
    def __init__(self, default=None, null=False, index=False):
        super().__init__(default=default, null=null, unique=False, index=index, primary_key=False)
        self._type = 'DATETIME'
        if self._default is not None:
            self.setValue(default)

    def validate(self) -> bool:
        return isinstance(self._value, datetime)

    def getSqlType(self, field_name) -> str:
        d = f"'{self._default}'"
        return f"{field_name} {self._type} {'NULL' if self._null else 'NOT NULL'} " \
               f"{f'DEFAULT {d}' if self._default is not None else ''}"


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

    def validate(self) -> bool:
        return isinstance(self._value, int) and self._value > -1

    def getSqKey(self, field_name) -> str:
        if self.fk:
            return f"FOREIGN KEY ({field_name}) REFERENCES {self._cls()._meta.table_name} ({self._cls().getPk()}) {self._on_delete.value}"
        else:
            ''

    def getSqlType(self, field_name) -> str:
        return f"{field_name} {self._type} {'PRIMARY KEY' if self.pk else ''}"


class OneToOneField(RelationShipField):
    def __init__(self, cls, on_delete: OnRelationShipModified, related_name: str = None):
        super().__init__(cls, on_delete, related_name)
        self._pk = True
        self._fk = True


class ForeignKeyField(RelationShipField):
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

    def validate(self) -> bool:
        return isinstance(self._value, str) and len(self._value) <= self._max_length

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
    def validate(self) -> bool:
        return super(EmailField, self).validate() and (True if VALID_EMAIL.fullmatch(self._value) else False)


class BooleanField(AbstractField):
    def getSqlType(self, field_name) -> str:
        return f"{field_name} INT {'NULL' if self._null else 'NOT NULL'}" \
               f" {'DEFAULT 1' if self._value == True and self._valid == True else 'DEFAULT 0'}"

    def validate(self) -> bool:
        return isinstance(self._value, bool)


class PasswordField(CharacterField):
    def __init__(self, max_length: int, index=False):
        super().__init__(max_length, default=None, null=False, unique=False, index=index, primary_key=False)
        self._db_len = 128
        self._type = f'VARCHAR ({self._db_len})'

    def setValue(self, value):
        self._value = hashlib.sha256(str(value).encode()).hexdigest()
        self._valid = len(value) >= isinstance(value, str) and self._max_length


class PositiveIntegerField(AbstractField):
    # default=None, null=False, unique=False, index=False, primary_key=False
    def __init__(self, default=None, null=False, primary_key=False, auto_increment=False, index=False, unique=False):
        super().__init__(default=default, null=null, unique=unique, index=index, primary_key=primary_key)
        self._auto_increment = auto_increment

    def validate(self) -> bool:
        return isinstance(self._value, int) and self._value >= 0

    def getSqlType(self, field_name) -> str:
        return f"{field_name} INTEGER {'NULL' if self._null and not self._pk else 'NOT NULL'}" \
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
        for key, value in self._get_class_attrs():
            try:
                if isinstance(value, BooleanField):
                    value.setValue(value.value == 1)
                else:
                    value.setValue(kwargs[key])
                # print(key, value.__dict__)
            except KeyError:
                pass
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

    def _get_class_attrs(self) -> typing.Tuple[typing.Tuple[str, typing.Any]]:
        raise NotImplementedError()

    def get_filed_name(self) -> typing.Tuple:
        return tuple([field[0] for field in self._get_class_attrs()])

    def get_valid_fields(self) -> typing.Tuple:
        return tuple([f for f in self.get_filed_name() if getattr(self, f)._valid])

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

    def save(self, commit=True) -> 'Model':
        model = None
        if commit:
            if self.id_._valid:
                # performs update
                db = SqliteDb.getDatabase()
                db.update(self)
                model = self
                db.close()
            else:
                kwargs = {key: getattr(self, key).value for key in self.get_valid_fields()}
                return self.create(**kwargs)
        else:
            pass

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
            data = db.getRecord(cls(**kwargs))
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
        return map(lambda x: cls(**x), records)

    @classmethod
    def filter(cls, **kwargs):
        db = SqliteDb.getDatabase()
        records = db.filterRecord(cls(**kwargs))
        db.close()
        # print(records)
        return map(lambda x: cls(**x), records)
