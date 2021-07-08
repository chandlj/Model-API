class ValidationError(Exception):
    def __init__(self, message="Invalid input"):
        super().__init__(message)

class NotFoundError(Exception):
    def __init__(self, message="Not found"):
        super().__init__(message)
