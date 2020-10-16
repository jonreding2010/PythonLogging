import os
import uuid
from os import path
import tempfile
import unittest
import time
from baseLogger.ConsoleLogger import ConsoleLogger
from baseLogger.FileLogger import FileLogger
from baseLogger.HtmlFileLogger import HtmlFileLogger
from baseLogger.LoggingConfig import LoggingConfig
from baseLogger.constants.MessageType import MessageType
from utilities.StringProcessor import StringProcessor


# Unit test class for FileLogger.java
# @Test(singleThreaded = true)
class FileLoggerUnitTest(unittest.TestCase):
    LOG_FOLDER_MESSAGING_LEVEL_DIRECTORY = LoggingConfig().get_log_directory() + "/" + \
                                           "Log Folder Messaging Level Directory"
    Test_Message = "Test to ensure LogMessage works as expected."

    # @DataProvider(name = "log_levels")
    @staticmethod
    def data():
        return [["VERBOSE",
                 [["VERBOSE", True], ["INFORMATION", True], ["GENERIC", True], ["SUCCESS", True], ["WARNING", True],
                  ["ERROR", True]]],
                ["INFORMATION",
                 [["VERBOSE", False], ["INFORMATION", True], ["GENERIC", True], ["SUCCESS", True], ["WARNING", True],
                  ["ERROR", True]]],
                ["GENERIC",
                 [["VERBOSE", False], ["INFORMATION", False], ["GENERIC", True], ["SUCCESS", True], ["WARNING", True],
                  ["ERROR", True]]],
                ["SUCCESS",
                 [["VERBOSE", False], ["INFORMATION", False], ["GENERIC", False], ["SUCCESS", True], ["WARNING", True],
                  ["ERROR", True]]],
                ["WARNING",
                 [["VERBOSE", False], ["INFORMATION", False], ["GENERIC", False], ["SUCCESS", False], ["WARNING", True],
                  ["ERROR", True]]],
                ["ERROR", [["VERBOSE", False], ["INFORMATION", False], ["GENERIC", False], ["SUCCESS", False],
                           ["WARNING", False], ["ERROR", True]]],
                ["SUSPENDED", [["VERBOSE", False], ["INFORMATION", False], ["GENERIC", False], ["SUCCESS", False],
                               ["WARNING", False], ["ERROR", False]]]]

    single_data = ["VERBOSE", [["VERBOSE", True], ["INFORMATION", True], ["GENERIC", True], ["SUCCESS", True],
                               ["WARNING", True], ["ERROR", True]]]

    # Verify the text file baseLogger respects hierarchical logging
    # @param logLevel The type of logging.
    # @param levels What should appear for each level.
    # @Test(dataProvider = "logLevels")
    def test_HierarchicalTxtFileLogger(self):
        log_level, levels = self.single_data
        file_logger = FileLogger(LoggingConfig().get_log_directory(), True,
                                 self.get_file_name(self._testMethodName + log_level, "txt"),
                                 MessageType.GENERIC)
        self.hierarchical_logging(file_logger, file_logger.get_file_path(), log_level, levels)
        os.remove(file_logger.get_file_path())
        self.assertTrue(path.exists(file_logger.get_file_path()))

    # Verify the console baseLogger respects hierarchical logging
    # @param logLevel The type of logging.
    # @param levels What should appear for each level.
    # @Test(dataProvider = "logLevels")
    def test_HierarchicalConsoleLogger(self):
        log_level, levels = self.data()
        # Calculate a file path
        file_path = LoggingConfig().get_log_directory() + \
                    self.get_file_name(self._testMethodName + log_level, "txt")
        try:
            open(file_path).read()
            console_logger = ConsoleLogger()
            self.hierarchical_logging(console_logger, file_path, log_level, levels)
        except Exception as e:
            raise FileExistsError()
        os.remove(file_path)
        self.assertTrue(path.exists(file_path))

    # Verify the Html File baseLogger respects hierarchical logging
    # @param logLevel The type of logging.
    # @param levels What should appear for each level.
    # @Test(dataProvider = "logLevels")
    # def test_HierarchicalHtmlFileLogger(self, log_level, levels):
    def test_HierarchicalHtmlFileLogger(self):
        log_level, levels = self.data()
        html_logger = HtmlFileLogger(True, LoggingConfig().get_log_directory(),
                                     self.get_file_name(self._testMethodName + log_level, "html"),
                                     MessageType.GENERIC.value)
        self.hierarchical_logging(html_logger, html_logger.get_file_path(), log_level, levels)
        os.remove(html_logger.get_file_path())
        self.assertTrue(path.exists(html_logger.get_file_path()))

    # Test logging to a new file.
    def test_fileLoggerNoAppendTest(self):
        file_logger = FileLogger(False, "", "WriteToFileLogger")
        file_logger.log_message(MessageType.WARNING, "Hello, this is a test.")
        os.remove(file_logger.get_file_path())
        self.assertTrue(path.exists(file_logger.get_file_path()))

    # Test logging to an existing file.
    def test_fileLoggerAppendFileTest(self):
        file_logger = FileLogger("", True, MessageType.INFORMATION , "WriteToExistingFileLogger")
        file_logger.log_message("This is a test to write to an existing file.", None, MessageType.WARNING)
        # os.remove(file_logger.get_file_path())
        self.assertTrue(path.exists(file_logger.get_file_path()))

    # Verify the logging suspension functions
    def Test_SuspendLogger(self):
        # Start logging
        file_logger = FileLogger(True, LoggingConfig().get_log_directory(),
                                 self.get_file_name("TestHierarchicalTxtFileLogger", "txt"), MessageType.GENERIC.value)
        file_logger.set_logging_level(MessageType.VERBOSE)
        file_logger.log_message(MessageType.VERBOSE, "HellO")

        # Suspend logging
        file_logger.suspend_logging()
        file_logger.log_message(MessageType.ERROR, "GoodByE")

        # Continue logging
        file_logger.continue_logging()
        file_logger.log_message(MessageType.VERBOSE, "BacK")

        # Get the log file content
        log_contents = self.read_text_file(file_logger.get_file_path())

        # Verify that logging was active
        hello_found = "HellO" in log_contents
        self.assertTrue(hello_found, "'HellO' was not found.  Logging Failed")

        # Verify that logging was suspended
        goodbye_found = "GoodByE" in log_contents
        self.assertFalse(goodbye_found, "'GoodByE' was found when it should not be written.  Logging Failed")

        # Verify that logging was active
        back_found = "BacK" in log_contents
        self.assertTrue(back_found, "'BacK' was not found.  Logging Failed")

        os.remove(file_logger.get_file_path())
        self.assertTrue(path.exists(file_logger.get_file_path()))

    # Test Writing to the File Logger
    def test_WriteToFileLogger(self):
        file_logger = FileLogger("", False, "WriteToFileLogger")
        file_logger.log_message(MessageType.WARNING.value, "Hello, this is a test.")
        os.remove(file_logger.get_file_path())
        self.assertTrue(path.exists(file_logger.get_file_path()))

    # Test Writing to an Existing File Logger
    def test_WriteToExistingFileLogger(self):
        file_logger = FileLogger("", True, "WriteToExistingFileLogger", MessageType.GENERIC)
        file_logger.log_message("This is a test.", None, MessageType.WARNING)
        file_logger.log_message(MessageType.WARNING, "This is a test to write to an existing file.")
        os.remove(file_logger.get_file_path())
        self.assertTrue(path.exists(file_logger.get_file_path()))

    # Verify FileLogger constructor creates the correct directory if it does not
    # already exist. Delete Directory after each run.
    def test_FileLoggerConstructorCreateDirectory(self):
        message = "Test to ensure that the file in the created directory can be written to."
        file_logger = FileLogger(LoggingConfig().get_log_directory(), True,
                                 "FileLoggerCreateDirectoryDelete", MessageType.GENERIC)
        file_logger.log_message(MessageType.WARNING.value,
                                "Test to ensure that the file in the created directory can be written to.")
        file = file_logger.get_file_path()
        actual_message = self.read_text_file(file.getCanonicalPath())
        self.assertTrue(message in actual_message, "Expected '" + message + "' but got '"
                        + actual_message + "' for: " + file.getCanonicalPath())
        os.remove(file)
        self.assertTrue(path.exists(file_logger.get_file_path()))

    # Verify that File Logger can log message without defining a Message Type
    def test_FileLoggerLogMessage(self):
        file_logger = FileLogger("", True, "FileLoggerLogMessage")
        file_logger.log_message("Test to ensure LogMessage works as expected.")
        self.assertTrue(self.Test_Message in self.read_text_file(file_logger.get_file_path()),
                        "Expected Log Message to be contained in log.")
        os.remove(file_logger.get_file_path())
        self.assertTrue(path.exists(file_logger.get_file_path()))

    # Verify that File Logger can log message and defining a Message Type
    def test_FileLoggerLogMessageSelectType(self):
        file_logger = FileLogger("", True, "FileLoggerLogMessage")
        file_logger.log_message(MessageType.GENERIC, "Test to ensure LogMessage works as expected.")
        self.assertTrue(self.Test_Message in self.read_text_file(file_logger.get_file_path()),
                        "Expected Log Message to be contained in log.")
        os.remove(file_logger.get_file_path())
        self.assertTrue(path.exists(file_logger.get_file_path()))

    # Verify that File Path field can be accessed and updated
    def test_FileLoggerSetFilePath(self):
        file_logger = FileLogger("", True, "FileLoggerSetFilePath", MessageType.GENERIC)
        file_logger.set_file_path("test file path")
        self.assertEquals(file_logger.get_file_path(), "test file path")
        self.assertFalse(path.exists(file_logger.get_file_path()))

    # Verify that File Logger catches and handles errors caused by incorrect file Paths
    def test_FileLoggerCatchThrownException(self):
        file_logger = FileLogger("", True, "FileLoggerCatchThrownException", MessageType.GENERIC)
        file_logger.set_file_path("<>")
        file_logger.log_message(MessageType.GENERIC, "test throws error")
        os.remove(file_logger.get_file_path())
        self.assertTrue(path.exists(file_logger.get_file_path()))

    # Test File Logger with empty file name throws Illegal Argument Exception.
    # @Test(expectedExceptions = IllegalArgumentException.class)
    def test_FileLoggerEmptyFileNameException(self):
        with self.assertRaises(AttributeError):
            logger = FileLogger("")
            self.assertTrue(logger is None)

    # Verify File Logger with No Parameters assigns the correct default values.
    def test_FileLoggerNoParameters(self):
        file_logger = FileLogger("")
        self.assertEquals(tempfile.TemporaryFile(), file_logger.get_directory(),
                          StringProcessor.safe_formatter("Expected Directory '{}'.", file_logger.DEFAULT_LOG_FOLDER))
        self.assertEquals("FileLog.txt", file_logger.get_file_name(), "Expected correct File Name.")
        self.assertEquals(MessageType.INFORMATION, file_logger.get_message_type(),
                          "Expected Information Message Type.")
        os.remove(file_logger.get_file_path())
        self.assertTrue(path.exists(file_logger.get_file_path()))

    # Verify File Logger with only append parameter assigns the correct default values.
    def test_FileLoggerAppendOnly(self):
        file_logger = FileLogger("", True)
        self.assertEquals(file_logger.DEFAULT_LOG_FOLDER, file_logger.get_directory(),
                          StringProcessor.safe_formatter("Expected Directory '{}'.", file_logger.DEFAULT_LOG_FOLDER))
        self.assertEquals("FileLog.txt", file_logger.get_file_name(), "Expected correct File Name.")
        self.assertEquals(MessageType.INFORMATION.name, file_logger.get_message_type(),
                          "Expected Information Message Type.")

        # os.remove(file_logger.get_file_path() + file_logger.get_file_name())
        self.assertFalse(path.exists(os.path.abspath(file_logger.get_file_path())))

    # Verify File Logger with only File Name parameter assigns the correct default values.
    # Verify default extension is added '.txt'
    def test_FileLoggerNameOnlyAddExtension(self):
        file_logger = FileLogger("FileNameOnly")
        self.assertEquals(tempfile.TemporaryFile(), file_logger.get_directory(),
                          StringProcessor.safe_formatter("Expected Directory '{}'.", file_logger.DEFAULT_LOG_FOLDER))
        self.assertEquals("FileNameOnly.txt", file_logger.get_file_name(), "Expected correct File Name.")
        self.assertEquals(MessageType.INFORMATION.value, file_logger.get_message_type(),
                          "Expected Information Message Type.")

        os.remove(file_logger.get_file_path())
        self.assertTrue(path.exists(file_logger.get_file_path()))

    # Verify File Logger with only Message Type parameter assigns the correct default values.
    def test_FileLoggerMessageTypeOnly(self):
        file_logger = FileLogger(MessageType.WARNING)
        self.assertEquals(tempfile.TemporaryFile(), file_logger.get_directory(),
                          StringProcessor.safe_formatter("Expected Directory '{}'.", file_logger.DEFAULT_LOG_FOLDER))
        self.assertEquals("FileLog.txt", file_logger.get_file_name(), "Expected correct File Name.")
        self.assertEquals(MessageType.WARNING.name, file_logger.get_message_type(),
                          "Expected Warning Message Type.")

        os.remove(file_logger.get_file_path())
        self.assertTrue(path.exists(file_logger.get_file_path()))

    # Verify File Logger with only Append and File Name parameters assigns the correct default values.
    def test_FileLoggerAppendFileName(self):
        file_logger = FileLogger("", True, "AppendFileName")
        self.assertEquals(tempfile.TemporaryFile(), file_logger.get_directory(),
                          StringProcessor.safe_formatter("Expected Directory '{}'.", file_logger.DEFAULT_LOG_FOLDER))
        self.assertEquals("AppendFileName.txt", file_logger.get_file_name(), "Expected correct File Name.")
        self.assertEquals(MessageType.INFORMATION.name, file_logger.get_message_type(),
                          "Expected Information Message Type.")

        os.remove(file_logger.get_file_path())
        self.assertTrue(path.exists(file_logger.get_file_path()))

    # Verify File Logger with only Log Folder and Append parameters assigns the correct default values.
    def test_FileLoggerAppendLogFolder(self):
        append_file_directory = LoggingConfig().get_log_directory() + "/" + "Append File Directory"
        file_logger = FileLogger(append_file_directory, True)
        self.assertEquals(append_file_directory, file_logger.get_directory(),
                          "Expected Directory 'Append File Directory'.")
        self.assertEquals("FileLog.txt", file_logger.get_file_name(), "Expected correct File Name.")
        self.assertEquals(MessageType.INFORMATION.name, file_logger.get_message_type(),
                          "Expected Information Message Type.")

        os.remove(file_logger.get_file_path())
        self.assertTrue(path.exists(file_logger.get_file_path()))

    # Verify File Logger with only Log Folder and File Name parameters assigns the correct default values.
    def test_FileLoggerLogFolderFileName(self):
        log_folder_file_name_directory = LoggingConfig().get_log_directory() + "/" + "Log Folder File Name Directory"
        file_logger = FileLogger(log_folder_file_name_directory, "LogFolderFileName.txt")

        self.assertEquals(log_folder_file_name_directory, file_logger.get_directory(),
                          "Expected Directory 'Log Folder File Name Directory'.")
        self.assertEquals("LogFolderFileName.txt", file_logger.get_file_name(), "Expected correct File Name.")
        self.assertEquals(MessageType.INFORMATION, file_logger.get_message_type(),
                          "Expected Information Message Type.")

        os.remove(file_logger.get_file_path())
        self.assertTrue(path.exists(file_logger.get_file_path()))

    # Verify File Logger with only Log Folder and Messaging Level parameters assigns the correct default values.
    def test_FileLoggerLogFolderMessagingLevel(self):
        file_logger = FileLogger(self.LOG_FOLDER_MESSAGING_LEVEL_DIRECTORY, MessageType.WARNING)
        self.assertEquals(self.LOG_FOLDER_MESSAGING_LEVEL_DIRECTORY, file_logger.get_directory(),
                          "Expected Directory 'Log Folder Messaging Level Directory'.")
        self.assertEquals("FileLog.txt", file_logger.get_file_name(), "Expected correct File Name.")
        self.assertEquals(MessageType.WARNING.value, file_logger.get_message_type(),
                          "Expected Warning Message Type.")

        os.remove(file_logger.get_file_path())
        self.assertTrue(path.exists(file_logger.get_file_path()))

    # Verify File Logger with only Append and Messaging Level parameters assigns the correct default values.
    def test_FileLoggerAppendMessagingLevel(self):
        file_logger = FileLogger(True, MessageType.WARNING.value)
        self.assertEquals(tempfile.TemporaryFile(), file_logger.get_directory(),
                          StringProcessor.safe_formatter("Expected Directory '{}'.", file_logger.DEFAULT_LOG_FOLDER))
        self.assertEquals("FileLog.txt", file_logger.get_file_name(), "Expected correct File Name.")
        self.assertEquals(MessageType.WARNING.value, file_logger.get_message_type(),
                          "Expected Warning Message Type.")

        os.remove(file_logger.get_file_path())
        self.assertTrue(path.exists(file_logger.get_file_path()))

    # Verify File Logger with only Messaging Level and file name parameters assigns the correct default values.
    def test_FileLoggerMessagingLevelFileName(self):
        file_logger = FileLogger("MessagingTypeFile.txt", None, MessageType.WARNING.value)
        self.assertEquals(tempfile.TemporaryFile(), file_logger.get_directory(),
                          StringProcessor.safe_formatter("Expected Directory '{}'.", file_logger.DEFAULT_LOG_FOLDER))
        self.assertEquals("MessagingTypeFile.txt", file_logger.get_file_name(), "Expected correct File Name.")
        self.assertEquals(MessageType.WARNING.name, file_logger.get_message_type(),
                          "Expected Warning Message Type.")

        os.remove(file_logger.get_file_path())
        self.assertTrue(path.exists(file_logger.get_file_path()))

    # Verify File Logger with only Append, log folder and file name parameters assigns the correct default values.
    def test_FileLoggerAppendLogFolderFileName(self):
        append_log_folder_file_name_directory = LoggingConfig().get_log_directory() + "/" + \
                                                "AppendLogFolderFileNameDirectory"
        file_logger = FileLogger(True, append_log_folder_file_name_directory, "AppendLogFolderFileName.txt")

        self.assertEquals(append_log_folder_file_name_directory, file_logger.get_directory(),
                          " Expected Directory AppendLogFolderFileNameDirectory")
        self.assertEquals("AppendLogFolderFileName.txt", file_logger.get_file_name(),
                          "Expected correct File Name.")
        self.assertEquals(MessageType.INFORMATION.name, file_logger.get_message_type(),
                          "Expected Information Message Type.")

        os.remove(file_logger.get_file_path())
        self.assertTrue(path.exists(file_logger.get_file_path()))

    # Verify File Logger with only Append, log folder and Messaging Level parameters assigns the correct default values.
    # @Test
    def test_FileLoggerAppendLogFolderMessagingLevel(self):
        append_log_folder_file_name_directory = LoggingConfig().get_log_directory() + "/" + \
                                                "AppendLogFolderFileNameDirectory "
        file_logger = FileLogger(True, append_log_folder_file_name_directory, MessageType.WARNING)

        self.assertEquals(append_log_folder_file_name_directory, file_logger.get_directory(),
                          " Expected Directory AppendLogFolderFileNameDirectory")
        self.assertEquals("FileLog.txt", file_logger.get_file_name(), "Expected correct File Name.")
        self.assertEquals(MessageType.WARNING.name, file_logger.get_message_type(),
                          "Expected Warning Message Type.")

        os.remove(file_logger.get_file_path())
        self.assertTrue(path.exists(file_logger.get_file_path()))

    # Verify File Logger with only File Name, Append and Messaging Level parameters assigns the correct default values.
    def test_FileLoggerFileNameAppendMessagingLevel(self):
        file_logger = FileLogger("FileNameAppendMessagingLevel.txt", True, MessageType.WARNING)
        self.assertEquals(tempfile.TemporaryFile(), file_logger.get_directory(),
                          StringProcessor.safe_formatter("Expected Directory '{}'.", file_logger.DEFAULT_LOG_FOLDER))
        self.assertEquals("FileNameAppendMessagingLevel.txt", file_logger.get_file_name(),
                          "Expected correct File Name.")
        self.assertEquals(MessageType.WARNING, file_logger.get_message_type(),
                          "Expected Warning Message Type.")

        os.remove(file_logger.get_file_path())
        self.assertTrue(path.exists(file_logger.get_file_path()))

    # Verify File Logger with only Log Folder, File Name and Messaging Level 
    # parameters assigns the correct default values.
    def test_FileLoggerLogFolderFileNameMessagingLevel(self):
        log_folder_file_name_messaging_level_directory = LoggingConfig().get_log_directory() + "/" + \
                                                         "LogFolderFileNameMessagingLevelDirectory"
        file_logger = FileLogger(log_folder_file_name_messaging_level_directory,
                                 "LogFolderFileNameMessagingLevel.txt", MessageType.WARNING)
        self.assertEquals(log_folder_file_name_messaging_level_directory, file_logger.get_directory(),
                          "Expected Directory 'LogFolderFileNameMessagingLevelDirectory'")
        self.assertEquals("LogFolderFileNameMessagingLevel.txt", file_logger.get_file_name(),
                          "Expected correct File Name.")
        self.assertEquals(MessageType.WARNING.name, file_logger.get_message_type(), "Expected Warning Message Type.")

        os.remove(file_logger.get_file_path())
        self.assertTrue(path.exists(file_logger.get_file_path()))

    # Verify hierarchical logging is respected
    # @param baseLogger The baseLogger we are checking
    # @param filePath Where the log output can be found
    # @param logLevelText The type of logging
    # @param levels What should appear for each level
    def hierarchical_logging(self, logger, file_path, log_level_text, levels):
        # Get the log level
        log_level = MessageType.valueOf(log_level_text)
        logger.set_logging_level(log_level)

        # Set the baseLogger options to set the log level and add log entries to the file
        logger.log_message(log_level, "\nThe Log level is set to " + log_level.name)

        # Message template
        log_line = "Test Log item {}"

        # Log the test messages
        logger.log_message(MessageType.VERBOSE, log_line, MessageType.VERBOSE)
        logger.log_message(MessageType.INFORMATION.name, log_line, MessageType.INFORMATION)
        logger.log_message(MessageType.GENERIC.name, log_line, MessageType.GENERIC)
        logger.log_message(MessageType.SUCCESS.name, log_line, MessageType.SUCCESS)
        logger.log_message(MessageType.WARNING.name, log_line, MessageType.WARNING)
        logger.log_message(MessageType.ERROR.name, log_line, MessageType.ERROR)

        # Give the write time
        try:
            time.sleep(.25)
        except InterruptedError as e:
            e.args

        # Get the file content
        log_contents = self.read_text_file(file_path)

        # Verify that only the logged messages at the log level or below are logged
        for level in levels:
            if level.getKey() is not "Row" and level.getKey() is not "LogLevel":
                # Verify if the Message Type is found
                log_message_found = log_contents in ''.format(log_line + level.getKey())
                self.assertEquals(str(log_message_found), level.getValue().toString(),
                                  "Looking for '" + ''.format(log_line, level.getKey())
                                  + "' with Logger of type '" + log_level.name()
                                  + "'. \nLog Contents: " + log_contents)
        # Set the log level so that the soft asserts log
        logger.set_logging_level(MessageType.VERBOSE.name)
        # Fail test if any soft asserts failed
        self.assertEqual(logger.log_level, MessageType.VERBOSE.name)

    # Read a file and return it as a string
    # @param filePath The file path to read
    # @return The contents of the file
    @staticmethod
    def read_text_file(file_path):
        text = ""
        try:
            text = open(file_path).read()
        except Exception as e:
            # TODO: Print stacktrace
            e.printStackTrace()
        return text

    # Get a unique file name
    # @param testName Prepend text
    # @param extension The file extension
    # @return A unique file name
    @staticmethod
    def get_file_name(test_name, extension):
        # UUID4 is the random equivalent method
        return StringProcessor.safe_formatter("UtilitiesUnitTesting.{}{}{}", [test_name, str(uuid.uuid4()), extension])
