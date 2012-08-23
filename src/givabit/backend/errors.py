class IllegalStateException(Exception):
    pass

class MissingValueException(Exception):
    pass

class MultipleValueException(Exception):
    def __init__(self, msg, values):
        self.msg = msg
        self.values = values
