from enum import Enum


class UavWeight(Enum):
    MICRO = 'MICRO' # A drone that weighs ≤ 0.55 pounds
    MINI = 'MINI' # A drone that weighs more than micro and ≤ 4.4 pounds
    LIMITED = 'LIMITED' # A drone that weighs more than mini and ≤ 20.9 pounds
    BANTAM = 'BANTAM' # A drone that weighs more than limited
