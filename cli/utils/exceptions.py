class CliException(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(f"CliException: {self.message}")
