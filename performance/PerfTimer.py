from datetime import datetime


# Response timer class - holds a single response timer
class PerfTimer:
    TimerContext = str()

    TimerName = str()

    StartTime = str()

    EndTime = str()

    Duration = int()

    # Gets the name of the Page associated with the Timer
    def getTimerContext(self):
        return self.TimerContext

    # Sets the name of the Page associated with the Timer
    def setTimerContext(self, new_timer_context):
        self.TimerContext = new_timer_context

    # Gets the Timer Name
    def getTimerName(self):
        return self.TimerName

    # Sets the Timer Name
    def setTimerName(self, new_timer_name):
        self.TimerName = new_timer_name

    # Gets the start time
    def getStartTime(self):
        return self.StartTime

    # Sets the start time
    def setStartTime(self, new_start_time):
        self.StartTime = new_start_time

    # Gets the end time
    def getEndTime(self):
        return self.EndTime

    # Sets the end time
    def setEndTime(self, new_end_time):
        self.EndTime = new_end_time

    # Gets the duration
    # [XmlIgnore]
    def getDuration(self):
        return self.Duration

    # Set the duration
    # [XmlIgnore]
    def setDuration(self, new_duration):
        self.Duration = new_duration

    # Gets the Serializable duration
    def getDurationTicks(self):
        return self.Duration

    # Sets the Serializable duration
    def setDurationTicks(self):
        self.Duration = int()
