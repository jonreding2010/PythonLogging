from enum import Enum


class TestResult(Enum):
    # Test status
    CREATED = -1,
    SUCCESS = 1,
    FAILURE = 2,
    SKIP = 3,
    SUCCESS_PERCENTAGE_FAILURE = 4,
    STARTED = 16,
