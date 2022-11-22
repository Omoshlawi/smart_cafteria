class ObjectDoesNotExistError(Exception):
    def __init__(self, message: str = "No object matching your query"):
        super(ObjectDoesNotExistError, self).__init__(message)


class MultipleObjectsError(Exception):
    def __init__(self, message: str = "Multiple objects matches your query"):
        super(MultipleObjectsError, self).__init__(message)


class InvalidArgumentsError(Exception):
    def __init__(self, message: str = "Invalid arguments provided"):
        super(InvalidArgumentsError, self).__init__(message)


class TemplateDoesNotExistError(Exception):
    def __init__(self, path: str):
        super(TemplateDoesNotExistError, self).__init__(f"Provided template {path} Doesn exits")


class InvalidArgumentError(Exception):
    def __init__(self, message="Invalid arguments Error"):
        super(InvalidArgumentError, self).__init__(message)
