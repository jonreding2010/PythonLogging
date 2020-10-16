import os
from os import path
from baseLogger.HtmlFileLogger import HtmlFileLogger
from baseLogger.LoggingConfig import LoggingConfig
from baseLogger.constants.MessageType import MessageType
import unittest
from utilities.StringProcessor import StringProcessor


# Unit test class for HtmlFileLogger
class HtmlFileLoggerUnitTest(unittest.TestCase):
    Test_Message = "Test to ensure that the file in the created directory can be written to."
    Log_Message = "Test to ensure LogMessage works as expected."

    # Test logging to a new file.
    def test_HtmlFileLoggerNoAppendTest(self):
        html_logger = HtmlFileLogger("", False, MessageType.INFORMATION, "WriteToHtmlFileLogger")
        html_logger.log_message(MessageType.WARNING, "Hello, this is a test.")

        file_path = html_logger.get_file_path() + "\\" + html_logger.get_file_name()
        self.assertTrue(path.exists(file_path))

    # Test logging to an existing file.
    def test_HtmlFileLoggerAppendFileTest(self):
        html_logger = HtmlFileLogger("", True, "WriteToExistingHtmlFileLogger")
        html_logger.log_message(MessageType.WARNING, "This is a test to write to an existing file.")
        html_logger.log_message(MessageType.WARNING, "This is a test to append to current file.")

        file_path = html_logger.get_file_path() + "\\" + html_logger.get_file_name()
        self.assertTrue(path.exists(file_path))

    # Test Writing to the Html File Logger
    def test_WriteToHtmlFileLogger(self):
        html_logger = HtmlFileLogger("", False, MessageType.INFORMATION, "WriteToHtmlFileLogger")
        html_logger.log_message("Hello, this is a test.", "", MessageType.WARNING)

        file_path = html_logger.get_file_path() + "\\" + html_logger.get_file_name()
        self.assertTrue(path.exists(file_path))

    # Test Writing to an Existing Html File Logger
    def test_WriteToExistingHtmlFileLogger(self):
        html_logger = HtmlFileLogger("", True, MessageType.GENERIC, "WriteToExistingHtmlFileLogger")
        html_logger.log_message(MessageType.WARNING, "This is a test.")
        html_logger.log_message(MessageType.WARNING, "This is a test to write to an existing file.")

        file_path = html_logger.get_file_path() + "\\" + html_logger.get_file_name()
        self.assertFalse(path.exists(file_path))

    # Verify HtmlFileLogger constructor creates the correct directory if it does not already exist.
    # Delete Directory after each run.
    def test_HtmlFileLoggerConstructorCreateDirectory(self):
        html_logger = HtmlFileLogger(True, LoggingConfig().get_log_directory(),
                                     "HtmlFileLoggerCreateDirectory", MessageType.GENERIC)
        html_logger.log_message(MessageType.WARNING,
                                "Test to ensure that the file in the created directory can be written to.")
        file = html_logger.get_file_path()
        self.assertTrue(self.readTextFile(self.Test_Message in html_logger.get_file_path()))
        file.delete()
        self.assertTrue(path.exists(html_logger.get_file_path()))
        file = html_logger.get_directory()

        try:
            os.remove(file)
        except IOError as e:
            e.printStackTrace()

    # Verify that HtmlFileLogger can log message without defining a Message Type
    def test_HtmlFileLoggerLogMessage(self):
        html_logger = HtmlFileLogger("", True, MessageType.INFORMATION, "HtmlFileLoggerLogMessage")
        html_logger.log_message("Test to ensure LogMessage works as expected.")
        html_text = self.readTextFile(html_logger.get_file_path())
        # os.remove(html_logger.get_file_path())
        self.assertFalse(path.exists(html_logger.get_file_path()))
        self.assertTrue(self.Log_Message in html_text, "Expected Log Message to be contained in log.")

    # Verify that HTML File Logger can log message and defining a Message Type.
    def test_HtmlFileLoggerLogMessageSelectType(self):
        html_logger = HtmlFileLogger("", True, MessageType.INFORMATION, "HtmlFileLoggerLogMessageType")
        html_logger.log_message("Test to ensure LogMessage works as expected.", None, MessageType.GENERIC)
        html_text = self.readTextFile(html_logger.get_file_path())
        # os.remove(html_logger.get_file_path())
        self.assertFalse(path.exists(html_logger.get_file_path()))
        self.assertTrue(self.Test_Message in html_text, "Expected Log Message to be contained in log.")

    # Verify that File Path field can be accessed and updated
    def test_HtmlFileLoggerSetFilePath(self):
        html_logger = HtmlFileLogger("", True, MessageType.GENERIC, "HtmlFileLoggerSetFilePath")
        html_logger.set_file_path("test file path")
        file_path = html_logger.get_file_path()
        # os.remove(html_logger.get_file_path())
        self.assertFalse(path.exists(html_logger.get_file_path()))
        self.assertEquals(file_path, "test file path", "Expected 'test file path' as file path")

    # Verify that HTML File Logger catches and handles errors caused by incorrect file Paths
    def test_HtmlFileLoggerCatchThrownException(self):
        html_logger = HtmlFileLogger(True, "", "HtmlFileLoggerCatchThrownException", MessageType.GENERIC)
        html_logger.set_file_path("<>")
        html_logger.log_message(MessageType.GENERIC, "Test throws error as expected.")

        file_path = html_logger.get_file_path() + "\\" + html_logger.get_file_name()
        self.assertTrue(path.exists(file_path))

    # Verify that HTML File Logger catches and handles errors caused by incorrect file Paths.
    def test_FileLoggerEmptyFileNameException(self):
        with self.assertRaises(AttributeError):
            html_logger = HtmlFileLogger()
            self.assertIsNone(html_logger)

    # Verify File Logger with No Parameters assigns the correct default values.
    def test_FileLoggerNoParameters(self):
        html_logger = HtmlFileLogger("")
        self.assertEquals(html_logger.DEFAULT_LOG_FOLDER, html_logger.get_directory,
                          StringProcessor.safe_formatter("Expected Directory '{}'.", html_logger.DEFAULT_LOG_FOLDER))
        self.assertEquals("FileLog.html", html_logger.get_file_name(), "Expected correct File Name.")
        self.assertEquals(MessageType.INFORMATION, html_logger.get_message_type(),
                          "Expected Information Message Type.")

        file_path = html_logger.get_file_path() + "\\" + html_logger.get_file_name()
        self.assertTrue(path.exists(file_path))

    # Verify File Logger with only append parameter assigns the correct default values.
    def test_FileLoggerAppendOnly(self):
        html_logger = HtmlFileLogger("", True)
        self.assertEquals(html_logger.DEFAULT_LOG_FOLDER, html_logger.get_directory(),
                          StringProcessor.safe_formatter("Expected Directory '{}'.", html_logger.DEFAULT_LOG_FOLDER))
        self.assertEquals("FileLog.html", html_logger.get_file_name(), "Expected correct File Name.")
        self.assertEquals(MessageType.INFORMATION.name, html_logger.get_message_type(),
                          "Expected Information Message Type.")

        file_path = html_logger.get_file_path() + "\\" + html_logger.get_file_name()
        self.assertFalse(path.exists(file_path))

    # Verify File Logger with only File Name parameter assigns the correct default values.
    # Verify default extension is added '.html'
    def test_FileLoggerNameOnlyAddExtension(self):
        html_logger = HtmlFileLogger("", False, MessageType.INFORMATION, "FileNameOnly")
        self.assertEquals(html_logger.DEFAULT_LOG_FOLDER, html_logger.get_directory(),
                          StringProcessor.safe_formatter("Expected Directory '{}'.", html_logger.DEFAULT_LOG_FOLDER))
        self.assertEquals("FileNameOnly.html", html_logger.get_file_name(), "Expected correct File Name.")
        self.assertEquals(MessageType.INFORMATION, html_logger.get_message_type(),
                          "Expected Information Message Type.")

        file_path = html_logger.get_file_path() + "\\" + html_logger.get_file_name()
        self.assertTrue(path.exists(file_path))

    # Verify File Logger with only Message Type parameter assigns the correct default values.
    def test_FileLoggerMessageTypeOnly(self):
        html_logger = HtmlFileLogger("", False, MessageType.WARNING)
        self.assertEquals(html_logger.DEFAULT_LOG_FOLDER, html_logger.get_directory(),
                          StringProcessor.safe_formatter("Expected Directory '{}'.", html_logger.DEFAULT_LOG_FOLDER))
        self.assertEquals("FileLog.html", html_logger.get_file_name(), "Expected correct File Name.")
        self.assertEquals(MessageType.WARNING, html_logger.get_message_type(), "Expected Warning Message Type.")

        file_path = html_logger.get_file_path() + "\\" + html_logger.get_file_name()
        self.assertTrue(path.exists(file_path))

    # Verify File Logger with only Append and File Name parameters assigns the correct default values.
    def test_FileLoggerAppendFileName(self):
        html_logger = HtmlFileLogger("", True, MessageType.INFORMATION, "AppendFileName")
        self.assertEquals(html_logger.DEFAULT_LOG_FOLDER, html_logger.get_directory(),
                          StringProcessor.safe_formatter("Expected Directory '{}'.", html_logger.DEFAULT_LOG_FOLDER))

        self.assertEquals("AppendFileName.html", html_logger.get_file_name(), "Expected correct File Name.")
        self.assertEquals(MessageType.INFORMATION.name, html_logger.get_message_type(),
                          "Expected Information Message Type.")

        file_path = html_logger.get_file_path() + "\\" + html_logger.get_file_name()
        self.assertFalse(path.exists(file_path))

    # Verify File Logger with only Log Folder and Append parameters assigns the correct default values.
    def test_FileLoggerAppendLogFolder(self):
        append_file_directory_path = LoggingConfig.get_log_directory() + "/" + "Append File Directory"
        html_logger = HtmlFileLogger(append_file_directory_path, True)
        self.assertEquals(append_file_directory_path, html_logger.get_directory(),
                          "Expected Directory 'Append File Directory'.")
        self.assertEquals("FileLog.html", html_logger.get_file_name(), "Expected correct File Name.")
        self.assertEquals(MessageType.INFORMATION.name, html_logger.get_message_type(),
                          "Expected Information Message Type.")

    # Verify File Logger with only Log Folder and File Name parameters assigns the correct default values.
    def test_FileLoggerLogFolderFileName(self):
        log_folder_file_name_directory = LoggingConfig.get_log_directory() + "/" + "Log Folder File Name Directory"
        html_logger = HtmlFileLogger(log_folder_file_name_directory, "LogFolderFileName.html")
        self.assertEquals(log_folder_file_name_directory, html_logger.get_directory(),
                          "Expected Directory 'Log Folder File Name Directory'.")
        self.assertEquals("LogFolderFileName.html", html_logger.get_file_name(), "Expected correct File Name.")
        self.assertEquals(MessageType.INFORMATION.name, html_logger.get_message_type(),
                          "Expected Information Message Type.")

    # Verify File Logger with only Log Folder and Messaging Level parameters assigns the correct default values.
    def test_FileLoggerLogFolderMessagingLevel(self):
        log_folder_messaging_level_directory_path = LoggingConfig.get_log_directory() + "/" \
                                                    + "Log Folder Messaging Level Directory"
        html_logger = HtmlFileLogger(log_folder_messaging_level_directory_path, False, MessageType.WARNING)
        self.assertEquals(log_folder_messaging_level_directory_path, html_logger.get_directory(),
                          "Expected Directory 'Log Folder Messaging Level Directory'.")
        self.assertEquals("FileLog.html", html_logger.get_file_name(), "Expected correct File Name.")
        self.assertEquals(MessageType.WARNING.name, html_logger.get_message_type(),
                          "Expected Warning Message Type.")

    # Verify File Logger with only Append and Messaging Level parameters assigns the correct default values.
    def test_FileLoggerAppendMessagingLevel(self):
        html_logger = HtmlFileLogger("", True, MessageType.WARNING)
        self.assertEquals(html_logger.DEFAULT_LOG_FOLDER, html_logger.get_directory(),
                          StringProcessor.safe_formatter("Expected Directory '{}'.", html_logger.DEFAULT_LOG_FOLDER))
        self.assertEquals("FileLog.html", html_logger.get_file_name(), "Expected correct File Name.")
        self.assertEquals(MessageType.WARNING.name, html_logger.get_message_type(), "Expected Warning Message Type.")

        file_path = html_logger.get_file_path() + "\\" + html_logger.get_file_name()
        self.assertFalse(path.exists(file_path))

    # Verify File Logger with only Messaging Level and file name parameters assigns the correct default values.
    def test_FileLoggerMessagingLevelFileName(self):
        html_logger = HtmlFileLogger("", False, MessageType.WARNING, "MessagingTypeFile.html")
        self.assertEquals(html_logger.DEFAULT_LOG_FOLDER, html_logger.get_directory(),
                          StringProcessor.safe_formatter("Expected Directory '{}'.", html_logger.DEFAULT_LOG_FOLDER))
        self.assertEquals("MessagingTypeFile.html", html_logger.get_file_name(), "Expected correct File Name.")
        self.assertEquals(MessageType.WARNING.name, html_logger.get_message_type(), "Expected Warning Message Type.")

        file_path = html_logger.get_file_path() + "\\" + html_logger.get_file_name()
        self.assertFalse(path.exists(file_path))

    # Verify File Logger with only Append, log folder and file name parameters assigns the correct default values.
    def test_FileLoggerAppendLogFolderFileName(self):
        append_log_folder_file_name_directory_path = LoggingConfig.get_log_directory() + "\\" \
                                                     + "AppendLogFolderFileNameDirectory "
        html_logger = HtmlFileLogger(append_log_folder_file_name_directory_path, True, MessageType.INFORMATION,
                                     "AppendLogFolderFileName.html")
        self.assertEquals(append_log_folder_file_name_directory_path, html_logger.get_directory(),
                          "Expected Directory AppendLogFolderFileNameDirectory")
        self.assertEquals("AppendLogFolderFileName.html", html_logger.get_file_name(),
                          "Expected correct File Name.")
        self.assertEquals(MessageType.INFORMATION.name, html_logger.get_message_type(),
                          "Expected Information Message Type.")

    # Verify File Logger with only Append, log folder and Messaging Level parameters assigns the correct default values.
    def test_FileLoggerAppendLogFolderMessagingLevel(self):
        append_log_folder_file_name_directory = LoggingConfig.get_log_directory() + "\\" \
                                                + "AppendLogFolderFileNameDirectory "
        html_logger = HtmlFileLogger(append_log_folder_file_name_directory, True, MessageType.WARNING)
        self.assertEquals(append_log_folder_file_name_directory, html_logger.get_directory(),
                          "Expected Directory AppendLogFolderFileNameDirectory")
        self.assertEquals("FileLog.html", html_logger.get_file_name(), "Expected correct File Name.")
        self.assertEquals(MessageType.WARNING.name, html_logger.get_message_type(), "Expected Warning Message Type.")

        file_path = html_logger.get_file_path() + "\\" + html_logger.get_file_name()
        self.assertFalse(path.exists(file_path))

    # Verify File Logger with only File Name, Append and Messaging Level parameters assigns the correct default values.
    def test_FileLoggerFileNameAppendMessagingLevel(self):
        html_logger = HtmlFileLogger("FileNameAppendMessagingLevel.html", True, MessageType.WARNING)
        self.assertEquals(html_logger.DEFAULT_LOG_FOLDER, html_logger.get_directory(),
                          StringProcessor.safe_formatter("Expected Directory '{}'.", html_logger.DEFAULT_LOG_FOLDER))
        self.assertEquals("FileNameAppendMessagingLevel.html", html_logger.get_file_name(),
                          "Expected correct File Name.")
        self.assertEquals(MessageType.WARNING.name, html_logger.get_message_type(), "Expected Warning Message Type.")

        file_path = html_logger.get_file_path() + "\\" + html_logger.get_file_name()
        self.assertTrue(path.exists(file_path))

    # Verify File Logger with only Log Folder,
    # File Name and Messaging Level parameters assigns the correct default values.
    def test_FileLoggerLogFolderFileNameMessagingLevel(self):
        log_folder_file_name_messaging_level_directory_path = LoggingConfig.get_log_directory() \
                                                              + "/" + "LogFolderFileNameMessagingLevelDirectory"
        html_logger = HtmlFileLogger(log_folder_file_name_messaging_level_directory_path,
                                     "LogFolderFileNameMessagingLevel.html", MessageType.WARNING)
        self.assertEquals(log_folder_file_name_messaging_level_directory_path, html_logger.get_directory(),
                          "Expected Directory 'LogFolderFileNameMessagingLevelDirectory'")
        self.assertEquals("LogFolderFileNameMessagingLevel.html", html_logger.get_file_name(),
                          "Expected correct File Name.")
        self.assertEquals(MessageType.WARNING, html_logger.get_message_type(), "Expected Warning Message Type.")

        file_path = html_logger.get_file_path() + "\\" + html_logger.get_file_name()
        self.assertTrue(path.exists(file_path))

    # Verify that HTML File Logger catches and handles errors caused by empty file name.
    def test_HtmlFileLoggerEmptyFileNameException(self):
        with self.assertRaises(AttributeError):
            html_logger = HtmlFileLogger()
            self.assertIsNone(html_logger)

    # Read a file and return it as a string
    # @ param filePath The file path to read
    # @ return The contents of the file
    @staticmethod
    def readTextFile(file_path):
        text = ""
        try:
            text = open(file_path).read()
        except FileNotFoundError as e:
            # TODO: Print stack trace
            e.args
        return text
