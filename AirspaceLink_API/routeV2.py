#!/usr/bin/env python

import requests
import json
from AirspaceLink_API.advisories import MultiPointGeometry, PolygonGeometry, MultiLineString, LineStringGeometry
from AirspaceLink_API.layer import Layer, Layers
from AirspaceLink_API.UberH3 import GetH3

from flask import Flask, g, jsonify
import threading
import logging

# Configure logging level and format
logging.basicConfig(level=logging.INFO)

class RouteV2Response:
    def __init__(self, data) -> None:
        self.status_code = data["statusCode"]
        self.message = data["message"]
        self.corridor = data["data"]["corridor"]
        self.network = MultiLineString(data["data"]["network"]["coordinates"])
        self.path = LineStringGeometry(data["data"]["path"]["coordinates"])
        self.hex_geojson = self.build_hex_geojson()

    def build_hex_geojson(self):
        hex_geojson_collection = []
        for hex_id in self.corridor:
            hex_geojson = GetH3.get_hex_geojson_from_h3(hex_id)
            if hex_geojson:
                hex_geojson_collection.append(hex_geojson)
        return hex_geojson_collection

    def to_json(self):
        response_data = {
            "statusCode": self.status_code,
            "message": self.message,
            "data": {
                "corridor": self.corridor,
                "network": {
                    "type": "MultiLineString",
                    "coordinates": self.network.coordinates
                },
                "path": {
                    "type": "LineString",
                    "coordinates": self.path.coordinates
                }
            },
            "hex_geojson": self.hex_geojson
        }
        return json.dumps(response_data)

class RouteV2Request:
    def __init__(self, api_key, token):
        self.__token = token
        self.__api_key = api_key
        self.lock = threading.Lock()

    def request_route(self, resolution: int = 10, layers = [], multipoint: MultiPointGeometry = None) -> RouteV2Response:
        if resolution == 1 or resolution > 11:
            resolution = 10

        try:
            
            header = {"Content-Type": "application/json", "Authorization": 'Bearer ' + self.__token, "x-api-key": self.__api_key}

            data = {
                "resolution": resolution, 
                "layers": layers.to_json(),
                "waypoints": multipoint.to_json()
            }
            
            data = json.dumps(data)

            response_data = "" 
            try:
                with self.lock:
                    response = requests.post(
                        url="https://airhub-api-dev.airspacelink.com/v2/route", 
                        headers=header,
                        data=data,
                        timeout=10  
                    )
                
                if response.status_code >= 500:
                    if resolution > 2:
                        self.request_route(resolution - 1, layers, multipoint)

                response_data = response.json()

            except requests.Timeout:
                print("Request timed out. Please try again later.")
                logging.error("Request timed out. Please try again later.")
            except requests.RequestException as e:
                print(f"An error occurred: {e}")
                logging.error(f"An error occurred: {e}")
                return None

            
            if response_data is not None:
                # self.test_route()
                routeV2Response = RouteV2Response(response_data)
                print(routeV2Response.to_json())
                return routeV2Response
            else:
                return None

        except Exception as ex:
            print('HTTP Request failed: %s' % ex)
            # Assuming response_data.message and response_data.statusCode contain the necessary data
            error_message = "HTTP Request failed: {}".format(response_data["message"])
            status_code = response_data["statusCode"]

            # Creating a dictionary to represent the data
            error_data = {
                "error": error_message,
                "status_code": status_code
            }

            # Converting the dictionary to a JSON string
            json_string = json.dumps(error_data)

            # Returning the JSON string
            return json_string

    def test_route(self):
        # Define the data and headers
        data = {
            "resolution": 5,
            "layers": [
                {"code": "helipads", "risk": 10},
                {"code": "urgent_care", "risk": 10},
                {"code": "sport_venues", "risk": 10},
                {"code": "police_stations", "risk": 10},
                {"code": "hospitals", "risk": 10},
                {"code": "schools", "risk": 10},
                {"code": "airports", "risk": 10}
            ],
            "waypoints": {
                "type": "MultiPoint",
                "coordinates": [
                    [-119.99798534584185, 38.91917451008874],
                    [-119.99970467184161, 38.93231266680202],
                    [-120.00480823415485, 38.936608890355465],
                    [-120.00782069536075, 38.93393930753754],
                    [-120.0132254864385, 38.93639687232849],
                    [-119.99798534584185, 38.91917451008874]
                ]
            }
        }
        
        # data = {"resolution": 5, "layers": [{"code": "helipads", "risk": 10}, {"code": "urgent_care", "risk": 10}, {"code": "sport_venues", "risk": 10}, {"code": "police_stations", "risk": 10}, {"code": "hospitals", "risk": 10}, {"code": "schools", "risk": 10}, {"code": "airports", "risk": 10}], "waypoints": {"type": "MultiPoint", "coordinates": [[-119.99798534584185, 38.91917451008874], [-119.99970467184161, 38.93231266680202], [-120.00480823415485, 38.936608890355465], [-120.00782069536075, 38.93393930753754], [-120.0132254864385, 38.93639687232849], [-119.99798534584185, 38.91917451008874]]}}
        data = json.dumps(data)

        header = {
            "Content-Type": "application/json",
            "Authorization": 'Bearer ' + self.__token,
            "x-api-key": self.__api_key
        }

        try:
            # Make the request
            response = requests.post(
                url="https://airhub-api-dev.airspacelink.com/v2/route",
                headers=header,
                data=data,
                timeout=10
            )

            # Check if the request was successful
            if response.ok:
                response_data = response.json()
                print(json.dumps(response_data, indent=2))  # Print the response for debugging
                return response_data, 200
            else:
                print("Error: {}".format(response.status_code))  # Print error for debugging
                return "Error: {}".format(response.status_code), response.status_code

        except requests.RequestException as e:
            print("An error occurred: {}".format(e))  # Print error for debugging
            return "An error occurred: {}".format(e), 500
        
    

if __name__ == '__main__':
    token = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ild3dDk2SlJDTE9ER1pEeEpiRVVxdSJ9.eyJodHRwczovL2Fpcmh1Yi5haXJzcGFjZWxpbmsuY29tL3V0bSI6InZhbnRpcyIsImlzcyI6Imh0dHBzOi8vaWQtZGV2LmFpcnNwYWNlbGluay5jb20vIiwic3ViIjoiV3hGV2Zud2d5MHhpZVhkV3dzNk9xTWlmVjFuRTlFazZAY2xpZW50cyIsImF1ZCI6Imh0dHBzOi8vYXBpbS1lbmctZGV2LWN1cy5henVyZS1hcGkubmV0IiwiaWF0IjoxNzA4MTM4NTY1LCJleHAiOjE3MTA3MzA1NjUsImF6cCI6Ild4RldmbndneTB4aWVYZFd3czZPcU1pZlYxbkU5RWs2Iiwic2NvcGUiOiJpbnNpZ2h0cy5kZW1vIHRyYWZmaWM6cmVhZCBzeXN0ZW06YWRtaW4gaW5zaWdodHM6ZGVtbyBzeXN0ZW06cmVhZCB1c2VyOnJlYWQgYWR2aXNvcnk6cmVhZCByb3V0ZTpjcmVhdGUgYW5vbm9wczpyZWFkIHN1cmZhY2U6Y3JlYXRlIGZsaWdodGxvZzpyZWFkIGludml0ZTpyZWFkIGludml0ZTpjcmVhdGUgaW52aXRlOmRlbGV0ZSBvcmc6cmVhZCByb2xlOnVwZGF0ZSBjcmV3OnVwZGF0ZSBhZHZpc29yeTpjcmVhdGUgYWR2aXNvcnk6dXBkYXRlIGFkdmlzb3J5OmRlbGV0ZSBvcGVyYXRpb246cmVhZCBvcGVyYXRpb246Y3JlYXRlIG9wZXJhdGlvbjp1cGRhdGUgb3BlcmF0aW9uOmRlbGV0ZSBhaXJjcmFmdDpyZWFkIGFpcmNyYWZ0OmNyZWF0ZSBhaXJjcmFmdDp1cGRhdGUgYWlyY3JhZnQ6ZGVsZXRlIGZsaWdodGxvZzpjcmVhdGUgZmxpZ2h0bG9nOnVwZGF0ZSBmbGlnaHRsb2c6ZGVsZXRlIGF2aWF0aW9uOnJlYWQgdXNlcjpkZWxldGUgdXNlcjpyZW1vdmUgYjR1Zmx5OnRlc3RlciB1c2VyLXR5cGU6ZGlyZWN0b3IgdXNlci10eXBlOm1hbmFnZXIgdXNlci10eXBlOm9wZXJhdG9yIGhhemFyOnJlYWQgZWxldmF0aW9uOnJlYWQgd3g6YWR2YW5jZWQ6cmVhZCIsImd0eSI6ImNsaWVudC1jcmVkZW50aWFscyIsInBlcm1pc3Npb25zIjpbImluc2lnaHRzLmRlbW8iLCJ0cmFmZmljOnJlYWQiLCJzeXN0ZW06YWRtaW4iLCJpbnNpZ2h0czpkZW1vIiwic3lzdGVtOnJlYWQiLCJ1c2VyOnJlYWQiLCJhZHZpc29yeTpyZWFkIiwicm91dGU6Y3JlYXRlIiwiYW5vbm9wczpyZWFkIiwic3VyZmFjZTpjcmVhdGUiLCJmbGlnaHRsb2c6cmVhZCIsImludml0ZTpyZWFkIiwiaW52aXRlOmNyZWF0ZSIsImludml0ZTpkZWxldGUiLCJvcmc6cmVhZCIsInJvbGU6dXBkYXRlIiwiY3Jldzp1cGRhdGUiLCJhZHZpc29yeTpjcmVhdGUiLCJhZHZpc29yeTp1cGRhdGUiLCJhZHZpc29yeTpkZWxldGUiLCJvcGVyYXRpb246cmVhZCIsIm9wZXJhdGlvbjpjcmVhdGUiLCJvcGVyYXRpb246dXBkYXRlIiwib3BlcmF0aW9uOmRlbGV0ZSIsImFpcmNyYWZ0OnJlYWQiLCJhaXJjcmFmdDpjcmVhdGUiLCJhaXJjcmFmdDp1cGRhdGUiLCJhaXJjcmFmdDpkZWxldGUiLCJmbGlnaHRsb2c6Y3JlYXRlIiwiZmxpZ2h0bG9nOnVwZGF0ZSIsImZsaWdodGxvZzpkZWxldGUiLCJhdmlhdGlvbjpyZWFkIiwidXNlcjpkZWxldGUiLCJ1c2VyOnJlbW92ZSIsImI0dWZseTp0ZXN0ZXIiLCJ1c2VyLXR5cGU6ZGlyZWN0b3IiLCJ1c2VyLXR5cGU6bWFuYWdlciIsInVzZXItdHlwZTpvcGVyYXRvciIsImhhemFyOnJlYWQiLCJlbGV2YXRpb246cmVhZCIsInd4OmFkdmFuY2VkOnJlYWQiXX0.DiwHAQt5FGrGmbivzRK2WNiqKhzQkVkys0sRhvmGyFNrPX7BW5GSZ91tTSORF_f1gJtDm08gWwKgFUnxd5FjfJmS8Z3AmtTwYzxzMxMU60IpGrQn7DbyEeHiSKoITadWkl--nBpAox8je-x3yccxX6qvdtmHqhiICOJ3lr8b65YWtLudcrQb1ylVeb02uuE9kzeFSfR5CZjCjw92XlkIYPySvYpOsJ1AYW4A6E3YZz_0a1i-2aqbm9sBX6mMcIEZ6sVrXMT14uBP7Z4tpNmLJ9tKM9op-H5Wxysfs_SurFJPNry042ZytW0ihka1efpBKBLp7kt2JcnjVWzFNEFhJQ'
    api_key = 'f15b282e5bd6495eae4cafe2d42b72e5'
    routev2 = RouteV2Request(api_key, token)
    routev2.request_route(5, None, None)
    routev2.test_route()

