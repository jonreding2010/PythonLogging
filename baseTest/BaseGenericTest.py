# Base Generic Test class for Unit Tests and Other testing scenarios.
from baseTest.BaseExtendableTest import BaseExtendableTest
from baseTest.BaseTestObject import BaseTestObject


class BaseGenericTest(BaseExtendableTest):

    # @Override
    def beforeLoggingTeardown(self, resultType):
        # No before logging steps needed in this scenario
        pass

    # @Override
    def createNewTestObject(self):
        self.set_test_object(BaseTestObject(self.create_logger(), self.get_fully_qualified_test_class_name()))
