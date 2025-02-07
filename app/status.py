from enum import Enum, auto


class STATUS(Enum):
    INIT = auto()
    WORKING = auto()
    CONNECTION_ERROR = auto()
    ERROR = auto()
