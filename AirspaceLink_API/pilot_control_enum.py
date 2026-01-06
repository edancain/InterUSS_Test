from enum import Enum


class PilotControl(Enum):
    SINGLE_PILOT = 'SINGLE_PILOT'
    MULTIPLE_PILOT = 'MULTIPLE_PILOT'
    AUTOMATED_CONTROL = 'AUTOMATED_CONTROL'
