from enum import Enum


# The type of message.
class MessageType(Enum):
    # Suspended message.
    SUSPENDED = -1,

    # Error message.
    ERROR = 0,

    # Warning message.
    WARNING = 1,

    # Success message.
    SUCCESS = 2,

    # Generic message.
    GENERIC = 3,

    # Informational message - Our default message type.
    INFORMATION = 4,

    # Verbose message.
    VERBOSE = 5

    @staticmethod
    def valueOf(message_type_text):
        message_type_text = message_type_text.upper()
        if message_type_text == MessageType.SUSPENDED.name:
            return MessageType.SUSPENDED
        elif message_type_text == MessageType.ERROR.name:
            return MessageType.ERROR
        elif message_type_text == MessageType.WARNING.name:
            return MessageType.WARNING
        elif message_type_text == MessageType.SUCCESS.name:
            return MessageType.SUCCESS
        elif message_type_text == MessageType.GENERIC.name:
            return MessageType.SUCCESS
        elif message_type_text == MessageType.GENERIC.name:
            return MessageType.GENERIC
        elif message_type_text == MessageType.INFORMATION.name:
            return MessageType.INFORMATION
        elif message_type_text == MessageType.VERBOSE.name:
            return MessageType.VERBOSE
        else:
            raise NotImplementedError("Message type is not supported")
