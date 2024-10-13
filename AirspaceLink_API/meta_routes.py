# NB: OUTLINE OF CALLS, THIS IS NOT SOMETHING THAT WE USE CURRENTLY FOR DRONE DELIVERIES, AND SO IT HASN'T
# BEEN WORKED ON. THIS IS A HOLDER ONLY, DESCRIBING THE CALLS AND CALL REQUIREMENTS.


# https://developers.airspacelink.com/#meta-routes

# METADATA
import requests
import json



def main():
  url = 'https://airhub-api-sandbox.airspacelink.com/v1/metadata'
  token = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ild3dDk2SlJDTE9ER1pEeEpiRVVxdSJ9.eyJodHRwczovL2Fpcmh1Yi5haXJzcGFjZWxpbmsuY29tL3V0bSI6InZhbnRpcyIsImlzcyI6Imh0dHBzOi8vaWQtZGV2LmFpcnNwYWNlbGluay5jb20vIiwic3ViIjoiV3hGV2Zud2d5MHhpZVhkV3dzNk9xTWlmVjFuRTlFazZAY2xpZW50cyIsImF1ZCI6Imh0dHBzOi8vYXBpbS1lbmctZGV2LWN1cy5henVyZS1hcGkubmV0IiwiaWF0IjoxNzA4MTM4NTY1LCJleHAiOjE3MTA3MzA1NjUsImF6cCI6Ild4RldmbndneTB4aWVYZFd3czZPcU1pZlYxbkU5RWs2Iiwic2NvcGUiOiJpbnNpZ2h0cy5kZW1vIHRyYWZmaWM6cmVhZCBzeXN0ZW06YWRtaW4gaW5zaWdodHM6ZGVtbyBzeXN0ZW06cmVhZCB1c2VyOnJlYWQgYWR2aXNvcnk6cmVhZCByb3V0ZTpjcmVhdGUgYW5vbm9wczpyZWFkIHN1cmZhY2U6Y3JlYXRlIGZsaWdodGxvZzpyZWFkIGludml0ZTpyZWFkIGludml0ZTpjcmVhdGUgaW52aXRlOmRlbGV0ZSBvcmc6cmVhZCByb2xlOnVwZGF0ZSBjcmV3OnVwZGF0ZSBhZHZpc29yeTpjcmVhdGUgYWR2aXNvcnk6dXBkYXRlIGFkdmlzb3J5OmRlbGV0ZSBvcGVyYXRpb246cmVhZCBvcGVyYXRpb246Y3JlYXRlIG9wZXJhdGlvbjp1cGRhdGUgb3BlcmF0aW9uOmRlbGV0ZSBhaXJjcmFmdDpyZWFkIGFpcmNyYWZ0OmNyZWF0ZSBhaXJjcmFmdDp1cGRhdGUgYWlyY3JhZnQ6ZGVsZXRlIGZsaWdodGxvZzpjcmVhdGUgZmxpZ2h0bG9nOnVwZGF0ZSBmbGlnaHRsb2c6ZGVsZXRlIGF2aWF0aW9uOnJlYWQgdXNlcjpkZWxldGUgdXNlcjpyZW1vdmUgYjR1Zmx5OnRlc3RlciB1c2VyLXR5cGU6ZGlyZWN0b3IgdXNlci10eXBlOm1hbmFnZXIgdXNlci10eXBlOm9wZXJhdG9yIGhhemFyOnJlYWQgZWxldmF0aW9uOnJlYWQgd3g6YWR2YW5jZWQ6cmVhZCIsImd0eSI6ImNsaWVudC1jcmVkZW50aWFscyIsInBlcm1pc3Npb25zIjpbImluc2lnaHRzLmRlbW8iLCJ0cmFmZmljOnJlYWQiLCJzeXN0ZW06YWRtaW4iLCJpbnNpZ2h0czpkZW1vIiwic3lzdGVtOnJlYWQiLCJ1c2VyOnJlYWQiLCJhZHZpc29yeTpyZWFkIiwicm91dGU6Y3JlYXRlIiwiYW5vbm9wczpyZWFkIiwic3VyZmFjZTpjcmVhdGUiLCJmbGlnaHRsb2c6cmVhZCIsImludml0ZTpyZWFkIiwiaW52aXRlOmNyZWF0ZSIsImludml0ZTpkZWxldGUiLCJvcmc6cmVhZCIsInJvbGU6dXBkYXRlIiwiY3Jldzp1cGRhdGUiLCJhZHZpc29yeTpjcmVhdGUiLCJhZHZpc29yeTp1cGRhdGUiLCJhZHZpc29yeTpkZWxldGUiLCJvcGVyYXRpb246cmVhZCIsIm9wZXJhdGlvbjpjcmVhdGUiLCJvcGVyYXRpb246dXBkYXRlIiwib3BlcmF0aW9uOmRlbGV0ZSIsImFpcmNyYWZ0OnJlYWQiLCJhaXJjcmFmdDpjcmVhdGUiLCJhaXJjcmFmdDp1cGRhdGUiLCJhaXJjcmFmdDpkZWxldGUiLCJmbGlnaHRsb2c6Y3JlYXRlIiwiZmxpZ2h0bG9nOnVwZGF0ZSIsImZsaWdodGxvZzpkZWxldGUiLCJhdmlhdGlvbjpyZWFkIiwidXNlcjpkZWxldGUiLCJ1c2VyOnJlbW92ZSIsImI0dWZseTp0ZXN0ZXIiLCJ1c2VyLXR5cGU6ZGlyZWN0b3IiLCJ1c2VyLXR5cGU6bWFuYWdlciIsInVzZXItdHlwZTpvcGVyYXRvciIsImhhemFyOnJlYWQiLCJlbGV2YXRpb246cmVhZCIsInd4OmFkdmFuY2VkOnJlYWQiXX0.DiwHAQt5FGrGmbivzRK2WNiqKhzQkVkys0sRhvmGyFNrPX7BW5GSZ91tTSORF_f1gJtDm08gWwKgFUnxd5FjfJmS8Z3AmtTwYzxzMxMU60IpGrQn7DbyEeHiSKoITadWkl--nBpAox8je-x3yccxX6qvdtmHqhiICOJ3lr8b65YWtLudcrQb1ylVeb02uuE9kzeFSfR5CZjCjw92XlkIYPySvYpOsJ1AYW4A6E3YZz_0a1i-2aqbm9sBX6mMcIEZ6sVrXMT14uBP7Z4tpNmLJ9tKM9op-H5Wxysfs_SurFJPNry042ZytW0ihka1efpBKBLp7kt2JcnjVWzFNEFhJQ'
  referer = "www.edancain.com"
  
  headers = {"Content-Type": "application/json", "Authorization": 'Bearer ' + token, "x-api-key": referer}


  response = requests.get(url, headers=headers)

  if response.status_code == 200:
      json_str = json.dumps(response.json(), indent=4)
      print(json_str)
  else:
      print(f"Error: {response.status_code}")


if __name__ == '__main__':
    main()


"""
[
        {
            "name": "Building Footprint",
            "code": "building_footprint",
            "description": "Building footprints from MS repository",
            "source": "Microsoft",
            "tier": 0
        },
        {
            "name": "Population in daytime",
            "code": "population",
            "description": "Population density data binned into h3 hexagons with units of people/mi2",
            "source": "Landscan",
            "tier": 0
        },
        {
            "name": "Roads",
            "code": "roads",
            "description": "OSM dataset of roads including everything between highways and residential roads",
            "source": "OpenStreetMap",
            "tier": 0
        },
        {
            "name": "Dubai Constraints",
            "code": "dubai_constraints",
            "description": "Dubai constraints",
            "source": "Dubai",
            "tier": 0
        },
        {
            "name": "Lidar Obstacles",
            "code": "lidar_obstacles",
            "description": "Hexes of lidar max_agl calculations, output by lidar pipeline",
            "source": "USGS Lidar",
            "tier": 0
        },
        {
            "name": "Dubai Roads Poly",
            "code": "dubai_roads_poly",
            "description": "Dubai road polygons in study area, given to us by dubai customer",
            "source": "Dubai",
            "tier": 0
        },
        {
            "name": "Dubai Lidar Obstacles Hex Res 12",
            "code": "dubai_lidar_obstacles",
            "description": "H3 grid resolutino 12 covering dubai study area.  Hexes contian x/y/z of location/height of lidar point in height with highest AGL",
            "source": "Dubai",
            "tier": 0
        },
        {
            "name": "Dubai Lidar Obstacles > 100ft",
            "code": "dubai_lidar_obstacles_over_100ft",
            "description": "Lidar obstacle hexes only if obstacle AGL is 100ft or more above ground level",
            "source": "Dubai",
            "tier": 0
        },
        {
            "name": "Airspace schedule",
            "code": "airspace_schedule",
            "description": "Controlled airspace schedule for select airports across the country (geometry has no bearing on the result)",
            "source": "FAA",
            "tier": 0
        },
        {
            "name": "Prisons",
            "code": "prisons",
            "description": "Prison locations in the United States",
            "source": "HIFLD",
            "tier": 0
        },
        {
            "name": "Dubai Parks",
            "code": "dubai_parks",
            "description": "Park locations in the Dubai study area.  Provided by dubai customer",
            "source": "Dubai",
            "tier": 0
        },
        {
            "name": "Streams",
            "code": "streams",
            "description": "Stream polylines throughout the United States",
            "source": "USGS",
            "tier": 0
        },
        {
            "name": "Dubai Sport",
            "code": "dubai_sport",
            "description": "Sport locations in the Dubai study area.  Provided by dubai customer",
            "source": "Dubai",
            "tier": 0
        },
        {
            "name": "Dubai Bus Stops",
            "code": "dubai_bus_stops",
            "description": "Bus stop point location in Dubai study area.  Provided by dubai customer",
            "source": "Dubai",
            "tier": 0
        },
        {
            "name": "Balloonports",
            "code": "balloonports",
            "description": "Balloonport points buffered at 1 nautical mile",
            "source": "FAA",
            "tier": 0
        },
        {
            "name": "Daytime population data",
            "code": "population_daytime",
            "description": "Population points that represent an approximate measure of how many people are in a specific area during the day across the United States",
            "source": "Landscan",
            "tier": 0
        },
        {
            "name": "Glideports",
            "code": "glideports",
            "description": "Glideport points buffered at 1 nautical mile",
            "source": "FAA",
            "tier": 0
        },
        {
            "name": "Ultralight",
            "code": "ultralight",
            "description": "Ultralight landing points buffered at 1 nautical mile",
            "source": "FAA",
            "tier": 0
        },
        {
            "name": "Schools",
            "code": "schools",
            "description": "School locations",
            "source": "HIFLD",
            "tier": 0
        },
        {
            "name": "NRHP Location Points",
            "code": "historical_location_points",
            "description": "Historic properties listed on the National Register of Historic Places (points)",
            "source": "NPS",
            "tier": 0
        },
        {
            "name": "State capitol buildings",
            "code": "state_capitol_buildings",
            "description": "Capitol building polygons",
            "source": "HIFLD",
            "tier": 0
        },
        {
            "name": "NRHP Location Polygons",
            "code": "historical_location_polygons",
            "description": "Historic properties listed on the National Register of Historic Places (polygons)",
            "source": "NPS",
            "tier": 0
        },
        {
            "name": "FAA Obstacles",
            "code": "faa_obstacles",
            "description": "Point locations of obstacles",
            "source": "FAA",
            "tier": 0
        },
        {
            "name": "Power Plants",
            "code": "power_plants",
            "description": "Polygons of power plants",
            "source": "HIFLD",
            "tier": 0
        },
        {
            "name": "Military Training Routes",
            "code": "mtr",
            "description": "Polylines of military training routes",
            "source": "FAA",
            "tier": 0
        },
        {
            "name": "Bridges",
            "code": "bridges",
            "description": "Bridges in the United States",
            "source": "HIFLD",
            "tier": 0
        },
        {
            "name": "Population Night",
            "code": "population_nighttime",
            "description": "Population points that represent an approximate measure of how many people are in a specific area during the day across the United States",
            "source": "FAA",
            "tier": 0
        },
        {
            "name": "Dubai Building Footprint",
            "code": "dubai_building_footprint",
            "description": "Dubai building footprints in study area given to us by dubai customer",
            "source": "Dubai",
            "tier": 0
        },
        {
            "name": "Dubai Helipad",
            "code": "dubai_helipad",
            "description": "Helipad locations in the Dubai study area.  Provided by dubai customer",
            "source": "Dubai",
            "tier": 0
        },
        {
            "name": "Dubai Master Plan Residential",
            "code": "dubai_master_plan_residential",
            "description": "Dubai master plan residential locations",
            "source": "Dubai",
            "tier": 0
        },
        {
            "name": "Dubai Master Plan",
            "code": "dubai_master_plan",
            "description": "Dubai master plan polygons given to us by dubai customer",
            "source": "Dubai",
            "tier": 0
        },
        {
            "name": "Dubai Trees",
            "code": "dubai_trees",
            "description": "Some trees in the Dubai study area.  not a complete count of all trees.  Provided by dubai customer",
            "source": "Dubai",
            "tier": 0
        },
        {
            "name": "Veteran health facilities",
            "code": "veteran_health_facilities",
            "description": "Health facility polygons for United States veterans of the armed forces",
            "source": "HIFLD",
            "tier": 0
        },
        {
            "name": "Helipads",
            "code": "helipads",
            "description": "Helipad locations throughout the United States",
            "source": "FAA",
            "tier": 0
        },
        {
            "name": "Bodies of water",
            "code": "water_bodies",
            "description": "General bodies of water in the United States",
            "source": "USGS",
            "tier": 0
        },
        {
            "name": "Child Care Centers",
            "code": "child_care_center",
            "description": "Child Care Centers in the United States",
            "source": "HIFLD",
            "tier": 0
        },
        {
            "name": "Railroad lines",
            "code": "railroad_lines",
            "description": "Railroad network of the United States",
            "source": "HIFLD",
            "tier": 0
        },
        {
            "name": "Parks",
            "code": "parks",
            "description": "Parks throughout the United States",
            "source": "HIFLD",
            "tier": 0
        },
        {
            "name": "Hazards",
            "code": "hazards",
            "description": "Hazards contain various types of infrastructure",
            "source": "Airspace Link",
            "tier": 0
        },
        {
            "name": "Landscan Night Polygon",
            "code": "landscan_night_polygon",
            "description": "Population points that represent an approximate measure of how many people are in a specific area during the night across the United States",
            "source": "Landscan",
            "tier": 0
        },
        {
            "name": "Landscan Day Polygon",
            "code": "landscan_day_polygon",
            "description": "Population points that represent an approximate measure of how many people are in a specific area during the day across the United States",
            "source": "Landscan",
            "tier": 0
        },
        {
            "name": "Convention centers and fairgrounds",
            "code": "convention_centers_and_fairgrounds",
            "description": "Locations of convention centers, conference centers, exposition centers, and fairgrounds for the 50 U.S. states, D.C., and the territory of Puerto Rico",
            "source": "HIFLD",
            "tier": 0
        },
        {
            "name": "Courthouses",
            "code": "courthouses",
            "description": "Courthouses across the United States",
            "source": "HIFLD",
            "tier": 0
        },
        {
            "name": "Special Flight Rules Area",
            "code": "sfra",
            "description": "Designated regions where special air traffic rules apply",
            "source": "FAA",
            "tier": 0
        },
        {
            "name": "Electric substations",
            "code": "electric_substations",
            "description": "Electric substations dispersed throughout the United States",
            "source": "HIFLD",
            "tier": 0
        },
        {
            "name": "EMS stations",
            "code": "ems_stations",
            "description": "Emergency Medical Service (EMS) stations throughout the United States",
            "source": "HIFLD",
            "tier": 0
        },
        {
            "name": "Fire stations",
            "code": "fire_stations",
            "description": "Fire stations throughout the United States",
            "source": "HIFLD",
            "tier": 0
        },
        {
            "name": "Government buildings",
            "code": "government_buildings",
            "description": "Government buildings throughout the United States",
            "source": "HIFLD",
            "tier": 0
        },
        {
            "name": "Hospitals",
            "code": "hospitals",
            "description": "Hospital locations throughout the United States",
            "source": "HIFLD",
            "tier": 0
        },
        {
            "name": "Military facilities",
            "code": "military_facilities",
            "description": "Military base locations in the United States",
            "source": "HIFLD",
            "tier": 0
        },
        {
            "name": "Police stations",
            "code": "police_stations",
            "description": "Police station locations",
            "source": "HIFLD",
            "tier": 0
        },
        {
            "name": "Sport venues",
            "code": "sport_venues",
            "description": "Sport venue locations",
            "source": "HIFLD",
            "tier": 0
        },
        {
            "name": "Transmission lines",
            "code": "transmission_lines",
            "description": "High-voltage electric lines",
            "source": "HIFLD",
            "tier": 0
        },
        {
            "name": "Controlled Airspace Classification",
            "code": "controlled_airspace",
            "description": "Airspace that is under FAA control",
            "source": "FAA",
            "tier": 0
        },
        {
            "name": "Special use airspace",
            "code": "sua",
            "description": "Special use airspace contains both prohibited and restricted airspace; see https://www.faa.gov/air_traffic/publications/atpubs/aim_html/chap3_section_4.html for more details",
            "source": "FAA",
            "tier": 0
        },
        {
            "name": "Colleges and universities",
            "code": "colleges_universities",
            "description": "Campus grounds for universities and colleges throughout the US",
            "source": "HIFLD",
            "tier": 0
        },
        {
            "name": "Urgent care facilities",
            "code": "urgent_care",
            "description": "Urgent care facilities dispersed throughout the United States",
            "source": "HIFLD",
            "tier": 0
        },
        {
            "name": "Wind farms",
            "code": "wind_farms",
            "description": "Polygons representing coverage of individual wind turbines",
            "source": "USGS",
            "tier": 0
        },
        {
            "name": "National Parks",
            "code": "national_parks",
            "description": "Polygons of national parks",
            "source": "NPS",
            "tier": 0
        },
        {
            "name": "Railroad bridge overpass",
            "code": "railroad_overpass",
            "description": "Railroad bridges that cross over roads",
            "source": "HIFLD",
            "tier": 0
        },
        {
            "name": "FCC Antenna Structures",
            "code": "fcc_asr",
            "description": "Antenna structures from the ASR dataset maintained by the FCC",
            "source": "FCC",
            "tier": 0
        },
        {
            "name": "Emergency operation centers",
            "code": "eocs",
            "description": "Emergency Operation Centers (EOCs)",
            "source": "HIFLD",
            "tier": 0
        },
        {
            "name": "ZIP codes",
            "code": "zip_codes",
            "description": "ZIP code regions breakdown in the United States",
            "source": "US Census Bureau",
            "tier": 0
        },
        {
            "name": "Landscan Night Point",
            "code": "landscan_night_point",
            "description": "Population points that represent an approximate measure of how many people are in a specific area during the night across the United States",
            "source": "Landscan",
            "tier": 0
        },
        {
            "name": "Landscan Day Point",
            "code": "landscan_day_point",
            "description": "Population points that represent an approximate measure of how many people are in a specific area during the day across the United States",
            "source": "Landscan",
            "tier": 0
        },
        {
            "name": "UAS Facility Management Flight Ceiling Primary",
            "code": "uasfm_ceiling_primary",
            "description": "Maximum altitude features surrounding airports where the FAA enables operations (primary)",
            "source": "FAA",
            "tier": 0
        },
        {
            "name": "UAS Facility Management Flight Ceiling Secondary",
            "code": "uasfm_ceiling_secondary",
            "description": "Maximum altitude features surrounding airports where the FAA enables operations (secondary)",
            "source": "FAA",
            "tier": 0
        },
        {
            "name": "US Building Footprints",
            "code": "building_footprints",
            "description": "Polygon dataset for US building footprints",
            "source": "Microsoft",
            "tier": 0
        },
        {
            "name": "Railroad bridges",
            "code": "railroad_bridges",
            "description": "All railroad bridges in the United States",
            "source": "HIFLD",
            "tier": 0
        },
        {
            "name": "Slope",
            "code": "slope",
            "description": "Slope - Steepness of raster cell derived from USGS 1/3 arcsec DEM for United States",
            "source": "USGS",
            "tier": 0
        },
        {
            "name": "Terrain Ruggedness Index",
            "code": "tri",
            "description": "Terrain Ruggedness Index (TRI) - elevation difference between adjacent raster cells derived from USGS 1/3 arcsec DEM for United States",
            "source": "USGS",
            "tier": 0
        },
        {
            "name": "Digital elevation model",
            "code": "dem_ft",
            "description": "CONUS digital elevation model in ft",
            "source": "USGS",
            "tier": 0
        },
        {
            "name": "Land use land cover",
            "code": "lulc",
            "description": "Land use land cover data binned into h3 hexagons with english labels applied",
            "source": "USGS",
            "tier": 0
        },
        {
            "name": "Airports",
            "code": "airports",
            "description": "Points designated for landing or takeoff",
            "source": "FAA",
            "tier": 0
        },
        {
            "name": "Community advisories",
            "code": "community_advisories",
            "description": "Advisories are areas of airspace in which governments seek to alert pilots of additional risk",
            "source": "Airspace Link",
            "tier": 0
        },
        {
            "name": "Class Airspace Schedule",
            "code": "class_airspace_schedule",
            "description": "Class Airspace Schedule (Airspace schedule joined with FAA Class Airpace dataset)",
            "source": "FAA",
            "tier": 0
        },
        {
            "name": "Point Helipad Locations",
            "code": "faa_helipads",
            "description": "Helipad locations throughout the United States from FAA (points)",
            "source": "FAA",
            "tier": 0
        },
        {
            "name": "Military Training Routes Buffer",
            "code": "mtr_buffer",
            "description": "Buffered Polylines of military training routes",
            "source": "FAA",
            "tier": 0
        },
        {
            "name": "National Parks Simplified",
            "code": "national_parks_simple",
            "description": "Simplified polygons of national parks",
            "source": "NPS",
            "tier": 0
        },
        {
            "name": "Notams",
            "code": "notams",
            "description": "Notice to Airmen (includes drotams) - specific to drone operations (under 400 ft)",
            "source": "FAA",
            "tier": 0
        },
        {
            "name": "Full Time National Security UAS Flight Restriction",
            "code": "nsufr_ft",
            "description": "Any full time flight restriction, created for national security purposes",
            "source": "FAA",
            "tier": 0
        },
        {
            "name": "Part Time National Security UAS Flight Restriction",
            "code": "nsufr_pt",
            "description": "Any part time flight restriction, created for national security purposes",
            "source": "FAA",
            "tier": 0
        },
        {
            "name": "Recreational Flyer Fixed Sites",
            "code": "recreational_flyer_fixed_sites",
            "description": "Active flying fields that are established by an agreement with the FAA",
            "source": "FAA",
            "tier": 0
        },
        {
            "name": "Part 93 Special Air Traffic Rules",
            "code": "satr",
            "description": "B4UFLY Special Air Traffic Rules",
            "source": "FAA",
            "tier": 0
        },
        {
            "name": "Seaport",
            "code": "seaport",
            "description": "Seaport points",
            "source": "FAA",
            "tier": 0
        },
        {
            "name": "Sporting Temporary Flight Restrictions",
            "code": "sporting_tfr",
            "description": "Temporary Flight Restrictions imposed by the FAA to restrict aircraft operations within designated areas where sporting events are taking place",
            "source": "FAA",
            "tier": 0
        },
        {
            "name": "Stadium",
            "code": "stadium",
            "description": "Select stadiums containing temporary flight restriction. The stadium points are buffered by 3 nautical miles",
            "source": "FAA",
            "tier": 0
        },
        {
            "name": "SUA Schedule",
            "code": "sua_schedule",
            "description": "Special Use Airspace Schedule",
            "source": "FAA",
            "tier": 0
        },
        {
            "name": "Temporary flight restrictions",
            "code": "tfr",
            "description": "Temporary Flight Restrictions imposed by the FAA to restrict aircraft operations within designated areas",
            "source": "FAA",
            "tier": 0
        },
        {
            "name": "UAS Facility Management Flight Ceiling",
            "code": "uasfm_ceiling",
            "description": "Maximum altitude features surrounding airports where the FAA enables operations",
            "source": "FAA",
            "tier": 0
        },
        {
            "name": "Washington DC Flight Restricted Zone",
            "code": "washington_frz",
            "description": "The prohibited flight restriction zone around the capitol",
            "source": "FAA",
            "tier": 0
        }
    ]
}
"""
