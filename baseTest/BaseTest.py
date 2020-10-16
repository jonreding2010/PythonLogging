import os
import traceback
from datetime import datetime
from baseLogger.ConsoleLogger import ConsoleLogger
from baseLogger.FileLogger import FileLogger
from baseLogger.LoggingConfig import LoggingConfig
from baseLogger.constants.LoggingEnabled import LoggingEnabled
from baseLogger.constants.MessageType import MessageType
from baseLogger.constants.TestResultType import TestResultType
from baseTest.BaseTestObject import BaseTestObject
from baseTest.TestResult import TestResult
from utilities.Config import Config
from utilities.StringProcessor import StringProcessor


# Base test class.
class BaseTest:
    # All logged exceptions caught and saved to be thrown later.
    loggedExceptions = dict()

    # Logging Enabled Setting from Config file.
    loggingEnabledSetting = str()

    # The test result object.
    testResult = str()

    # The Collection of Base Test Objects to use.
    baseTestObjects = dict()

    # The Performance Timer Collection.
    perfTimerCollection = str()

    # The TestNG Test Context.
    testContextInstance = str()

    # The Fully Qualified Test Class Name.
    # ThreadLocal<String> fullyQualifiedTestClassName = new ThreadLocal<>();
    fullyQualifiedTestClassName = list()

    # Initializes a new instance of the BaseTest class.
    def __init__(self):
        self.loggedExceptions = dict()
        self.baseTestObjects = dict()

    # Gets the Performance Timer Collection.
    # @return Performance Timer Collection
    def get_perf_timer_collection(self):
        return self.perfTimerCollection

    # Sets the Performance Timer Collection.
    # @param perfTimerCollection Performance Timer Collection to use
    def set_perf_timer_collection(self, perf_timer_collection):
        self.perfTimerCollection = perf_timer_collection

    # Gets the Logger for this test.
    # @return Logger object
    def get_logger(self):
        return self.get_test_object().getLogger()

    # Set the Logger for this test.
    # @param log The Logger object
    def set_logger(self, log):
        self.get_test_object().setLogger(log)

    # Gets the Logging Enabled setting.
    # @return Logging Enabled setting
    def get_logging_enabled_setting(self):
        return self.loggingEnabledSetting

    # Set the Logging Enabled setting.
    # @param setting The LoggingEnabled enum
    def set_logging_enabled(self, setting):
        self.loggingEnabledSetting = setting

    # Get logged exceptions for this test.
    # @return ArrayList of logged exceptions for this test
    def get_logged_exceptions(self):
        if not (self.fullyQualifiedTestClassName in self.loggedExceptions):
            result = list()
        else:
            result = self.loggedExceptions.get(self.fullyQualifiedTestClassName)
        return result

    # Set Logged Exception List - Add/Update entry in Hash Map with test class name as key.
    # @param loggedExceptionList ArrayList of logged exceptions to use.
    def set_logged_exceptions(self, logged_exception_list):
        self.loggedExceptions[self.fullyQualifiedTestClassName] = logged_exception_list

    # Gets the Driver Store.
    # @return The Driver Store
    def get_manager_store(self):
        return self.get_test_object().getManagerStore()

    # Gets the TestNG Test Context.
    # @return The TestNG Test Context
    def get_test_context(self):
        return self.testContextInstance

    # Sets the TestNG Test context.
    # @param testContext The TestNG Test Context to use
    def set_test_context(self, test_context):
        self.testContextInstance = test_context

    # Get the BaseTestObject for this test.
    # @return The BaseTestObject
    def get_test_object(self):
        if not (self.fullyQualifiedTestClassName in self.baseTestObjects):
            self.create_new_test_object()

        return self.baseTestObjects.get(self.fullyQualifiedTestClassName)

    # Sets the Test Object.
    # @param baseTestObject The Base Test Object to use
    def set_test_object(self, base_test_object):
        key = self.fullyQualifiedTestClassName
        # if key in self.baseTestObjects:
        #    self.baseTestObjects[key] base_test_object)
        # else:
        self.baseTestObjects[key] = base_test_object

    # Setup before a test.
    # @param method      The initial executing Method object
    # @param testContext The initial executing Test Context object
    # @BeforeMethod(alwaysRun = true)
    def setup(self, method, test_context):
        self.testContextInstance = test_context

        # Get the Fully Qualified Test Class Name and set it in the object
        test_name = method.getDeclaringClass() + "." + method.getName()
        test_name = test_name.replaceFirst("class ", "")
        self.fullyQualifiedTestClassName.append(test_name)
        self.create_new_test_object()

    # Cleanup after a test.
    # @AfterMethod(alwaysRun = true)
    def teardown(self):
        try:
            self.before_logging_teardown(self.testResult)
        except Exception as e:
            self.try_to_log(MessageType.WARNING, "Failed before logging teardown because: {}", e.message)

        # Log the test result
        if self.testResult.getStatus() == TestResult.SUCCESS:
            self.try_to_log(MessageType.SUCCESS, "Test Passed")
        elif self.testResult.getStatus() == TestResult.FAILURE:
            self.try_to_log(MessageType.ERROR, "Test Failed")
        elif self.testResult.getStatus() == TestResult.SKIP:
            self.try_to_log(MessageType.INFORMATION, "Test was skipped")
        else:
            self.try_to_log(MessageType.WARNING, "Test had an unexpected result.")

        # Cleanup log files we don't want
        try:
            if isinstance(FileLogger,
                          self.get_logger()) and self.testResult.getStatus() == TestResult.SUCCESS and self.loggingEnabledSetting == LoggingEnabled.ONFAIL:
                # Files.delete(self.getLogger()).getFilePath())
                os.remove(self.get_logger().get_file_path())
        except Exception as e:
            self.try_to_log(MessageType.WARNING, "Failed to cleanup log files because: {}", e.message)

        # Get the Fully Qualified Test Name
        fully_qualified_test_name = self.fullyQualifiedTestClassName

        try:
            base_test_object = self.get_test_object()
            # Release logged messages
            self.loggedExceptions.pop(fully_qualified_test_name)

            # Release the Base Test Object
            self.baseTestObjects.pop(fully_qualified_test_name, base_test_object)
        except Exception:
            pass

        # Create console logger to log subsequent messages
        self.set_test_object(BaseTestObject(ConsoleLogger(), fully_qualified_test_name))
        self.fullyQualifiedTestClassName.clear()

    # Set the test result after each test execution.
    # @param testResult The result object
    # @AfterMethod(alwaysRun = true)
    def set_test_result(self, test_result):
        self.testContextInstance = test_result.get_test_context()
        self.testResult = test_result

    # Steps to do before logging teardown results.
    # @param resultType The test result
    def before_logging_teardown(self, result_type):
        pass

    # Setup logging data.
    # @return Logger
    def create_logger(self):
        self.loggingEnabledSetting = LoggingConfig.get_logging_level_setting(Config())
        self.set_logged_exceptions(list)

        if self.loggingEnabledSetting != LoggingEnabled.NO:
            log = LoggingConfig().get_logger(StringProcessor.safe_formatter("{} - {}",
                                                                            [self.fullyQualifiedTestClassName,
                                                                             str(datetime.now().strftime(
                                                                                 "uuuu-MM-dd-HH-mm-ss-SSSS"))]),
                                             Config())
        else:
            log = ConsoleLogger()
        return log

    # Get the type of test result.
    # @return The type of test result
    def get_result_type(self):
        status = self.testResult.getStatus()
        if status == TestResult.SUCCESS:
            return TestResultType.PASS
        elif status == TestResult.FAILURE:
            return TestResultType.FAIL
        elif status == TestResult.SKIP:
            return TestResultType.SKIP
        else:
            return TestResultType.OTHER

    # Get the test result type as text.
    # @return The test result type as text
    def get_result_text(self):
        status = self.testResult.getStatus()
        if status == TestResult.SUCCESS:
            return "SUCCESS"
        elif status == TestResult.FAILURE:
            return "FAILURE"
        elif status == TestResult.SKIP:
            return "SKIP"
        else:
            return "OTHER"

    # Get the fully qualified test name.
    # @return The test name including class
    def get_fully_qualified_test_class_name(self):
        return self.fullyQualifiedTestClassName

    # Try to log a message - Do not fail if the message is not logged.
    # @param messageType The type of message
    # @param message     The message text
    # @param args        String format arguments
    def try_to_log(self, message_type, message, args=None):
        # Get the formatted message
        formatted_message = StringProcessor.safe_formatter(message, args)

        try:
            # Write to the log
            self.get_logger().logMessage(message_type, formatted_message)

            # If this was an error and written to a file, add it to the console
            # output as well
            if message_type == MessageType.ERROR and not isinstance(ConsoleLogger, self.get_logger()):
                print(formatted_message)
        except Exception as e:
            print(formatted_message)
            print("Logging failed because: " + e.message)

    # Log a verbose message and include the automation specific call stack data.
    # @param message The message text
    # @param args    String format arguments
    def log_verbose(self, message, args=None):
        messages = list()
        messages.append(StringProcessor.safe_formatter(message, args) + os.linesep)

        for element in traceback.format_exc():
            # If the stack trace element is from the com.magenic package
            # (excluding this method) append the stack trace line
            if element.startsWith("com.magenic") and not ("BaseTest.logVerbose" in str(element)):
                messages.append(element + os.linesep)
        self.get_logger().logMessage(MessageType.VERBOSE, messages)

    # Create a Base test object.
    def create_new_test_object(self):
        new_logger = self.create_logger()
        self.set_test_object(BaseTestObject(new_logger, self.fullyQualifiedTestClassName))
