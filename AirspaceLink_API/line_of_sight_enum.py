from enum import Enum


class LineOfSight(Enum):
    VLOS = 'VLOS'   # Visual line of sight: the pilot can see the drone throughout the entire operation
    EVLOS = 'EVLOS' # Extended visual line of sight: the drone has spotters relaying information to the pilot
    BVLOS = 'BVLOS' # Beyond visual line of sight: the pilot may not see the drone at some point throughout the operation
