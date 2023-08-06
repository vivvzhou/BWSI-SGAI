from enum import IntEnum
from enum import Enum
import numpy as np
import random

class Action(Enum):
    Skip = 0
    Save = 1
    Squish = -1
    Skum = 0
    
class ActionCost(Enum):
    SAVE = 30
    SQUISH = 5
    SKIP = 15
    SCRAM = 120