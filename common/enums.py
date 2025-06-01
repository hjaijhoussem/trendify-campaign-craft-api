from enum import Enum, auto


class BaseEnum(Enum):
    pass


class StrEnum(str, BaseEnum):
    # noinspection PyMethodParameters
    def _generate_next_value_(name, start, count, last_values) -> str:  # type: ignore
        return name


class LogLevelEnum(StrEnum):
    """
    Log levels
    """

    CRITICAL = auto()
    FATAL = auto()
    ERROR = auto()
    WARNING = auto()
    WARN = auto()
    INFO = auto()
    DEBUG = auto()
    NOTSET = auto()