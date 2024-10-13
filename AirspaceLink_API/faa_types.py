# Enumeration, used in aviation calls
from enum import Enum

class AviationType(Enum):
    CONTROLLED_AIRSPACE = 'controlled_airspace'
    UASFM_CEILING = 'uasfm_ceiling'
    SUA = 'sua'
    WASHINGTON_FRZ = 'washington_frz'
    NSUFR_PT = 'nsufr_pt'
    NSUFR_FT = 'nsufr_ft'
    STADIUM = 'stadium'
    AIRPORTS = 'airports'
    AIRSPACE_SCHEDULE = 'airspace_schedule'
    TFR = 'tfr'

"""
Type	Description
'controlled_airspace'	| Controlled Airspace Classification.
'uasfm_ceiling' | UAS Facility Management Flight Ceiling.
'sua' |	Both sua_prohibited and sua_restricted.
'washington_frz' |	Washington DC Flight Restricted Zone.
'nsufr_pt' | Part Time National Security UAS Flight Restriction.
'nsufr_ft' | Full Time National Security UAS Flight Restriction.
'stadium' | Select stadiums containing temporary flight restriction. The stadium points are buffered by 3 nautical miles.
'airports' | Points designated for landing or takeoff. Returns all airports within 3 nautical miles of input geometry by default.
'airspace_schedule' | Controlled airspace schedule for select airports across the country (geometry has no bearing on the result).
'tfr' | Temporary Flight Restrictions imposed by the FAA to restrict aircraft operations within designated areas.

"""
