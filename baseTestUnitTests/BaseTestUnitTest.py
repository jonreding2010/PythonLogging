import unittest
from baseLogger.ConsoleLogger import ConsoleLogger
from baseLogger.FileLogger import FileLogger
from baseLogger.LoggingConfig import LoggingConfig
from baseLogger.constants.MessageType import MessageType
from baseTest.BaseTest import BaseTest
from baseTest.BaseTestObject import BaseTestObject
from performance.PerfTimerCollection import PerfTimerCollection
from utilities.Config import Config


# Unit test class for BaseTest class.
class BaseTestUnitTest(unittest.TestCase, BaseTest):
    # Verify fully qualified test name.
    # @Test(groups = TestCategories.FRAMEWORK)
    def fullyQualifiedTestNameTest(self):
        test_name = self.get_fully_qualified_test_class_name()
        self.assertEquals(test_name,
                          "com.magenic.jmaqs.base.BaseTestUnitTest.fullyQualifiedTestNameTest")

    # Validate setting a new logger.
    # @Test(groups = TestCategories.FRAMEWORK)
    def fileLoggerTest(self):
        self.set_logger(FileLogger())

        if not isinstance(FileLogger, self.get_logger()):
            self.fail("FileLogger was not set.")

    # Validate Logging Verbose works.
    # @Test(groups = TestCategories.FRAMEWORK)
    def logVerboseTest(self):
        self.log_verbose("This is a test to log verbose.", None)

    # Validate that Try To Log is working.
    # @Test(groups = TestCategories.FRAMEWORK)
    def tryToLogTest(self):
        self.try_to_log(MessageType.INFORMATION, "Try to log message.")

    # Validate adding exceptions to the Logged Exception list adds the exceptions correctly.
    # @Test(groups = TestCategories.FRAMEWORK)
    def addLoggedExceptionsTest(self):
        exceptions = list()
        exceptions.append("First Exception.")
        exceptions.append("Second Exception.")
        exceptions.append("Third Exception.")
        self.set_logged_exceptions(exceptions)

        self.assertTrue(self.get_logged_exceptions() == 3,
                        "Expect that 3 Logged exceptions are in this exception list.")

    # Validate the Logging Enabled Setting is YES (set in Config).
    # @Test(groups = TestCategories.FRAMEWORK)
    def loggingEnabledSettingTest(self):
        config = Config()
        self.assertEquals(self.get_logging_enabled_setting(), LoggingConfig.get_logging_enabled_setting(config))

    # Validate Setting the Test Object to a new Test Object (Console Logger instead of File Logger).
    # @Test(groups = TestCategories.FRAMEWORK)
    def setTestObjectTest(self):
        logger = ConsoleLogger()
        base_test_object = BaseTestObject(logger, self.get_fully_qualified_test_class_name())
        self.set_test_object(base_test_object)
        self.assertTrue(isinstance(self.get_test_object().getLogger(), ConsoleLogger),
                        "Expected Test Object to be set to have a Console Logger.")

    # @Test(groups = TestCategories.FRAMEWORK)
    def testSetPerformanceCollection(self):
        perf_timer_collection = PerfTimerCollection(self.get_logger(), self.get_fully_qualified_test_class_name())
        self.set_perf_timer_collection(perf_timer_collection)

    # @Test(groups = TestCategories.FRAMEWORK)
    def testGetPerformanceCollection(self):
        perf_timer_collection = PerfTimerCollection(self.get_logger(),
                                                    self.get_fully_qualified_test_class_name())
        self.set_perf_timer_collection(perf_timer_collection)
        self.assertIsNotNone(self.get_perf_timer_collection())

    # @Test(groups = TestCategories.FRAMEWORK)
    def testGetTestContext(self):
        self.assertIsNotNone(self.get_test_context())

    # @Test(groups = TestCategories.FRAMEWORK)
    def testSetTestContext(self):
        test_context = self.get_test_context()
        test_context.setAttribute("testName", "SetTestContext")
        self.set_test_context(test_context)
        self.assertIsNotNone(self.get_test_context())
        self.assertEquals(self.get_test_context().getAttribute("testName"), "SetTestContext")

    # @Test(groups = TestCategories.FRAMEWORK)
    def testGetManagerStore(self):
        self.assertIsNotNone(self.get_manager_store())

    # @see com.magenic.jmaqs.utilities.BaseTest.BaseTest#beforeLoggingTeardown(org.testng.ITestResult)
    # @Override
    def beforeLoggingTeardown(self, resultType):
        pass
