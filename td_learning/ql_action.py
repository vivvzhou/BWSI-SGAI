from enum import IntEnum

class QLAction(IntEnum):
    """
    Enum of possible actions in the Cliff environment.
    """
    SAVE = 0
    SQUISH = 1
    SKIP = 2
    CURE = 3
    SCRAM = 4
