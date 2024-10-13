#!/usr/bin/env python

import uuid
import requests
import json
from AirspaceLink_API.advisories import Geometry, GeometryType


class Operation_Properties:
    def __init__(self, operationName: str, category: str, startTime: str, timezoneName: str, duration: int, maxAltitude: float, fixedAltitude: bool, callbackUrl: str):
        self.operationName = operationName
        self.category = category
        self.startTime = startTime
        self.timezoneName = timezoneName
        self.duration = duration
        self.maxAltitude = maxAltitude
        self.fixedAltitude = fixedAltitude
        self.callbackUrl = callbackUrl

    def to_json(self):
        return {
            "operationName": self.operationName,
            "category": self.category,
            "startTime": self.startTime,
            "timezoneName": self.timezoneName,
            "duration": self.duration,
            "maxAltitude": self.maxAltitude,
            "fixedAltitude": self.fixedAltitude,
            "callbackUrl": self.callbackUrl
        }


class Operational_Feature:
    def __init__(self, operational_type: str, properties: Operation_Properties, geometry: Geometry):
        self.type = operational_type,
        self.geometry = geometry
        self.properties = properties
    

    def to_json(self):        
        return {
            "type": "Feature",
            "properties": self.properties.to_json(),
            "geometry": {
                "type": self.geometry.type,
                "coordinates": [self.geometry.coordinates]
            }
        }


class Operation:
    def __init__(self, api_key, token):
        self.api_key = api_key
        self.token = token

    def request_operation(self, feature: Operational_Feature ):

        try:
            header = {"Content-Type": "application/json;charset=UTF-8", 'Authorization': 'Bearer ' + self.token,
                        "x-api-key": self.api_key}
            data = feature.to_json()

            data = json.dumps(data)
            response = requests.post(
                url='https://airhub-api-dev.airspacelink.com/v2/operation',  
                headers=header,
                data=data
            )

            response_data = response.json()
            print(response_data) 
            # {'statusCode': 401, 'message': 'Access denied due to invalid subscription key. Make sure to provide a valid key for an active subscription.'}
            # {'statusCode': 400, 'message': 'parsing time "2024-01-23 23:59:43.404671" as "2006-01-02T15:04:05Z07:00": cannot parse " 23:59:43.404671" as "T"'}

            url = response_data["data"]["url"]
            return response_data
        except Exception as ex:
            print(ex)


# TEST
if __name__ == '__main__':
    # Create instances of Operational_Feature and Operation_Properties
    # Generate a unique ID for the operation
    operation_id = str(uuid.uuid4())
    # Prepare the callback URL with the unique ID
    _callback_url = f"https://78bc-2406-2d40-72ab-5910-902-dee6-d0a0-af4c.ngrok-free.app/{operation_id}"

    operation_properties = Operation_Properties(
        operationName="test",
        category="faa_107",
        startTime="2023-01-01T12:00:00Z",
        timezoneName="America/New_York",
        duration=55,
        maxAltitude=100,
        fixedAltitude=True,
        callbackUrl = _callback_url
    )

    geometry = Geometry(geometry_type=GeometryType.POLYGON, coordinates=[[-77.83744812011719, 40.676211751311484],
                                                             [-77.82714843749999, 40.676211751311484],
                                                             [-77.82714843749999, 40.683241578458706],
                                                             [-77.83744812011719, 40.683241578458706],
                                                             [-77.83744812011719, 40.676211751311484]])

    operational_feature = Operational_Feature(geometry=geometry, properties=operation_properties, operational_type="Feature")

    api_key = "f15b282e5bd6495eae4cafe2d42b72e5"
    token = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ild3dDk2SlJDTE9ER1pEeEpiRVVxdSJ9.eyJodHRwczovL2Fpcmh1Yi5haXJzcGFjZWxpbmsuY29tL3V0bSI6InZhbnRpcyIsImlzcyI6Imh0dHBzOi8vaWQtZGV2LmFpcnNwYWNlbGluay5jb20vIiwic3ViIjoiV3hGV2Zud2d5MHhpZVhkV3dzNk9xTWlmVjFuRTlFazZAY2xpZW50cyIsImF1ZCI6Imh0dHBzOi8vYXBpbS1lbmctZGV2LWN1cy5henVyZS1hcGkubmV0IiwiaWF0IjoxNzA4MTM4NTY1LCJleHAiOjE3MTA3MzA1NjUsImF6cCI6Ild4RldmbndneTB4aWVYZFd3czZPcU1pZlYxbkU5RWs2Iiwic2NvcGUiOiJpbnNpZ2h0cy5kZW1vIHRyYWZmaWM6cmVhZCBzeXN0ZW06YWRtaW4gaW5zaWdodHM6ZGVtbyBzeXN0ZW06cmVhZCB1c2VyOnJlYWQgYWR2aXNvcnk6cmVhZCByb3V0ZTpjcmVhdGUgYW5vbm9wczpyZWFkIHN1cmZhY2U6Y3JlYXRlIGZsaWdodGxvZzpyZWFkIGludml0ZTpyZWFkIGludml0ZTpjcmVhdGUgaW52aXRlOmRlbGV0ZSBvcmc6cmVhZCByb2xlOnVwZGF0ZSBjcmV3OnVwZGF0ZSBhZHZpc29yeTpjcmVhdGUgYWR2aXNvcnk6dXBkYXRlIGFkdmlzb3J5OmRlbGV0ZSBvcGVyYXRpb246cmVhZCBvcGVyYXRpb246Y3JlYXRlIG9wZXJhdGlvbjp1cGRhdGUgb3BlcmF0aW9uOmRlbGV0ZSBhaXJjcmFmdDpyZWFkIGFpcmNyYWZ0OmNyZWF0ZSBhaXJjcmFmdDp1cGRhdGUgYWlyY3JhZnQ6ZGVsZXRlIGZsaWdodGxvZzpjcmVhdGUgZmxpZ2h0bG9nOnVwZGF0ZSBmbGlnaHRsb2c6ZGVsZXRlIGF2aWF0aW9uOnJlYWQgdXNlcjpkZWxldGUgdXNlcjpyZW1vdmUgYjR1Zmx5OnRlc3RlciB1c2VyLXR5cGU6ZGlyZWN0b3IgdXNlci10eXBlOm1hbmFnZXIgdXNlci10eXBlOm9wZXJhdG9yIGhhemFyOnJlYWQgZWxldmF0aW9uOnJlYWQgd3g6YWR2YW5jZWQ6cmVhZCIsImd0eSI6ImNsaWVudC1jcmVkZW50aWFscyIsInBlcm1pc3Npb25zIjpbImluc2lnaHRzLmRlbW8iLCJ0cmFmZmljOnJlYWQiLCJzeXN0ZW06YWRtaW4iLCJpbnNpZ2h0czpkZW1vIiwic3lzdGVtOnJlYWQiLCJ1c2VyOnJlYWQiLCJhZHZpc29yeTpyZWFkIiwicm91dGU6Y3JlYXRlIiwiYW5vbm9wczpyZWFkIiwic3VyZmFjZTpjcmVhdGUiLCJmbGlnaHRsb2c6cmVhZCIsImludml0ZTpyZWFkIiwiaW52aXRlOmNyZWF0ZSIsImludml0ZTpkZWxldGUiLCJvcmc6cmVhZCIsInJvbGU6dXBkYXRlIiwiY3Jldzp1cGRhdGUiLCJhZHZpc29yeTpjcmVhdGUiLCJhZHZpc29yeTp1cGRhdGUiLCJhZHZpc29yeTpkZWxldGUiLCJvcGVyYXRpb246cmVhZCIsIm9wZXJhdGlvbjpjcmVhdGUiLCJvcGVyYXRpb246dXBkYXRlIiwib3BlcmF0aW9uOmRlbGV0ZSIsImFpcmNyYWZ0OnJlYWQiLCJhaXJjcmFmdDpjcmVhdGUiLCJhaXJjcmFmdDp1cGRhdGUiLCJhaXJjcmFmdDpkZWxldGUiLCJmbGlnaHRsb2c6Y3JlYXRlIiwiZmxpZ2h0bG9nOnVwZGF0ZSIsImZsaWdodGxvZzpkZWxldGUiLCJhdmlhdGlvbjpyZWFkIiwidXNlcjpkZWxldGUiLCJ1c2VyOnJlbW92ZSIsImI0dWZseTp0ZXN0ZXIiLCJ1c2VyLXR5cGU6ZGlyZWN0b3IiLCJ1c2VyLXR5cGU6bWFuYWdlciIsInVzZXItdHlwZTpvcGVyYXRvciIsImhhemFyOnJlYWQiLCJlbGV2YXRpb246cmVhZCIsInd4OmFkdmFuY2VkOnJlYWQiXX0.DiwHAQt5FGrGmbivzRK2WNiqKhzQkVkys0sRhvmGyFNrPX7BW5GSZ91tTSORF_f1gJtDm08gWwKgFUnxd5FjfJmS8Z3AmtTwYzxzMxMU60IpGrQn7DbyEeHiSKoITadWkl--nBpAox8je-x3yccxX6qvdtmHqhiICOJ3lr8b65YWtLudcrQb1ylVeb02uuE9kzeFSfR5CZjCjw92XlkIYPySvYpOsJ1AYW4A6E3YZz_0a1i-2aqbm9sBX6mMcIEZ6sVrXMT14uBP7Z4tpNmLJ9tKM9op-H5Wxysfs_SurFJPNry042ZytW0ihka1efpBKBLp7kt2JcnjVWzFNEFhJQ'
        
    operation = Operation(api_key, token)
    response = operation.request_operation(operational_feature)
    print(response)
'''
'{
    "type": "Feature",
    "properties": {"operationName": "test", "category": "faa_107", "startTime": "2023-01-01T12:00:00Z", "timezoneName": "America/New_York", "duration": 55, "maxAltitude": 100},
    "geometry": {"type": "Polygon", "coordinates": [[[-77.83744812011719,40.676211751311484],[-77.82714843749999,40.676211751311484],[-77.82714843749999,40.683241578458706],[-77.83744812011719,40.683241578458706],[-77.83744812011719,40.676211751311484]]]}
  }'
'''