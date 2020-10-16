from baseLogger.Logger import Logger
from baseLogger.constants.MessageType import MessageType
from baseTest.ManagerDictionary import ManagerDictionary
from performance.PerfTimerCollection import PerfTimerCollection
from utilities.StringProcessor import StringProcessor


# The BaseTestObject class.
class BaseTestObject:
    # The Logger.
    logger = Logger()

    # The Performance Timer Collection.
    perfTimerCollection = str()

    # Concurrent Hash Map of string key value pairs.
    values = dict()

    # Concurrent Hash Map of string key and object value pairs.
    objects = dict()

    # Dictionary of String key and driver value pairs.
    managerStore = ManagerDictionary

    # ArrayList of Strings for associated files.
    associatedFiles = list()

    # The Fully Qualified Test Name.
    fullyQualifiedTestName = str()

    # Was the object closed.
    isClosed = False

    # Check if the object has been closed
    # @return True if the object is closed
    def getClosed(self):
        return self.isClosed

    # Initializes a new instance of the BaseTestObject class.
    # @param logger                 The test's logger
    # @param fullyQualifiedTestName The test's fully qualified test name
    def __init__(self, base_test_object=None, logger=None, fully_qualified_test_name=str()):
        if base_test_object is None:
            self.set_up_without_base_test_object(logger, fully_qualified_test_name)
        else:
            self.set_up_base_test_object(base_test_object)

    def set_up_without_base_test_object(self, logger, fully_qualified_test_name):
        self.logger = logger
        self.perfTimerCollection = PerfTimerCollection(logger, fully_qualified_test_name)
        self.values = dict()
        self.objects = dict()
        self.managerStore = dict()
        self.associatedFiles = list()
        self.fullyQualifiedTestName = fully_qualified_test_name

        logger.logMessage(MessageType.INFORMATION, "Setup test object for " + fully_qualified_test_name)

    # Initializes a new instance of the BaseTestObject class.
    # @param baseTestObject An existing base test object
    def set_up_base_test_object(self, base_test_object):
        self.logger = base_test_object.get_logger()
        self.perfTimerCollection = base_test_object.get_perf_timer_collection()
        self.values = base_test_object.get_values()
        self.objects = base_test_object.getObjects()
        self.managerStore = base_test_object.get_manager_store()
        self.associatedFiles = list()
        self.fullyQualifiedTestName = base_test_object.get_fully_qualified_test_name()

        base_test_object.get_logger().logMessage(MessageType.INFORMATION, "Setup test object")

    # Gets the logger.
    # @return The logger
    def get_logger(self):
        return self.logger

    # Sets the logger.
    # @param logger The logger to use
    def set_logger(self, logger):
        self.logger = logger

    # Gets the Performance Timer Collection.
    # @return Performance Timer Collection
    def get_perf_timer_collection(self):
        return self.perfTimerCollection

    # Sets the Performance Timer Collection.
    # @param perfTimerCollection Performance Timer Collection
    def set_perf_timer_collection(self, perf_timer_collection):
        self.perfTimerCollection = perf_timer_collection

    def get_fully_qualified_test_name(self):
        return self.fullyQualifiedTestName

    # Gets the Concurrent Hash Map of string key value pairs.
    # @return Concurrent Hash Map of string key value pairs
    def get_values(self):
        return self.values

    # Sets the Concurrent Hash Map of string key and object value pairs.
    # @param values Concurrent Hash Map of string key value pairs to use
    # def setValues(self, ConcurrentHashMap<String, String> values) {
    def set_values(self, new_values):
        self.values = new_values

    # Gets the Concurrent Hash Map of string key and object value pairs.
    # @return Concurrent Hash Map of string key and object value pairs
    # def public ConcurrentMap<String, Object> getObjects() {
    def get_objects(self):
        return self.objects

    # Sets the Concurrent Hash Map of string key and object value pairs.
    # @param objects Concurrent Hash Map of string key and object value pairs to use
    # def setObjects(self, ConcurrentHashMap<String, Object> objects) {
    def set_objects(self, new_objects):
        self.objects = new_objects

    # Gets the Concurrent Hash Map of string key and driver value pairs.
    # @return Concurrent Hash Map of string key and driver value pairs
    def get_manager_store(self):
        return self.managerStore

    # Sets the Concurrent Hash Map of string key and driver value pairs.
    # @param managerStore Concurrent Hash Map of string key and driver value pairs to use.
    def set_manager_store(self, manager_store):
        self.managerStore = manager_store

    # Sets a string value, will replace if the key already exists.
    # @param key   The key
    # @param value The value to associate with the key
    def set_value(self, key, value):
        if self.values.containsKey(key):
            self.values.replace(key, value)
        else:
            self.values.put(key, value)

    # Sets an object value, will replace if the key already exists.
    # @param key   The key
    # @param value The value to associate with the key
    def set_object(self, key, value):
        if self.objects.containsKey(key):
            self.objects.replace(key, value)
        else:
            self.objects.put(key, value)

    # Add driver manager.
    # @param <T>              the type parameter
    # @param driverManager    the driver manager
    # @param overrideIfExists the override if exists
    # public <T extends DriverManager<?>> void addDriverManager(final T driverManager, final boolean overrideIfExists) {
    def add_driver_manager(self, driver_manager, override_if_exists=False):
        if override_if_exists:
            self.override_driver_manager(driver_manager.getClass().getTypeName(), driver_manager)
        else:
            self.managerStore.put(driver_manager.getClass().getTypeName(), driver_manager)

    # Override driver manager.
    # @param key           the key
    # @param driverManager the driver manager
    # def overrideDriverManager(final String key, final DriverManager<?> driverManager) {
    def override_driver_manager(self, key, driver_manager):
        if self.managerStore.containsKey(key):
            self.managerStore.putOrOverride(key, driver_manager)
        else:
            self.managerStore.put(key, driver_manager)

    # Add associated file boolean.
    # @param path the path
    # @return the boolean
    def add_associated_file(self, path):
        if path.exists():
            return self.associatedFiles.append(path)
        return False

    # Dispose of the driver store.
    # @param closing the closing
    def close(self, closing=False):
        if not closing:
            if self.managerStore is None:
                return
            self.logger.logMessage(MessageType.VERBOSE, "Start dispose")

            # for (final DriverManager<?> singleDriver : this.managerStore.values()) {
            for singleDriver in self.managerStore:
                if singleDriver is not None:
                    try:
                        singleDriver.close()
                    except Exception as e:
                        # raise DriverDisposalException(StringProcessor.safe_formatter("Unable to properly dispose of
                        # driver"), e)
                        raise Error(StringProcessor.safe_formatter("Unable to properly dispose of driver"), e)
                self.managerStore = None
                self.logger.logMessage(MessageType.VERBOSE, "End dispose")

            self.isClosed = True

    # Remove associated file boolean.
    # @param path the path
    # @return the boolean
    def remove_associated_file(self, path):
        return self.associatedFiles.remove(path)

    # Get array of associated files string [ ].
    # @return the string [ ]
    def get_array_of_associated_files(self):
        return self.associatedFiles

    # Contains associated file boolean.
    # @param path the path
    # @return the boolean
    def contains_associated_file(self, path):
        return path in self.associatedFiles
