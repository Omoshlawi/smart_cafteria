class ObjectDoesNotExistError(BaseException):
    def __init__(self, message: str = "No object matching your query"):
        super(ObjectDoesNotExistError, self).__init__(message)


class MultipleObjectsError(BaseException):
    def __init__(self, message: str = "Multiple objects matches your query"):
        super(MultipleObjectsError, self).__init__(message)


class InvalidArgumentsError(BaseException):
    def __init__(self, message: str = "Invalid arguments provided"):
        super(InvalidArgumentsError, self).__init__(message)


class TemplateDoesNotExistError(BaseException):
    def __init__(self, path: str):
        super(TemplateDoesNotExistError, self).__init__(f"Provided template {path} Doesn exits")
