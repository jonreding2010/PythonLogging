from baseTest.BaseTest import BaseTest
from baseTest.BaseTestObject import BaseTestObject


# The type Base extendable test.
# @param <T> the type parameter
class BaseExtendableTest(BaseTestObject, BaseTest):
    # Instantiates a new Base extendable test.
    def init__(self):
        pass

    # @Override
    # @SuppressWarnings("unchecked")
    def get_test_object(self):
        return super().get_test_object()

    # @BeforeMethod
    # @Override
    def setup(self, method, test_context):
        super().setup(method, test_context)

    # @Override
    def create_new_test_object(self):
        pass
