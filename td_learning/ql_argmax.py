import copy
from enum import IntEnum
import numpy as np

def QLargmax_all(list_):
    """
    Returns all argmax of given list in a list. Different from np.argmax which 
    returns first instance only.
    """
    return np.argwhere(list_ == list_.max()).flatten()