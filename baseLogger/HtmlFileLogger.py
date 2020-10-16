import os
from datetime import datetime
from baseLogger.ConsoleLogger import ConsoleLogger
from baseLogger.FileLogger import FileLogger
from baseLogger.Logger import Logger
from baseLogger.constants.MessageType import MessageType
from utilities.StringProcessor import StringProcessor


# Helper class for adding logs to an HTML file. Allows configurable file path.
class HtmlFileLogger(FileLogger):
    # The default log name.
    DEFAULT_LOG_NAME = "FileLog.html"

    # Default header for the HTML file, this gives us our colored text.
    DEFAULT_HTML_HEADER = "<!DOCTYPE html><html><header><title>Test Log</title></header><body>"
    LOG_ERROR_MESSAGE = "Failed to write to event log because: {}"

    # Initializes a new instance of the HtmlFileLogger class.
    # @param append       True to append to an existing log file or false to overwrite it.
    #                     If the file does not exist this, flag will have no affect.
    # @param logFolder    Where log files should be saved
    # @param name         File Name
    # @param messageLevel Messaging Level
    def __init__(self, log_folder="", append=False, message_level=MessageType.INFORMATION,
                 log_name=DEFAULT_LOG_NAME):
        super().__init__(log_folder, append, message_level, log_name)

        try:
            writer = open(super().get_file_path(), "w")
            writer.write(self.DEFAULT_HTML_HEADER)
        except IOError as e:
            console = ConsoleLogger()
            console.log_message(MessageType.ERROR,
                                StringProcessor.safe_formatter(self.LOG_ERROR_MESSAGE, e.args))

    # @see com.magenic.jmaqs.utilities.Logging.Logger#logMessage(com.magenic.jmaqs.utilities.
    # Logging.MessageType, java.lang.String, java.lang.Object[])
    # @Override
    def log_message(self, message="", args=None, message_type=MessageType.INFORMATION):
        super(FileLogger, self).log_message(message, args, message_type)
        # If the message level is greater that the current log level then do not log it.
        if super(FileLogger, self).should_message_be_logged(message_type):
            # Log the message
            try:
                writer = open(super().get_file_path(), "w")
                date_object = datetime.now()
                date_format = date_object.strftime(Logger.DEFAULT_DATE_FORMAT)
                date = date_format.format(date_object)

                # Set the style
                writer.write(self.get_text_with_color_flag(message_type))

                # Add the content
                writer.write(StringProcessor.safe_formatter("{}{}", [os.linesep, date]))
                writer.write(StringProcessor.safe_formatter("{}:\t", message_type.name()))
                writer.write(StringProcessor.safe_formatter(os.linesep + message, args))

                # Close off the style
                writer.write("</p>")

                # Close the pre tag when logging Errors
                if message_type is "ERROR":
                    writer.write("</pre>")
            except Exception as e:
                # Failed to write to the event log, write error to the console instead
                console_logger = ConsoleLogger()
                console_logger.log_message(MessageType.ERROR,
                                           StringProcessor.safe_formatter(self.LOG_ERROR_MESSAGE, e.args))
                console_logger.log_message(message_type, message, args)

    # Gets the file extension.
    @staticmethod
    def extension():
        return ".html"

    #  Close the class and HTML file.
    def close(self):
        if os.path.exists(self.get_file_path()):
            try:
                writer = open(self.get_file_path(), "w")
                writer.write("</body></html>")
            except IOError as e:
                console_logger = ConsoleLogger()
                console_logger.log_message(MessageType.ERROR,
                                           StringProcessor.safe_formatter(self.LOG_ERROR_MESSAGE, e.getMessage()))

    # Get the HTML style key for the given message type.
    # @param type The message type
    # @return String - The HTML style key for the given message type
    def get_text_with_color_flag(self, message_type):
        if message_type is MessageType.VERBOSE.value:
            return "<p style =\"color:purple\">"
        elif message_type is MessageType.ERROR.value:
            return "<pre><p style=\"color:red\">"
        elif message_type is MessageType.GENERIC.value:
            return "<p style =\"color:black\">"
        elif message_type is MessageType.INFORMATION.value:
            return "<p style =\"color:blue\">"
        elif message_type is MessageType.SUCCESS.value:
            return "<p style=\"color:green\">"
        elif message_type is MessageType.WARNING.value:
            return "<p style=\"color:orange\">"
        else:
            print(self.unknown_message_type_message(message_type))
            return "<p style=\"color:hotpink\">"
