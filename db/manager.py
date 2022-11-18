class Manager:
    @classmethod
    def get(cls, **kwargs):
        raise NotImplementedError()

    @classmethod
    def filter(cls, **kwargs):
        raise NotImplementedError()

    @classmethod
    def all(cls):
        raise NotImplementedError()

    @classmethod
    def create(cls, **kwargs):
        raise NotImplementedError()
