class DatabaseOperationException(Exception):

    def __init__(self, message="Something went wrong"):
        self.message = message
        super().__init__(self.message)