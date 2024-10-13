#!/usr/bin/env python
import requests
import json
from enum import Enum

class Feature:
    def __init__(self, geometry, properties):
        self.geometry = geometry
        self.properties = properties


class GeometryType(Enum):
    POINT = "Point"
    LINE_STRING = "LineString"
    POLYGON = "Polygon"
    MULTI_POINT = "MultiPoint"
    MULTI_LINE_STRING = "MultiLineString"


class Geometry:
    def __init__(self, geometry_type : GeometryType, coordinates):
        self.coordinates = coordinates
        self.type = geometry_type.value
        

    def to_json(self):
        # return json.dumps(self.__dict__)
        return {"type": self.type, "coordinates": self.coordinates}


class PointGeometry(Geometry):
    def __init__(self, coordinates):
        super().__init__(GeometryType.POINT, coordinates)


class LineStringGeometry(Geometry):
    def __init__(self, coordinates):
        super().__init__(GeometryType.LINE_STRING, coordinates)

class MultiLineString(Geometry):
    def __init__(self,  coordinates):
        super().__init__(GeometryType.MULTI_LINE_STRING, coordinates)


class PolygonGeometry(Geometry):
    def __init__(self, coordinates):
        super().__init__(GeometryType.POLYGON, coordinates)


class MultiPointGeometry(Geometry):
    def __init__(self, coordinates):
        super().__init__(GeometryType.MULTI_POINT, coordinates)


class Waypoints(Geometry):  #RouteV2
    def __init__(self, coordinates):
        super().__init__(GeometryType.MULTI_POINT, coordinates)

class BoundingBox:
    def __init__(self, min_longitude, min_latitude, max_longitude, max_latitude):
        self.coordinates = [min_longitude, min_latitude, max_longitude, max_latitude]

    def to_json(self):
        return json.dumps({
            "bbox": self.coordinates
        })
 

class Properties:
    def __init__(self, advisoryCategory, altitudeLower, altitudeUpper, createdBy, endTime, geoID, id, lastEditedBy, name, published, startTime, timezoneName, version):
        self.advisoryCategory = advisoryCategory
        self.altitudeLower = altitudeLower
        self.altitudeUpper = altitudeUpper
        self.createdBy = createdBy
        self.endTime = endTime
        self.geoID = geoID
        self.id = id
        self.lastEditedBy = lastEditedBy
        self.name = name
        self.published = published
        self.startTime = startTime
        self.timezoneName = timezoneName
        self.version = version


# https://developers.airspacelink.com/#advisories-get-advisories
class Advisories:

    def __init__(self, api_key, token):
        self.__api_key = api_key
        self.__token = token

    def request_advisory(self, geometry: Geometry, altitudeUpper, altitudeLower, startTime, endTime, geoIDs: [], boundingBox: BoundingBox) -> list[Feature]:

        try:
            # Find advisories that intersect the input geometry.
            headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + self.__token,
                       'x-api-key': self.__api_key}
            
            data = None
            response = None

            # two types of request. One takes a geometry "POST", the other a bounding box "GET"
            if geometry is not None:
                data = {
                    'geometry': geometry.to_json(),
                    "altitudeUpper": altitudeUpper, # 500
                    "altitudeLower": altitudeLower, # -100
                    "startTime": startTime, # "2022-06-01T23:39:00Z"
                    "endTime": endTime, # "2022-06-30T23:39:00Z"
                    "geoIDs": geoIDs # ["1300021", "13"]
                }

                response = requests.post(
                url="https://airhub-api-sandbox.airspacelink.com/v4/advisory/query", 
                headers=headers,
                data=json.dumps(data)
            )

            if boundingBox is not None:
                data = {
                    "bbox": boundingBox.to_json(), 
                    "altitudeUpper": altitudeUpper, # 500
                    "altitudeLower": altitudeLower, # -100
                    "startTime": startTime, # "2022-06-01T23:39:00Z"
                    "endTime": endTime, # "2022-06-30T23:39:00Z"
                    "geoIDs": geoIDs # ["1300021", "13"]
                }

                response = requests.get(
                url="https://airhub-api-sandbox.airspacelink.com/v4/advisory/query", 
                headers=headers,
                data=json.dumps(data)
            )

            response_data = response.json()
            data_features = response_data['data']['features']

            features = []
            for feature_data in data_features:
                geometry_data = feature_data["geometry"]
                properties_data = feature_data["properties"]
                geometry = Geometry(geometry_data["type"], geometry_data["coordinates"])
                properties = Properties(**properties_data)

                feature = Feature(geometry, properties)
                features.append(feature)

            return features
        except Exception as ex:
            print('HTTP Request failed: %s' % ex)
            return 'HTTP Request failed'



