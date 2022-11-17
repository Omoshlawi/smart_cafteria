import typing

from .manager import Manager
from .sqlite import getDatabase


class Model(Manager):
    def __init__(self, **kwargs):
        super().__init__()
        self._meta = Model.Meta(self)
        self._fields = []
        for attr in kwargs:
            try:
                getattr(self, attr)
                setattr(self, attr, kwargs[attr])
            except ValueError as e:
                raise e

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
        """
        Checks if database schemer is up to date
        :return: boolean
        """
        conn = getDatabase()
        if conn:
            pass
        else:
            pass
            #  TODO ADD CODE TO CORRECT CONFLICTING DB SCHEEMER

    def _get_inst_field(self):
        return [attr for attr in self.__dict__ if not attr.startswith("_")]
        # return Model.__dict__

    def _get_class_attrs(self) -> typing.Tuple[typing.Tuple[str, typing.Any]]:
        raise NotImplementedError()


