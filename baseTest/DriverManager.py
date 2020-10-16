from baseTest.BaseTestObject import BaseTestObject


# The type Driver manager.
class DriverManager:
    # Base Test Object.
    baseTestObject = BaseTestObject

    # The Base driver.
    baseDriver = object()

    # The Get driver.
    getDriverSupplier = object()

    # Instantiates a new Driver manager.
    # @param getDriverFunction driver function supplier
    # @param baseTestObject    the base test object
    def __init__(self, get_driver_function, base_test_object):
        self.baseTestObject = base_test_object
        self.getDriverSupplier = get_driver_function

    # Gets base driver.
    # @return the base driver
    def get_base_driver(self):
        return self.baseDriver

    # Sets base driver.
    # @param baseDriver the base driver
    def set_base_driver(self, base_driver):
        self.baseDriver = base_driver

    # Is driver initialized boolean.
    # @return the boolean
    def is_driver_initialized(self):
        return self.baseDriver is not None

    # Gets logger.
    # @return the logger
    def get_logger(self):
        return self.baseTestObject.get_logger()

    # Get base object.
    # @return the object
    def get_base(self):
        if self.baseDriver is None:
            self.baseDriver = self.getDriverSupplier
        return self.baseDriver

    # Gets test object.
    # @return the test object
    def get_test_object(self):
        return self.baseTestObject
