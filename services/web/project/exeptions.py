class BackendExeption(Exception):
    def __init__(self, error_type: str, error_message: str, *args, **kwargs):
        self.result = False
        self.error_type = error_type
        self.error_message = error_message

    def __repr__(self):
        return {
            "result": False,
            "error_type": self.error_type,
            "error_message": self.error_message,
        }
