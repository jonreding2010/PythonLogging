import unittest
from baseLogger.ConsoleLogger import ConsoleLogger
from baseLogger.constants.MessageType import MessageType


# Unit test class for ConsoleLogger.java
class ConsoleLoggerUnitTest(unittest.TestCase):
    # Log message to a new console baseLogger
    def test_consoleLoggerLogMessage(self):
        console_logger = ConsoleLogger()
        console_logger.log_message("Test String {} {}", ["args1", "args2"])
        self.assertIsNotNone(console_logger)

    # Log message to a new console baseLogger using defined message type
    def test_consoleLoggerLogMessageSelectType(self):
        console_logger = ConsoleLogger()
        console_logger.log_message("Test String {}", "args1", MessageType.GENERIC)
        self.assertIsNotNone(console_logger)

    # Write message to new console baseLogger
    def test_consoleLoggerWriteMessage(self):
        console_logger = ConsoleLogger()
        console_logger.write("Test String {} {}", ["args1", "args2"])
        self.assertIsNotNone(console_logger)

    #  Write message to new console baseLogger using defined message type
    def test_consoleLoggerWriteMessageSelectType(self):
        console_logger = ConsoleLogger()
        console_logger.write("TestString {}", "args1", MessageType.GENERIC)
        self.assertIsNotNone(console_logger)

    # Write message with new line to new console baseLogger
    def test_consoleLoggerWriteLineMessage(self):
        console_logger = ConsoleLogger()
        console_logger.write("Test String {} {}", ["args1", "args2"])
        self.assertIsNotNone(console_logger)

    # Write message with new line to new console baseLogger using defined message type
    def test_consoleLoggerWriteMessageLineSelectType(self):
        console_logger = ConsoleLogger()
        console_logger.write("TestString {}", "args1", MessageType.GENERIC)
        self.assertIsNotNone(console_logger)
