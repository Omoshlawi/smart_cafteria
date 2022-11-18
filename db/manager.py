class Manager:
    def get(self, **kwargs):
        raise NotImplementedError()

    def filter(self, **kwargs):
        raise NotImplementedError()

    def all(self):
        raise NotImplementedError()

    @classmethod
    def create(cls, **kwargs):
        raise NotImplementedError()
