import os
import os.path as path
import tempfile
import time
from baseLogger.ConsoleLogger import ConsoleLogger
from baseLogger.Logger import Logger
from baseLogger.constants.MessageType import MessageType
from utilities.StringProcessor import StringProcessor


# Helper class for adding logs to a plain text file. Allows configurable file path.
class FileLogger(Logger):
    # The default log file save location.
    DEFAULT_LOG_FOLDER = tempfile.gettempdir()

    # Initializes a new instance of the FileLogger class.
    DEFAULT_LOG_NAME = "FileLog.txt"

    # Creates a private string for the name of the file.
    fileName = str()

    # Create a private string for the path of the file.
    filePath = str()

    # Creates a private Message Type.
    messageType = None

    # Creates a private string for the directory of the folder.
    directory = str()

    # Initializes a new instance of the FileLogger class.
    # @ param append True to append to an existing log file or false to overwrite it.
    # If the file does not exist, this flag will have no affect.
    # @ param logFolder Where log files should be saved
    # @ param name File Name
    # @ param messageLevel Messaging Level
    def __init__(self, log_folder="", append=False, message_level=MessageType.INFORMATION,
                 log_name=DEFAULT_LOG_NAME):
        super().__init__(message_level)

        if log_folder is None or log_folder == "":
            self.directory = self.DEFAULT_LOG_FOLDER
        else:
            self.directory = log_folder

        if not os.path.exists(self.directory):
            os.makedirs(self.directory)

        name = self.make_valid_file_name(log_name)

        if not name.lower().endswith(self.extension()):
            name += self.extension()

        self.fileName = name
        self.filePath = self.directory
        self.messageType = message_level

        if path.exists(self.filePath) and not append:
            try:
                with open(self.filePath, "w") as writer:
                    # writer = open(self.filePath, "w")
                    writer.write(" ")
            except IOError as e:
                # Failed to write to the event log, write error to the console instead
                console = ConsoleLogger()
                console.log_message(MessageType.ERROR,
                                    StringProcessor.safe_formatter("Failed to write to event log because: {}",
                                                                   e.strerror + self.filePath))

    @staticmethod
    def extension():
        # Gets the file extension.
        return ".txt"

    # Gets the FilePath value.
    # @return returns the file path
    def get_file_path(self):
        return self.filePath

    # Gets the Message Type name.
    # @return The Message Type.
    def get_message_type(self):
        return self.messageType.name

    # Gets the Directory Path.
    # @return Returns the Directory
    def get_directory(self):
        return self.directory

    # Sets the FilePath value.
    # @param path sets the file path
    def set_file_path(self, new_path):
        self.filePath = new_path

    # Gets the File Name value.
    # @return Returns the File Name.
    def get_file_name(self):
        return self.fileName

    # Close the temp file
    # @param file the file name
    def close_temp_file(self, file):
        file.close()

    # @see com.magenic.jmaqs.utilities.Logging.Logger#logMessage(com.magenic.jmaqs.utilities.
    # Logging.MessageType, java.lang.String, java.lang.Object[])
    # @Override
    def log_message(self, message="", args=None, message_type=MessageType.INFORMATION):
        # If the message level is greater that the current log level then do not log it.
        if self.should_message_be_logged(message_type):
            try:
                with open(self.filePath, "w") as writer:
                    writer.write(StringProcessor.safe_formatter("{}{}", [os.linesep, int(round(time.time() * 1000))]))
                    writer.write(StringProcessor.safe_formatter("{}:\t", message_type))
                    writer.write(StringProcessor.safe_formatter(message, args))
            except IOError as e:
                # Failed to write to the event log, write error to the console instead
                console = ConsoleLogger()
                console.log_message(StringProcessor.safe_formatter("Failed to write to event log because: {}",
                                                                   e.strerror), args, MessageType.ERROR)
                console.log_message(message, args, message_type)

    # Take a name sting and make it a valid file name.
    # @param name The string to cleanup
    # @return returns the string of a valid filename
    @staticmethod
    def make_valid_file_name(new_name):
        if new_name is None or new_name == "":
            raise FileExistsError("Blank or null file name was provided")

        # Replace invalid characters
        replaced_name = new_name
        try:
            replaced_name = new_name.replace("[^a-zA-Z0-9\\._\\- ]+", "~")
        except Exception as e:
            console = ConsoleLogger()
            console.log_message(MessageType.ERROR, StringProcessor
                                .safe_formatter("Failed to Replace Invalid Characters because: {}", e.args))
        return replaced_name

    # Get the message for an unknown message type.
    # @param type The Message Type.
    # @return The Unknown Message Type Message.
    @staticmethod
    def unknown_message_type_message(new_type):
        args = [new_type, os.linesep, "Message will be displayed with the MessageType of: ", MessageType.GENERIC.Name]
        return StringProcessor.safe_formatter("Unknown MessageType: {}{}{}{}", args)
