class APIError(Exception):
    """Raised when API error occurs."""

    def __init__(self, message: str, code: int = 400, error_type: str = None):
        self.message = message
        self.code = code
        self.error_type = error_type


class UnauthorizedError(APIError):
    """Raised when API error occurs."""

    def __init__(
            self,
            msg: str = 'Unauthorized',
            code: int = 401,
            error_type: str = None
    ):
        super().__init__(
            msg,
            code,
            error_type
        )
