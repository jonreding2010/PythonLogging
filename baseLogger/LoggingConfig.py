import os
from baseLogger.ConsoleLogger import ConsoleLogger
from baseLogger.FileLogger import FileLogger
from baseLogger.constants.LoggingEnabled import LoggingEnabled
from baseLogger.constants.MessageType import MessageType
from utilities.Config import Config
from utilities.StringProcessor import StringProcessor


# Get logging config data.
class LoggingConfig(Config):

    def __init__(self):
        config = super()

    # Get our logging state - Yes, no or on failure.
    # @return The log enabled state
    # def get_logging_enabled_setting(config, default_value=None):
    def get_logging_enabled_setting(self, default_value=None):
        value = str(self.config.get_general_value("Log", default_value)).upper()
        if value == "YES":
            return LoggingEnabled.YES.name
        elif value == "ONFAIL":
            return LoggingEnabled.ONFAIL.name
        elif value == "NO":
            return LoggingEnabled.NO.name
        else:
            raise NotImplementedError(StringProcessor.safe_formatter("Log value {} is not a valid option",
                                                                     Config().get_general_value("Log", "NO")))

    # Get our logging level.
    # @return MessageType - The current log level.
    def get_logging_level_setting(self, default_value=None):
        value = str(self.config.get_general_value("LogLevel", default_value)).upper()

        if value == "VERBOSE":
            # Includes this and all of those below
            return MessageType.VERBOSE.name
        elif value == "INFORMATION":
            # Includes this and all of those below
            return MessageType.INFORMATION.name
        elif value == "GENERIC":
            # Includes this and all of those below
            return MessageType.GENERIC.name
        elif value == "SUCCESS":
            # Includes this and all of those below
            return MessageType.SUCCESS.name
        elif value == "WARNING":
            # Includes this and all of those below
            return MessageType.WARNING.name
        elif value == "ERROR":
            # Includes this and all of those below
            return MessageType.ERROR.name
        elif value == "SUSPENDED":
            # Includes this and all of those below
            return MessageType.SUSPENDED.name
        else:
            raise AttributeError(StringProcessor
                                 .safe_formatter("Logging level value '{}' is not a valid option",
                                                 Config().get_general_value("LogLevel")))

    # Get the baseLogger.
    # @param fileName File name to use for the log
    # @return The baseLogger
    def get_logger(self, file_name):
        # Disable logging means we just send any logged messages to the console
        if self.get_logging_enabled_setting(self.config) == LoggingEnabled.NO.name:
            return ConsoleLogger()

        log_directory = self.get_log_directory()
        logging_level = self.get_logging_level_setting(Config())

        # value = Config().get_general_value("LogType", "CONSOLE").upper()
        value = self.config.get_general_value("LogType").upper()
        if value == "CONSOLE":
            return ConsoleLogger(logging_level)
        elif value == "TXT":
            return FileLogger(log_directory, False, file_name, logging_level)
        else:
            raise AttributeError(StringProcessor.safe_formatter("Log type {} is not a valid option",
                                                                Config().get_general_value("LogType", "CONSOLE")))

    # Gets the File Directory to store log files.
    # @return String of file path
    def get_log_directory(self):
        path = os.path.abspath(os.getcwd()) + "\\Logs"
        return self.config.get_general_value("FileLoggerPath", path)
