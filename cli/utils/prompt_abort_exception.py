class PromptAbortException(Exception):
    def __init__(self, message="User aborted :)"):
        self.message = message
        super().__init__(self.message)
