#!/usr/bin/env python

import requests
import json
from Airspacelink.advisories import Geometry, PolygonGeometry, Feature


class Aviation:
    def __init__(self, api_key, token):
        self.__api_key = api_key
        self.__token = token
        self.__aviation_features = []

    def request_aviation(self, geometry: Geometry, buffer: int):  # test response is read from file and used for testing

        try:
            data = None

        
            header = {"Content-Type": "application/json;charset=UTF-8", "Authorization": "Bearer %s" % self.__token, "x-api-key": self.__api_key}
            data = {
                "type": ["airports", "controlled_airspace", "uasfm_ceiling", "sua", "stadium"],  # FAA TYPES
                "geometry": geometry.to_json()   
            }

            data = json.dumps(data)
            endpoint = "https://airhub-api-sandbox.airspacelink.com/v1/aviation?buffer={0}"  # BUFFER nautical miles

            response = requests.post(
                url=endpoint.format(buffer),
                headers=header,
                data=data
            )

            response = response.json()
            response_data = response.get('data', [])
            
            for feature_data in response_data:
                geometry_data = feature_data.get('geometry', {})
                properties_data = feature_data.get('properties', {})

                coordinates = geometry_data.get('coordinates', [])[0]  

                geometry = Geometry(geometry_data.get('type'), coordinates)
                feature = Feature(geometry, properties_data)
        except Exception as ex:
            print(ex)
            return False    

