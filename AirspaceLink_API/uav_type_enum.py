from enum import Enum


class UavType(Enum):
    FIXED_WING = 'FIXED_WING'
    HELICOPTER = 'HELICOPTER'
    MULTIROTOR = 'MULTIROTOR'
    HYBRID = 'HYBRID'
