from enum import Enum


# The type of result.
class TestResultType(Enum):
    # test passed.
    PASS = "PASS",

    # The test failed.
    FAIL = "FAIL",

    # The test was inconclusive.
    INCONCLUSIVE = "INCONCLUSIVE",

    # The test was skipped.
    SKIP = "SKIP",

    # The test had an unexpected result.
    OTHER = "OTHER"
