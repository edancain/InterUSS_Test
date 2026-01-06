#!/usr/bin/env python
import requests
import json
from AirspaceLink_API.advisories import Geometry, Feature

class HazardRisk:
    def __init__(self, api_key, token):  
        self.api_key = api_key
        self.token = token

    def request_hazard_risk(self, geometry: Geometry):

        try:
            # self.authentication = Authentication(self.api_key, self.client_id, self.client_secret)
            # token = self.authentication.request_token("hazar.read")
            header = {"Content-Type": "application/json", 'Authorization': 'Bearer ' + self.token,
                        "x-api-key": self.api_key}
            data = {"geometry": geometry }

            data = json.dumps(data)
            response = requests.post(
                url="https://airhub-api-sandbox.airspacelink.com/v1/hazard/",
                headers=header,
                data=data
            )

            response_data = response.json()
            print(response_data)
            guid = response_data["data"]
            return guid
        except Exception as ex:
            print(ex)

    def request_hazard_risk_ground_type(self, geometry: Geometry, resolution: int):

        try:
            headers1 = {"Content-Type": "application/json;charset=UTF-8", "Authorization": self.token,
                        "x-api-key": self.api_key}
            data1 = {
                "geometry": geometry.to_json(),
                "resolution": resolution
            }

            data1 = json.dumps(data1)
            response = requests.post(
                url="https://airhub-api-sandbox.airspacelink.com/v1/hazard/groundType",
                headers=headers1,
                data=data1
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
