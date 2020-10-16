import os
import unittest
from baseLogger.ConsoleLogger import ConsoleLogger
from baseLogger.FileLogger import FileLogger
from baseLogger.LoggingConfig import LoggingConfig
from baseLogger.constants.LoggingEnabled import LoggingEnabled
from baseLogger.constants.MessageType import MessageType
from utilities.Config import Config
from utilities.StringProcessor import StringProcessor


# Logging Configuration unit test class.
# Tests running in serial.
# @Test(singleThreaded = true)
class LoggingConfigUnitTest(unittest.TestCase):
    # Test getting Logging Enabled Setting.
    # Override Config to 'YES'
    def test_getLoggingEnabledSettingTest(self):
        new_value_map = {"log": "YES"}
        config = Config()
        config.add_general_test_setting_values(new_value_map, True)
        self.assertEquals(LoggingConfig(config).get_logging_enabled_setting(Config()), LoggingEnabled.YES.name,
                          "Expected Logging Enabled Setting YES.")

    # Test getting Logging Enabled Setting.
    # Override Config to 'ONFAIL'
    def test_getLoggingEnabledOnFailSettingTest(self):
        new_value_map = {"Log": "ONFAIL"}
        config = Config()
        config.add_general_test_setting_values(new_value_map, True)
        self.assertEquals(LoggingConfig().get_logging_enabled_setting(config), LoggingEnabled.ONFAIL.name,
                          "Expected Logging Enabled Setting ONFAIL.")

    # Test getting Logging Enabled Setting.
    # Override Config to 'NO'
    def test_getLoggingDisabledSettingTest(self):
        new_value_map = {"Log": "NO"}
        Config().add_general_test_setting_values(new_value_map, True)
        self.assertEquals(LoggingConfig().get_logging_enabled_setting(), LoggingEnabled.NO.name,
                          "Expected Logging Enabled Setting NO.")

    # Test getting Logging Enabled Setting with an Illegal Argument
    # Override Config to 'INVALIDVALUE' - Expect IllegalArgumentException
    def test_getLoggingSettingIllegalArgumentTest(self):
        with self.assertRaises(NotImplementedError):
            new_value_map = {"Log": "INVALIDVALUE"}
            Config().add_general_test_setting_values(new_value_map, True)
            LoggingConfig().get_logging_enabled_setting()

    # Test getting Logging Level Setting.
    # Override Config to 'VERBOSE'
    def test_getLoggingLevelVerboseSettingTest(self):
        new_value_map = {"LogLevel": "VERBOSE"}
        Config().add_general_test_setting_values(new_value_map, True)
        self.assertEquals(MessageType.VERBOSE.name, LoggingConfig().get_logging_level_setting(),
                          "Expected Logging Level Setting VERBOSE.")

    # Test getting Logging Level Setting.
    #  Override Config to 'INFORMATION'
    def test_getLoggingLevelInformationSettingTest(self):
        new_value_map = {"LogLevel": "INFORMATION"}
        Config().add_general_test_setting_values(new_value_map, True)
        self.assertEquals(MessageType.INFORMATION.name, LoggingConfig().get_logging_level_setting(),
                          "Expected Logging Level Setting INFORMATION.")

    # Test getting Logging Level Setting.
    # Override Config to 'GENERIC'
    def test_getLoggingLevelGenericSettingTest(self):
        new_value_map = {"LogLevel": "GENERIC"}
        Config().add_general_test_setting_values(new_value_map, True)
        self.assertEquals(MessageType.GENERIC.name, LoggingConfig().get_logging_level_setting(),
                          "Expected Logging Level Setting GENERIC.")

    # Test getting Logging Level Setting.
    # Override Config to 'SUCCESS'
    def test_getLoggingLevelSuccessSettingTest(self):
        new_value_map = {"LogLevel": "SUCCESS"}
        Config().add_general_test_setting_values(new_value_map, True)
        self.assertEquals(MessageType.SUCCESS.name, LoggingConfig().get_logging_level_setting(),
                          "Expected Logging Level Setting SUCCESS.")

    # Test getting Logging Level Setting.
    # Override Config to 'WARNING'
    def test_getLoggingLevelWarningSettingTest(self):
        new_value_map = {"LogLevel": "WARNING"}
        Config().add_general_test_setting_values(new_value_map, True)
        self.assertEquals(MessageType.WARNING.name, LoggingConfig().get_logging_level_setting(),
                          "Expected Logging Level Setting WARNING.")

    # Test getting Logging Level Setting.
    # Override Config to 'ERROR'
    def test_getLoggingLevelErrorSettingTest(self):
        new_value_map = {"LogLevel": "ERROR"}
        Config().add_general_test_setting_values(new_value_map, True)
        self.assertEquals(MessageType.ERROR.name, LoggingConfig().get_logging_level_setting(),
                          "Expected Logging Level Setting ERROR.")

    # Test getting Logging Level Setting.
    # Override Config to 'SUSPENDED'
    def test_getLoggingLevelSuspendedSettingTest(self):
        new_value_map = {"LogLevel": "SUSPENDED"}
        Config().add_general_test_setting_values(new_value_map, True)
        self.assertEquals(MessageType.SUSPENDED.name, LoggingConfig().get_logging_level_setting(),
                          "Expected Logging Level Setting SUSPENDED.")

    # Test getting Logging Level Setting with Illegal Argument.
    # Override Config to 'INVALIDVALUE' - Expect IllegalArgumentException
    def test_getLoggingLevelIllegalArgumentTest(self):
        with self.assertRaises(AttributeError):
            new_value_map = {"LogLevel": "INVALIDVALUE"}
            config = Config().add_general_test_setting_values(new_value_map, True)
            LoggingConfig(config).get_logging_level_setting()

    # Test getting File Logger.
    # Override Config LogType to 'TXT' which creates FileLogger.
    def test_getFileLoggerTest(self):
        new_value_map = {"LogType": "TXT", "Log": "YES"}
        config = Config().add_general_test_setting_values(new_value_map, True)
        file_name = "TestLog.txt"
        logging_config = LoggingConfig(config).get_logger(file_name)
        self.assertTrue(isinstance(logging_config, FileLogger), "Expected Logger to be of Type FileLogger.")

    # Test getting File Logger.
    # Override Config LogType to 'CONSOLE' which creates ConsoleLogger.
    def test_getConsoleLoggerTest(self):
        new_value_map = {"LogType": "CONSOLE", "Log": "YES"}
        logging_config = LoggingConfig()
        logging_config.add_general_test_setting_values(new_value_map, True)
        file_name = "TestLog.txt"
        logger = logging_config.get_logger(file_name)
        instance = isinstance(logger, ConsoleLogger)
        self.assertTrue(instance, "Expected Logger to be of Type ConsoleLogger.")

    # Test getting File Logger.
    # Override Config Log to 'NO' which creates ConsoleLogger by default.
    def test_getConsoleLoggerLoggingDisabledTest(self):
        new_value_map = {"Log": "NO"}
        Config().add_general_test_setting_values(new_value_map, True)
        file_name = "TestLog.txt"
        logging_config = LoggingConfig().get_logger(file_name)
        instance = isinstance(logging_config, ConsoleLogger)
        self.assertTrue(instance, "Expected Logger to be of Type ConsoleLogger.")

    # Test getting Log Directory.
    def test_getLogDirectoryTest(self):
        default_path = os.path.abspath(os.path.dirname(__file__)) + "\\Logs"
        self.assertEquals(LoggingConfig().get_log_directory(), default_path,
                          StringProcessor.safe_formatter("Expected Default Path '{}'.", default_path))
