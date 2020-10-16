from enum import Enum


# The type of message.
class LoggingEnabled(Enum):
    # Yes log.
    YES = "YES",

    # Only save a log when there is a failure.
    ONFAIL = "ONFAIL",

    # No, don't log.
    NO = "NO"
