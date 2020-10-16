from datetime import datetime
from baseLogger.ConsoleLogger import ConsoleLogger
from baseLogger.Logger import Logger
from baseLogger.LoggingConfig import LoggingConfig
from baseLogger.constants.MessageType import MessageType
from performance.PerfTimer import PerfTimer


# Response timer collection class -  Object to be owned by Test Class (Object),
# and passed to page Constructors to insert Performance Timers
class PerfTimerCollection:
    # Locker object so the Performance Timer Document save doesn't save at the same time
    writerLocker = object()

    # List object to store Timers
    openTimerList = {str(): PerfTimer()}

    TimerList = [PerfTimer()]

    FileName = str()

    TestName = str()

    PerfPayloadString = str()

    Log = Logger()

    # Initializes a new instance of the < see cref = "PerfTimerCollection" / > class
    # @param "logger" Logger to use
    # @param "fullyQualifiedTestName" Test name
    def __init__(self, fully_qualified_test_name, logger=ConsoleLogger()):
        self.Log = logger
        self.TestName = fully_qualified_test_name

    # Gets the list of response time tests
    def getTimerList(self):
        return [PerfTimer]

    # Gets the File name
    def getFileName(self):
        return self.FileName

    # Sets the file name
    def setFileName(self, new_file_name):
        self.FileName = new_file_name

    # Gets the test name
    def getTestName(self):
        return self.TestName

    # Sets the test name
    def setTestName(self, new_test_name):
        self.TestName = new_test_name

    # Gets or sets the generic payload string
    def getPerfPayloadString(self):
        return self.PerfPayloadString

    def setPerfPayloadString(self, new_payload_string):
        self.PerfPayloadString = new_payload_string

    # Gets the logger
    def getLogger(self):
        return Logger()

    def setLogger(self, new_logger):
        self.Log = new_logger

    # Method to start a timer with a specified name and for a specific context
    # @param contextName Name of the context
    # @param timerName Name of the timer
    def StartTimer(self, timer_name, context_name=str()):
        if timer_name in self.openTimerList:
            raise ArgumentException("Timer already Started: " + timer_name)
        else:
            self.Log.log_message(MessageType.INFORMATION, "Starting response timer: {}", timer_name)
            timer = PerfTimer()
            timer.TimerName = timer_name
            timer.TimerContext = context_name
            timer.StartTime = datetime.now()
            self.openTimerList[timer_name] = timer

    # Method to stop an existing timer with a specified name for a test
    # @param name = "timerName" > Name of the timer
    def EndTimer(self, timerName):
        et = datetime.now()
        if not timerName in self.openTimerList:
            raise ArgumentException("Response time test does not exist")
        else:
            self.Log.log_message(MessageType.INFORMATION, "Stopping response time test: {}", timerName)
            self.openTimerList.get(timerName).EndTime = et
            self.openTimerList.get(timerName).Duration = self.openTimerList[timerName].EndTime \
                                                         - self.openTimerList[timerName].StartTime
            self.TimerList.append(self.openTimerList[timerName])
            self.openTimerList.pop(timerName)

    # Method to Write the Performance Timer Collection to disk
    # @param log The current test Logger
    def Write(self, log):
        # Only run if the response times is greater than 0
        if len(self.TimerList) > 0:
            # Locks the writer if other tests are using it
            lock(writerLocker)
            try:
                # If filename doesn't exist, we haven't created the file yet
                if self.FileName is None:
                    self.FileName = "PerformanceTimerResults" + "-" + self.TestName + "-" + DateTime.UtcNow.ToString(
                        "O").Replace(':', '-') + ".xml"

                log.LogMessage(MessageType.INFORMATION,
                               "filename: " + LoggingConfig.get_log_directory() + "\\" + self.FileName)

                settings = XmlWriterSettings();
                settings.WriteEndDocumentOnClose = True;
                settings.Indent = True;

                writer = XmlWriter.Create(string.Format("{0}\\{1}", LoggingConfig.get_log_directory(), self.FileName),
                                          settings)

                x = XmlSerializer(self.GetType())
                x.Serialize(writer, self)

                writer.Flush()
                writer.Close()
            except Exception as e:
                log.LogMessage(MessageType.ERROR, "Could not save response time file.  Error was: {}", e)

    # Method to Read in the Performance Timer Collection from disk
    # @param filepath The file from which to initialize
    # @returns PerfTimerCollection initialized from file path
    @staticmethod
    def LoadPerfTimerCollection(filepath):
        serializer = XmlSerializer(typeof(PerfTimerCollection))

        reader = StreamReader(filepath)
        perfTimerCollection = PerfTimerCollection
        serializer.Deserialize(reader)
        reader.Close()
        return perfTimerCollection
