class Manager:
    def get(self, **kwargs):
        raise NotImplementedError()

    def filter(self, **kwargs):
        raise NotImplementedError()

    def all(self):
        raise NotImplementedError()

    def create(self, **kwargs):
        raise NotImplementedError()
