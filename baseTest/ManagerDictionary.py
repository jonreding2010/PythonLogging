
# Driver manager dictionary.
from baseTest.DriverManager import DriverManager


class ManagerDictionary(DriverManager):

    # @Override
    def close(self):
        self.clear()

    # @Override
    def clear(self):
        for entry in self.entrySet():
            try:
                entry.getValue().close()
            except Exception as e:
                raise ManagerDisposalException(e)

        super().clear()

    # Gets driver.
    # @param <T> the type parameter
    # @param key the key
    # @return the driver
    # @SuppressWarnings("unchecked")
    def get_driver(self, key):
        return self.get(key)

    # Put.
    # @param driverManager the driver manager
    def put(self, driver_manager):
        self.put(driver_manager.getClass().getName(), driver_manager)

    # Put or override.
    # @param key           the key
    # @param driverManager the driver manager
    def putOrOverride(self, driver_manager, key=None):
        if key is None:
            key = driver_manager.getClass().getName()

        self.remove(key)
        self.put(key, driver_manager)

    # Remove boolean.
    # @param key the key
    # @return the boolean
    def remove(self, key):
        if self.containsKey(key):
            try:
                self.get(key).close()
            except Exception as e:
                raise ManagerDisposalException(e)

        super().remove(key)
        return not self.containsKey(key)
