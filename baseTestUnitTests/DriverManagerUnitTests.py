import unittest
from baseLogger.ConsoleLogger import ConsoleLogger
from baseTest.BaseGenericTest import BaseGenericTest
from baseTest.BaseTestObject import BaseTestObject
from baseTest.DriverManager import DriverManager
from baseTest.ManagerDictionary import ManagerDictionary


class DriverManagerUnitTest(unittest.TestCase, BaseGenericTest):
    # @Test(groups = TestCategories.FRAMEWORK)
    def testGetBaseDriver(self):
        driver_manager = self.getDriverManager()
        driver_manager.set_base_driver("Fake String")
        self.assertIsNotNone(driver_manager.get_base_driver())


    # @Test(groups = TestCategories.FRAMEWORK)
    def testSetBaseDriver(self):
        driver_manager = self.getDriverManager()
        driver_manager.set_base_driver("Fake String")
        self.assertIsNotNone(driver_manager.get_base_driver())

    # @Test(groups = TestCategories.FRAMEWORK)
    def testIsDriverInitializedTrue(self):
        driver_manager = self.getDriverManager()
        self.assertIsNotNone(driver_manager.get_base())
        self.assertTrue(driver_manager.is_driver_initialized())

    # @Test(groups = TestCategories.FRAMEWORK)
    def testIsDriverInitializedFalse(self):
        driver_manager = self.getDriverManager()
        self.assertFalse(driver_manager.is_driver_initialized())

    # @Test(groups = TestCategories.FRAMEWORK)
    def testGetLogger(self):
        driver_manager = self.getDriverManager()
        self.assertIsNotNone(driver_manager.get_logger())

    # @Test(groups = TestCategories.FRAMEWORK)
    def testGetBase(self):
        driver_manager = self.getDriverManager()
        self.assertIsNotNone(driver_manager.get_base())

    # Can we add a manager by type
    # [TestMethod]
    # [TestCategory(TestCategories.Framework)]
    def testAddManagerByType(self):
        dictionary = self.getDictionary()
        dictionary.Add(self.getDriverManager())
        self.assertTrue(dictionary.ContainsKey(typeof(WebServiceDriverManager).FullName))

    # Does adding item increment count
    # [TestMethod]
    # [TestCategory(TestCategories.Framework)]
    def testAddIncrementCount(self):
        dictionary = self.getDictionary()
        dictionary.Add(self.getDriverManager())
        self.assertEquals(1, dictionary.Count)

    # Is empty count zero
    # [TestMethod]
    # [TestCategory(TestCategories.Framework)]
    def testEmptyCountZero(self):
        dictionary = self.getDictionary()
        self.assertEquals(0, dictionary.Count)

    # Does clear remove all item
    # [TestMethod]
    # [TestCategory(TestCategories.Framework)]
    def testClearRemovesAll(self):
        dictionary = self.getDictionary()
        dictionary.Add(self.getDriverManager())
        dictionary.Add(str(), self.getDriverManager())
        dictionary.Clear()
        self.assertEquals(0, dictionary.Count)

    # Throw exception if we try add on top of an existing manager
    # [TestMethod]
    # [TestCategory(TestCategories.Framework)]
    # [ExpectedException(typeof(ArgumentException))]
    def testThrowDriverAlreadyExist(self):
        dictionary = self.getDictionary()
        dictionary.Add(self.getDriverManager())
        dictionary.Add(self.getDriverManager())

        self.fail("Previous line should have failed the test.")

    # Throw exception if we try add a named manager on top of an existing manager
    # [TestMethod]
    # [TestCategory(TestCategories.Framework)]
    # [ExpectedException(typeof(ArgumentException))]
    def testThrowNamedDriverAlreadyExist(self):
        dictionary = self.getDictionary()
        dictionary.Add(str(), self.getDriverManager())
        dictionary.Add(str(), self.getDriverManager())
        self.fail("Previous line should have failed the test.")

    # Can override existing
    # [TestMethod]
    # [TestCategory(TestCategories.Framework)]
    def testCanOverrideExisting(self):
        dictionary = self.getDictionary()
        dictionary.Add(self.getDriverManager())
        dictionary.AddOrOverride(self.getDriverManager())

        self.assertEquals(1, dictionary.Count)

    # Can use override for new manager
    # [TestMethod]
    # [TestCategory(TestCategories.Framework)]
    def testCanOverrideNonExisting(self):
        dictionary = self.getDictionary()
        dictionary.AddOrOverride(self.getDriverManager())
        self.assertEqual(1, dictionary.Count)

    # Can add named and unnamed
    # [TestMethod]
    # [TestCategory(TestCategories.Framework)]
    def testAddNamedAndUnnamed(self):
        dictionary = self.getDictionary()
        dictionary.Add(str(), self.getDriverManager())
        dictionary.Add(self.getDriverManager())
        self.assertEquals(2, dictionary.Count)

    # Remove by type
    # [TestMethod]
    # [TestCategory(TestCategories.Framework)]
    def testRemoveByType(self):
        dictionary = self.getDictionary()
        manager_to_keep = self.getDriverManager()
        dictionary.Add(self.getDriverManager())
        dictionary.Add(str(), manager_to_keep)
        dictionary.Remove(typeof(WebServiceDriverManager))
        self.assertEquals(manager_to_keep, dictionary[str()])

    # Remove by name
    # [TestMethod]
    # [TestCategory(TestCategories.Framework)]
    def testRemoveByName(self):
        dictionary = self.getDictionary()
        manager_to_keep = self.getDriverManager()
        dictionary.Add(manager_to_keep)
        dictionary.Add(str(), self.getDriverManager())
        dictionary.Remove(str())
        self.assertEquals((((WebServiceDriverManager)managerToKeep).Get(),
                        dictionary.GetDriver <EventFiringWebServiceDriver, WebServiceDriverManager > ())

    # Managers map correctly
    # [TestMethod]
    # [TestCategory(TestCategories.Framework)]
    def testManagersMap(self):
        dictionary = self.getDictionary()
        manager_to_keep = self.getDriverManager()
        manager_to_keep2 = self.getDriverManager()

        dictionary.Add(manager_to_keep)
        dictionary.Add(str()), manager_to_keep2)

        self.assertEquals((((WebServiceDriverManager)managerToKeep).Get(),
                        dictionary.GetDriver <EventFiringWebServiceDriver, WebServiceDriverManager> ())
        self.assertEquals(manager_to_keep2, dictionary[str()])

    # Manager dispose
    # [TestMethod]
    # [TestCategory(TestCategories.Framework)]
    def ManagerDispose(self):
        manager = ManagerDictionary()
        manager.close()
        self.assertIsNotNone(manager)

    @staticmethod
    def getDictionary():
        base_test_object = BaseTestObject(ConsoleLogger(), str())
        return base_test_object.get_manager_store()

    # private DriverManager<String> getDriverManager() {

    def getDriverManager(self):
        baseTestObject = BaseTestObject(ConsoleLogger(), str())
        return DriverManager(() -> "Fake String here", getTestObject())

