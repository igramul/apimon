class ConnectionException(Exception):
    """Custom exception class for connection-related errors."""

    def __init__(self, message: str = "A connection error occurred"):
        super().__init__(message)

