
# Abstract logging interface base class.
from baseLogger.constants.MessageType import MessageType


class Logger:
    # Default date format.
    DEFAULT_DATE_FORMAT = "yyyy-MM-dd HH:mm:ss"

    # Log Level value area.
    log_level = MessageType.INFORMATION.name

    # Log Level value save area.
    log_level_saved = MessageType.SUSPENDED.value

    # Initializes a new instance of the Logger class.
    def __init__(self, level=MessageType.INFORMATION):
        self.log_level = level

    # Set the logging level.
    # @param level The logging level.
    def set_logging_level(self, level):
        self.log_level = level

    # Suspends logging.
    def suspend_logging(self):
        if self.log_level is not MessageType.SUSPENDED.value:
            self.log_level_saved = self.log_level
            self.log_level = MessageType.SUSPENDED
            self.log_message("Suspending Logging..", None, MessageType.VERBOSE)

    # Continue logging after it was suspended.
    def continue_logging(self):
        # Check if the logging was suspended
        if self.log_level_saved is not MessageType.SUSPENDED.value:
            # Return to the log level at the suspension of logging
            self.log_level = self.log_level_saved

        self.log_level_saved = MessageType.SUSPENDED.value
        self.log_message(MessageType.VERBOSE.value, "Logging Continued..")

    # Write the formatted message (one line) to the console as a generic message.
    # @param message Type The type of message
    # @param message The message text
    # @param args String format arguments
    def log_message(self, message="", args=None, message_type=MessageType.INFORMATION):
        print("")

    # Determine if the message should be logged.
    # The message should be logged if it's level is greater than or equal to the current logging level.
    # @param messageType The type of message being logged.
    # @return True if the message should be logged.
    def should_message_be_logged(self, message_type):
        # The message should be logged if it's level is less than or equal to the current logging level
        return message_type.value[0] <= self.log_level.value[0]
