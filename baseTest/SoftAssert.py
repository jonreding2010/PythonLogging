import os
from baseLogger.ConsoleLogger import ConsoleLogger
from baseTest.SoftAssertException import SoftAssertException
from baseLogger.constants.MessageType import MessageType
from utilities.StringProcessor import StringProcessor


# SoftAssert class
class SoftAssert:
    # List of all asserted exceptions
    listOfExceptions = list()

    # Initializes a new instance of the SoftAssert class.
    # Setup the Logger
    # @param baseLogger Logger to be used
    def __init__(self, test_name, logger=ConsoleLogger()):
        self.test_name = test_name
        self.Log = logger

    # Gets a value indicating whether the user checked for failures
    DidUserCheckForFailures = False

    # Gets a count of total number of Asserts
    NumberOfAsserts = 0

    # Gets a count of total number of Passed Asserts
    NumberOfPassedAsserts = 0

    # Gets a count of total number of Failed Asserts
    NumberOfFailedAsserts = 0

    # Gets the baseLogger being used
    Log = None

    # Override the baseLogger
    # @param log The new baseLogger
    def override_logger(self, log):
        self.Log = log

    # Gets a value indicating whether the boolean if the user checks for failures at the end of the test.
    # @returns If the user checked for failures.  If the number of asserts is 0, it returns true.
    def did_user_check(self):
        if self.NumberOfAsserts > 0:
            return self.DidUserCheckForFailures
        else:
            return True

    # Check if there are any failed soft asserts.
    # returns True if there are failed soft asserts
    def did_soft_asserts_fail(self):
        return self.NumberOfFailedAsserts > 0

    # Asserts if two strings are equal
    # @param expectedText Expected value of the string
    # @param actualText Actual value of the string
    # @param softAssertName Soft assert name
    # @param message Message to be used when logging
    # @returns Boolean if they are equal
    def assertEquals(self, expected_text, actual_text, soft_assert_name, message=""):
        if expected_text is not actual_text:
            if message is not None:
                raise SoftAssertException(
                    StringProcessor().safe_formatter("SoftAssert.AreEqual failed for {}.  Expected '{}' but got '{}'",
                                                     [soft_assert_name, expected_text, actual_text]))
            raise SoftAssertException(
                StringProcessor().safe_formatter("SoftAssert.AreEqual failed for {}.  Expected '{}' but got '{}'.  {}",
                                                 [soft_assert_name, expected_text, actual_text, message]))

        return self.invoke_test_text(self.test_name, expected_text, actual_text, message)

    # Soft assert for IsTrue
    # @param condition Boolean condition
    # @param softAssertName Soft assert name
    # @param failureMessage Failure message
    # @returns Boolean if condition is met
    def assertTrue(self, condition, soft_assert_name, failure_message=""):
        if not condition:
            if failure_message is None:
                raise SoftAssertException(
                    StringProcessor.safe_formatter("SoftAssert.IsTrue failed for: {}", soft_assert_name))
            raise SoftAssertException(StringProcessor.safe_formatter("SoftAssert.IsTrue failed for: {}. {}",
                                                                     [soft_assert_name, failure_message]))
        return self.invoke_test(self.test_name, soft_assert_name, failure_message)

    # Soft assert for IsFalse
    # @param condition Boolean condition
    # @param softAssertName Soft assert name
    # @param failureMessage Failure message
    # @returns Boolean if condition is met
    def assertFalse(self, condition, soft_assert_name, failure_message=""):
        if condition:
            if failure_message is None:
                raise SoftAssertException(
                    StringProcessor.safe_formatter("SoftAssert.IsFalse failed for: {}", soft_assert_name))
            raise SoftAssertException(StringProcessor.safe_formatter("SoftAssert.IsFalse failed for: {}. {}",
                                                                     [soft_assert_name, failure_message]))
        return self.invoke_test(self.test_name, soft_assert_name, failure_message)

    # Log final assert count summary
    def log_final_assert_data(self):
        message = ""

        message += StringProcessor.safe_formatter(
            "Total number of Asserts: {1}. Passed Asserts = {2} Failed Asserts = {2}{3}",
            [self.NumberOfAsserts, self.NumberOfPassedAsserts, self.NumberOfFailedAsserts, os.linesep])

        if len(self.listOfExceptions) > 0:
            message_type = MessageType.ERROR.value
            message += "List of failed exceptions:"

            for exception in self.listOfExceptions:
                # Will log all the exceptions that were caught in Asserts to the log file.
                message += exception
        else:
            # There are no exceptions that were caught in Asserts.
            message_type = MessageType.INFORMATION.value
            message += "There are no failed exceptions in the Asserts."

        self.Log.log_message(type, message)

    # Fail test if there were one or more failures
    # @param message Customer error message
    def fail_test_if_assert_failed(self, message="*See log for more details"):
        self.log_final_assert_data()
        self.DidUserCheckForFailures = True

        if self.did_soft_asserts_fail():
            errors = os.linesep.join(self.listOfExceptions)
            raise AssertionError("Soft Asserts failed:" + os.linesep + errors + os.linesep + message)

    # Wrap an assert inside a soft assert
    # @param assertFunction The assert function
    # @returns True if the asset passed
    def Assert(self, assert_function):
        # Resetting every time we invoke a test to verify the user checked for failures
        self.DidUserCheckForFailures = False

        try:
            assert_function.Invoke()
            self.NumberOfPassedAsserts = self.NumberOfPassedAsserts + 1
            assert_result = True
            self.Log.log_message("SoftAssert passed for: {}.", assert_function.Method.Name, MessageType.SUCCESS.name)
        except Exception as ex:
            self.NumberOfFailedAsserts = self.NumberOfFailedAsserts + 1
            assert_result = False
            self.Log.log_message(MessageType.WARNING, "SoftAssert failed for: {}. {}",
                                 [assert_function.Method.Name, ex.message])
            self.listOfExceptions.append(ex.message)
        finally:
            self.NumberOfAsserts = self.NumberOfAsserts + 1
        return assert_result

    # Wrap an assert that is expected to fail and the expected failure
    # @param assertFunction The assert function
    # @param expectedException The type of expected exception
    # @param assertName soft assert name
    # @param failureMessage Failure message
    # @returns True if the assert failed
    def fails(self, assert_function, expected_exception, assert_name, failureMessage=""):
        # Resetting every time we invoke a test to verify the user checked for failures
        self.DidUserCheckForFailures = False

        try:
            assert_function.Invoke()
            self.NumberOfFailedAsserts = self.NumberOfFailedAsserts + 1
            result = False
            self.Log.log_message(MessageType.WARNING.value,
                                 "SoftAssert failed for assert {}:  {} passed.  Expected failure type {}.",
                                 [assert_name, assert_function.Method.Name, expected_exception])
        except Exception as ex:
            if expected_exception in ex.args:
                self.NumberOfPassedAsserts = self.NumberOfPassedAsserts + 1
                result = True
                self.Log.log_message(MessageType.SUCCESS.value, "SoftAssert passed for assert {}: {}.",
                                     [assert_name, assert_function.Method.Name])
            else:
                self.NumberOfFailedAsserts = self.NumberOfFailedAsserts
                result = False
                self.Log.log_message(MessageType.WARNING.value,
                                     "SoftAssert failed for assert {}: {}. Expected failure:{} Actual failure: {}",
                                     [assert_name, assert_function, expected_exception, ex])
                self.listOfExceptions.append(ex)
        finally:
            self.NumberOfAsserts = self.NumberOfAsserts + 1
        return result

    # Executes the assert type passed as parameter and updates the total assert count
    # @param test Test method Action
    # @param expectedText">Expected value of the string
    # @param actualText">Actual value of the string
    # @param message">Test Name or Message
    # @returns Boolean if the assert is true
    def invoke_test_text(self, test, expected_text, actual_text, message):
        # Resetting every time we invoke a test to verify the user checked for failures
        self.DidUserCheckForFailures = False

        try:
            test.Invoke()
            self.NumberOfPassedAsserts = self.NumberOfPassedAsserts + 1
            result = True
            self.log_message(expected_text, actual_text, message, result)
        except Exception as ex:
            self.NumberOfFailedAsserts = self.NumberOfFailedAsserts + 1
            result = False
            self.log_message(expected_text, actual_text, message, result)
            self.listOfExceptions.append(ex)
        finally:
            self.NumberOfAsserts = self.NumberOfAsserts + 1
        return result

    # Executes the assert type passed as parameter and updates the total assert count
    # @param test Test method Action
    # @param softAssertName Soft assert name
    # @param message Test Name or Message
    # @returns Boolean if the assert is true
    def invoke_test(self, test, soft_assert_name, message):
        # Resetting every time we invoke a test to verify the user checked for failures
        self.DidUserCheckForFailures = False

        try:
            test.Invoke()
            self.NumberOfPassedAsserts = self.NumberOfPassedAsserts + 1
            result = True
            self.Log.log_message(MessageType.SUCCESS.value, "SoftAssert passed for: {}.", soft_assert_name)
        except Exception as ex:
            self.NumberOfFailedAsserts = self.NumberOfFailedAsserts + 1
            result = False
            self.Log.log_message(MessageType.WARNING.value, "SoftAssert failed for: {}. {}",
                                 [soft_assert_name, message])
            self.listOfExceptions.append(ex.message)
        finally:
            self.NumberOfAsserts = self.NumberOfAsserts + 1
        return result

    # Logs the message to the baseLogger
    # @param expectedText Expected value of the string
    # @param actualText">Actual value of the string
    # @param message Test Name or Message
    # @param result Decides the message type to be logged
    def log_message(self, expected_text, actual_text, message, result):
        if result:
            self.Log.log_message(MessageType.SUCCESS, StringProcessor.safe_formatter(
                "Soft Assert '{}' passed. Expected Value = '{}', Actual Value = '{}'.",
                [message, expected_text, actual_text]))
        else:
            self.Log.log_message(MessageType.WARNING, StringProcessor.safe_formatter(
                "Soft Assert '{}' failed. Expected Value = '{}', Actual Value = '{}'.",
                [message, expected_text, actual_text]))
