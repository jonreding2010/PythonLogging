import unittest
from baseLogger.FileLogger import FileLogger
from baseLogger.LoggingConfig import LoggingConfig
from baseTest.SoftAssert import SoftAssert
from baseLogger.constants.MessageType import MessageType


# Test class for soft asserts
# [TestClass]
# [ExcludeFromCodeCoverage]
class SoftAssertUnitTests(unittest.TestCase):
    # Examples of Soft Assert fails that would pass a test
    # [TestCategory(TestCategories.Utilities)]
    def test_SoftAssertFailsValidTest(self):
        soft_assert = SoftAssert(
            FileLogger(LoggingConfig.get_log_directory(), "UnitTests.SoftAssertUnitTests.SoftAssertFailsValidTest"))
        soft_assert.fails(lambda x: self.MethodThrowsNoneException(), TypeError,
                          "Assert Method Throws Explicit Exception",
                          "Failed to assert that method threw a NullReferenceException")
        result = 9 / 0
        soft_assert.fails(self.fail(f"Result should have thrown an error but is {result} instead"),
                          # soft_assert.assertFails(lambda x: (result = 9 / 0) self.fail(f"Result should have thrown
                          # an error but is {result} instead"),
                          ZeroDivisionError,
                          "Assert  action throws divide by zero exception",
                          "Failed to assert that we couldn't divide by zero")

        soft_assert.fail_test_if_assert_failed()

    # Examples of Soft Assert fails that would fail a test
    # [TestCategory(TestCategories.Utilities)]
    # [ExpectedException(typeof(AggregateException))]
    def test_SoftAssertFailsInvalidTest(self):
        with self.assertRaises(AttributeError):
            soft_assert = SoftAssert(FileLogger(LoggingConfig.get_log_directory(),
                                                "UnitTests.SoftAssertUnitTests.SoftAssertFailsInvalidTest"))
            soft_assert.fails(lambda x: self.MethodThrowsNoneException(), NotImplementedError,
                              "Assert Method Throws Explicit Exception",
                              "Failed to assert that method threw a NotImplementedException")
            result = 9 / 0
            soft_assert.fails(self.fail(f"Result should have thrown an error but is {result} instead"),
                              # soft_assert.assertFails(lambda x: (result = 9 / 0) self.fail(f"Result should have
                              # thrown an error but is {result} instead"),
                              TypeError,
                              "Assert  dividing by zero throws a null reference",
                              "Failed to assert that we couldn't divide by zero")
            soft_assert.fail_test_if_assert_failed()

    # Tests for soft asserts
    # [TestCategory(TestCategories.Utilities)]
    @staticmethod
    def test_SoftAssertValidTest():
        soft_assert = SoftAssert(
            FileLogger(LoggingConfig.get_log_directory(), "UnitTests.SoftAssertUnitTests.SoftAssertValidTest"))
        soft_assert.assertEquals("Yes", "Yes", "Utilities Soft Assert", "Message is not equal")
        soft_assert.assertEquals("YesAgain", "YesAgain", "Utilities Soft Assert 2")
        soft_assert.fail_test_if_assert_failed()

    # Tests for soft assert failures
    # [TestCategory(TestCategories.Utilities)]
    # [ExpectedException(typeof(AggregateException))]
    def test_SoftAssertFailTest(self):
        with self.assertRaises(AttributeError):
            soft_assert = SoftAssert(
                FileLogger(LoggingConfig.get_log_directory(), "UnitTests.SoftAssertUnitTests.SoftAssertFailTest"))
            soft_assert.assertEquals("Yes", "No", "Utilities Soft Assert", "Message is not equal")
            soft_assert.assertEquals("Yes", "NoAgain", "Utilities Soft Assert 2")
            soft_assert.fail_test_if_assert_failed()

    # Will return true if no asserts are done
    # [TestCategory(TestCategories.Utilities)]
    def test_SoftAssertVerifyUserCheck(self):
        soft_assert = SoftAssert(
            FileLogger(LoggingConfig.get_log_directory(), "UnitTests.SoftAssertUnitTests.SoftAssertVerifyUserCheck"))
        self.assertTrue(soft_assert.did_user_check())

    # Test to verify that the did user check will be set back to false if they check for failures
    # [TestCategory(TestCategories.Utilities)]
    def test_SoftAssertVerifyCheckForFailures(self):
        soft_assert = SoftAssert(FileLogger(LoggingConfig.get_log_directory(),
                                            "UnitTests.SoftAssertUnitTests.SoftAssertVerifyCheckForFailures"))
        soft_assert.assertEquals("Yes", "Yes", "Utilities Soft Assert", "Message is not equal")

        soft_assert.fail_test_if_assert_failed()
        self.assertTrue(soft_assert.did_user_check())

        soft_assert.assertEquals("Yes", "Yes", "Utilities Soft Assert", "Message is not equal")
        self.assertFalse(soft_assert.did_user_check())

    # Verify the did soft asserts fail check works
    # [TestCategory(TestCategories.Utilities)]
    def test_SoftAssertDidFailCheck(self):
        soft_assert = SoftAssert(FileLogger(LoggingConfig.get_log_directory(),
                                            "UnitTests.SoftAssertUnitTests.SoftAssertIsTrueTest",
                                            MessageType.GENERIC.name, True))
        soft_assert.assertTrue(True, "Test1")
        self.assertFalse(soft_assert.did_soft_asserts_fail())

        soft_assert.assertTrue(1 == 2, "Test2")
        self.assertTrue(soft_assert.did_soft_asserts_fail())

    # Test to verify the Is True method works
    # [TestCategory(TestCategories.Utilities)]
    @staticmethod
    def test_SoftAssertIsTrueTest():
        soft_assert = SoftAssert(FileLogger(LoggingConfig.get_log_directory(),
                                            "UnitTests.SoftAssertUnitTests.SoftAssertIsTrueTest",
                                            MessageType.GENERIC.name, True))
        soft_assert.assertTrue(True, "Test")
        soft_assert.fail_test_if_assert_failed()

    # Test to verify that soft asserts will fail a test
    # [TestCategory(TestCategories.Utilities)]
    # [ExpectedException(typeof(AggregateException))]
    def test_SoftAssertIsTrueTestFailure(self):
        with self.assertRaises(AttributeError):
            soft_assert = SoftAssert(FileLogger(LoggingConfig.get_log_directory(),
                                                "UnitTests.SoftAssertUnitTests.SoftAssertFailTest",
                                                MessageType.GENERIC.name, True))
            soft_assert.assertTrue(1 == 2, "Test")
            soft_assert.assertTrue(1 == 2, "Test1")
            soft_assert.assertTrue(True, "Test2")
            soft_assert.fail_test_if_assert_failed()

    # Test to verify the Is False method works
    # [TestCategory(TestCategories.Utilities)]
    @staticmethod
    def test_SoftAssertIsFalseTest():
        soft_assert = SoftAssert(FileLogger(LoggingConfig.get_log_directory(),
                                            "UnitTests.SoftAssertUnitTests.SoftAssertIsFalseTest",
                                            MessageType.GENERIC.value, True))
        soft_assert.assertFalse(2 == 1, "Test")
        soft_assert.fail_test_if_assert_failed()

    # Throws a None reference exception
    @staticmethod
    def MethodThrowsNoneException():
        return TypeError("Reference is None")
