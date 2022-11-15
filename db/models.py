from .manager import Manager


class Model(object):
    objects: Manager = Manager()

    def __init__(self, **kwargs):
        # if 'username' in kwargs:
        #     self.username = kwargs['username']
        # if 'password' in kwargs:
        #     self.password = kwargs['password']
        # if 'first_name' in kwargs:
        #     self.first_name = kwargs['first_name']
        # if 'last_name' in kwargs:
        #     self.last_name = kwargs['last_name']
        # if 'is_active' in kwargs:
        #     self.is_staff = kwargs['is_active']
        # if 'is_staff' in kwargs:
        #     self.is_staff = kwargs['is_staff']
        # if 'is_admin' in kwargs:
        #     self.is_admin = kwargs['is_admin']
        super().__init__()
        for attr in kwargs:
            try:
                getattr(self, attr)
                setattr(self, attr, kwargs[attr])
            except ValueError as e:
                raise e

    def save(self, commit=True) -> 'Model':
        raise NotImplemented()

    def delete(self):
        raise NotImplemented()

    class Meta:
        table_name: str = ""
