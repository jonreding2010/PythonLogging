from baseLogger.Logger import Logger
from baseLogger.constants.MessageType import MessageType
from utilities.StringProcessor import StringProcessor


# Helper class for logging to the console.
class ConsoleLogger(Logger):
    # Initializes a new instance of the ConsoleLogger class.
    # @param level The logging level.
    def __init__(self, level=MessageType.INFORMATION):
        super().__init__(level)

    # Write the formatted message (one line) to the console as the specified type.
    # @param messageType The type of message
    # @param message The message text
    # @param args String format arguments
    # @Override
    def log_message(self, message="", args=None, message_type=MessageType.INFORMATION):
        self.write_line(message, args, message_type)

    # Write the formatted message to the console as the given message type.
    # @param type The type of message
    # @param message The message text
    # @param args Message string format arguments
    def write(self, message, args, message_type=MessageType.INFORMATION):
        self.write_to_console(False, message, args, message_type)

    # Write the formatted message followed by a line break to the console as the given message type.
    # @param type the type of message
    # @param message The message text
    # @param args Message string format arguments
    def write_line(self, message, args, message_type=MessageType.INFORMATION):
        self.write_to_console(True, message, args, message_type)

    # write the message to the console.
    # @param type The type of message
    # @param line Is this a write-line command, else it is just a write
    # @param message The log message
    # @param args Message string format arguments
    def write_to_console(self, line, message, args, message_type):
        # Just return if there is no message
        if message is None or not self.should_message_be_logged(message_type):
            return

        result = StringProcessor.safe_formatter(message, args)
        try:
            # If this a write-line command
            if line:
                print(result)
            else:
                print(result)
        except Exception as e:
            print(StringProcessor.safe_formatter(
                "Failed to write to the console because: {}", e.args))
