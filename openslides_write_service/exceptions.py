class BackendBaseException(Exception):
    def __init__(self, message):
        self.message = message


class MediaTypeException(BackendBaseException):
    pass


class ActionException(BackendBaseException):
    pass


class EventStoreException(BackendBaseException):
    pass
