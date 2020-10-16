import unittest
from baseTest.BaseGenericTest import BaseGenericTest
from baseTest.BaseTestObject import BaseTestObject
from baseTest.DriverManager import DriverManager
from performance.PerfTimerCollection import PerfTimerCollection


# The type Base test object test.
class BaseTestObjectUnitTest(unittest.TestCase, BaseGenericTest):
    # Test Constructor with Log and Method.
    # @Test(groups = TestCategories.FRAMEWORK)
    def testBaseTestObject1(self):
        test_object = self.get_test_object()

        # final String methodName = this.method.getName();
        base_test_object = BaseTestObject(test_object.get_logger(), "FakeTestName")
        self.assertIsNotNone(base_test_object, "Checking that Base Test Object instantiated correctly")

    # Test Constructor with Test Object.
    # @Test(groups = TestCategories.FRAMEWORK)
    def testBaseTestObject2(self):
        test_object = self.get_test_object()
        base_test_object = BaseTestObject(test_object)
        self.assertIsNotNone(base_test_object, "Checking that Base Test Object instantiated correctly")

    # Test set value.
    # @Test(groups = TestCategories.FRAMEWORK)
    def testSetValue(self):
        test_object = self.get_test_object()
        key = "SetKey"
        value = "SetKey Value"
        test_object.setValue(key, value)
        self.assertTrue(test_object.getValues().containsKey(key), "Checking that key exists in test object dictionary")
        self.assertEquals(test_object.getValues().get(key), value, "Checking that value set correctly")

    # Test set object.
    # @Test(groups = TestCategories.FRAMEWORK)
    def testSetObject(self):
        # TODO: check test in java
        test_object = self.get_test_object()
        test_key = "SetObject"
        test_object = dict()
        test_object.append(test_key, test_object)
        self.assertTrue(test_key in test_object, "Checking that key exists in test object dictionary")
        self.assertEquals(test_object.get(test_key), test_object, "Checking that value set correctly")

    # Test get log.
    # @Test(groups = TestCategories.FRAMEWORK)
    def testGetLog(self):
        test_object = self.get_test_object()
        self.assertIsNotNone(test_object.getLogger(), "Checking that logger is not null.")

    # Test set log.
    # @Test(groups = TestCategories.FRAMEWORK)
    def testSetLog(self):
        test_object = self.get_test_object()
        logger = self.get_logger()
        test_object.setLogger(logger)
        self.assertEquals(test_object.get_logger(), logger, "Checking that logger set correctly.")

    # Test Get Perf Collection Timer - Not Null.
    # @Test(groups = TestCategories.FRAMEWORK)
    def testGetPerfTimerCollectionNotNull(self):
        test_object = self.get_test_object()
        self.assertIsNotNone(test_object.getPerfTimerCollection(), "Checking that logger is not null.")

    # Test Set Perf Collection Timer - Get/Set.
    # @Test(groups = TestCategories.FRAMEWORK)
    def testSetPerfTimerCollectionGetSet(self):
        test_object = self.get_test_object()
        perf_timer_collection = PerfTimerCollection(test_object.get_logger(), "FakeTestName")
        test_object.setPerfTimerCollection(perf_timer_collection)
        self.assertEquals(test_object.getPerfTimerCollection(), perf_timer_collection,
            "Checking that perf timer collection set correctly.")

    # Test get values.
    # @Test(groups = TestCategories.FRAMEWORK)
    def testGetValues(self):
        test_object = self.get_test_object()
        self.assertIsNotNone(test_object.getValues(), "Checking that values is not null.")

    # Test get objects.
    # @Test(groups = TestCategories.FRAMEWORK)
    def testGetObjects(self):
        test_object = self.get_test_object()
        self.assertIsNotNone(test_object.getObjects(), "Checking that objects is not null.")

    # Test Get Manager Store - Not Null.
    # @Test(groups = TestCategories.FRAMEWORK)
    def testGetManagerStoreNotNull(self):
        test_object = self.get_test_object()
        self.assertIsNotNone(test_object.getManagerStore(), "Checking that objects is not null.")

    # Test add driver manager.
    # @Test(groups = TestCategories.FRAMEWORK)
    def testAddDriverManager(self):
        test_object = self.get_test_object()
        # supplier = () -> null;
        supplier = None
        driver_manager = self.getDriverManager(test_object, supplier)
        self.assertEquals(test_object.getManagerStore().size(), 0, "Checking that manager store is empty")
        test_object.addDriverManager(driver_manager)
        self.assertEquals(test_object.getManagerStore().size(), 1, "Checking that manager store has 1 object added")

    # Test add driver manager - Overwrite True.
    # @Test(groups = TestCategories.FRAMEWORK)
    def testAddDriverManagerTrue(self):
        test_object = self.get_test_object()
        # supplier = () -> null;
        supplier = None
        driver_manager = self.getDriverManager(test_object, supplier)
        driver_manager2 = self.getDriverManager(test_object, supplier)
        self.assertEquals(test_object.getManagerStore().size(), 0, "Checking that manager store is empty")
        test_object.addDriverManager(driver_manager, True)
        self.assertEquals(test_object.getManagerStore().size(), 1, "Checking that manager store has 1 object added")
        test_object.addDriverManager(driver_manager2, True)
        self.assertEquals(test_object.getManagerStore().size(), 1, "Checking that manager store has 1 object added")

    # Test add driver manager - Overwrite False.
    # @Test(groups = TestCategories.FRAMEWORK)
    def testAddDriverManagerFalse(self):
        test_object = self.get_test_object()
        # supplier = () -> null;
        supplier = None
        driver_manager = self.getDriverManager(test_object, supplier)

        self.assertEquals(test_object.getManagerStore().size(), 0, "Checking that manager store is empty")
        test_object.addDriverManager(driver_manager, False)
        self.assertEquals(test_object.getManagerStore().size(), 1, "Checking that manager store has 1 object added")

    # Test add driver manager 2.
    # @Test(groups = TestCategories.FRAMEWORK)
    def testAddDriverManager2(self):
        test_object = self.get_test_object()
        # supplier = () -> null;
        supplier = None
        driver_manager = self.getDriverManager(test_object, supplier)
        test_key = "DriverManager1"
        self.assertEquals(test_object.getManagerStore().size(), 0, "Checking that manager store is empty")
        test_object.addDriverManager(test_key, driver_manager)
        self.assertEquals(test_object.getManagerStore().size(), 1, "Checking that manager store has 1 object added")
        self.assertTrue(test_object.getManagerStore().containsKey(test_key), "Checking if key exists in Manager Store")

    # Test close.
    # @Test(groups = TestCategories.FRAMEWORK)
    def testClose(self):
        test_object = self.get_test_object()
        # supplier = () -> null;
        supplier = None
        driver_manager = self.getDriverManager(test_object, supplier)
        test_key = "DriverManager1"
        test_object.addDriverManager(test_key, driver_manager)
        test_object.close()
        self.assertIsNone(test_object.getManagerStore(), "Checking that manager store has been closed");
        self.assertEquals(test_object.getValues().size(), 0, "Checking if values in manager store are closed");

    # Test add associated file.
    # @Test(groups = TestCategories.FRAMEWORK)
    def testAddAssociatedFile(self):
        test_object = self.get_test_object()
        File temp = None
        try:
            temp = File.createTempFile("tempfile", ".tmp")
        except IOError as e:
            e.printStackTrace()

        assert temp.exists();

        self.assertTrue(test_object.addAssociatedFile(temp.getAbsolutePath()), "Checking that associated file was added");
        self.assertEquals((test_object.getArrayOfAssociatedFiles()).length, 1,
            "Checking that one file was added to array.")

    # Test remove associated file.
    # @Test(groups = TestCategories.FRAMEWORK)
    def testRemoveAssociatedFile(self):
        test_object = self.get_test_object()
        File temp = None
        try:
            temp = File.createTempFile("tempfile", ".tmp")
        except IOError as e:
            e.printStackTrace()

        assert temp.exists();
        path = temp.getAbsolutePath()

        self.assertTrue(test_object.addAssociatedFile(path), "Checking that associated file was added")
        self.assertTrue(test_object.removeAssociatedFile(path), "Checking that assocai")

    # Test get array of associated files.
    # @Test(groups = TestCategories.FRAMEWORK)
    def testGetArrayOfAssociatedFiles(self):
        test_object = self.get_test_object()
        File temp = None
        try:
            temp = File.createTempFile("tempfile", ".tmp")
        except IOError as e:
            e.printStackTrace()

        assert temp.exists();
        path = temp.getAbsolutePath()
        self.assertTrue(test_object.addAssociatedFile(path), "Checking that associated file was added")
        self.assertIsNotNone(test_object.getArrayOfAssociatedFiles(), "Checking that array is instantiated")
        self.assertEquals(test_object.getArrayOfAssociatedFiles().length, 1, "Checking that array is not empty")

    # Test contains associated file.
    # @Test(groups = TestCategories.FRAMEWORK)
    def testContainsAssociatedFile(self):
        test_object = self.get_test_object()
        File temp = None
        try:
            temp = File.createTempFile("tempfile", ".tmp")
        except IOError as e:
            e.printStackTrace()

        assert temp.exists();
        path = temp.getAbsolutePath()
        self.assertTrue(test_object.addAssociatedFile(path), "Checking that associated file was added")
        self.assertIsNotNone(test_object.getArrayOfAssociatedFiles(), "Checking that array is instantiated")
        self.assertTrue(test_object.containsAssociatedFile(path), "Checking if array contains file")

    @staticmethod
    def getDriverManager(supplier, test_object):
        return DriverManager(supplier, test_object)
