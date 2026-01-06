#!/usr/bin/env python3

import requests
import json
from AirspaceLink_API.advisories import Geometry
from AirspaceLink_API.line_of_sight_enum import LineOfSight
from AirspaceLink_API.pilot_control_enum import PilotControl
from AirspaceLink_API.uav_weight_enum import UavWeight
from AirspaceLink_API.uav_type_enum import UavType


class Corridor:
    def __init__(self, corridor):
        self.corridor = corridor

class Network:
    def __init__(self, type, coordinates):
        self.type = type
        self.coordinates = coordinates


class RouteData:
    def __init__(self, type, coordinates):
        self.type = type
        self.coordinates = coordinates

    def to_json(self):
        return {
            'type': self.type,
            'coordinates': self.coordinates
        }


class SurfaceData:
    def __init__(self, density, infrastructure_types, pop_per_sq_mi, score, suitable_features):
        self.density = density
        self.infrastructure_types = infrastructure_types
        self.pop_per_sq_mi = pop_per_sq_mi
        self.score = score
        self.suitable_features = suitable_features


class Surface:
    def __init__(self, data_dict):
        self.surface_data = {key: SurfaceData(**value) for key, value in data_dict.items()}


class RouteResponse:
    def __init__(self, status_code: str, message: str, cooridor: Corridor, network: Network, route: RouteData):
        self.status_code = status_code
        self.message = message
        self.cooridor = cooridor
        self.network = network
        self.route = route
      

class RouteRequest:
    def __init__(self, api_key, token):
        self.__token = token
        self.__api_key = api_key

    def request_route(self, losType: LineOfSight = LineOfSight.BVLOS, maxAltitude: int = 100, pilotControl: PilotControl = PilotControl.SINGLE_PILOT, 
                      resolution: int = 10, returnCorridor: bool = True, return_network: bool = True, return_surface: bool = True, uavType: UavType = UavType.HYBRID, 
                      uavWeight: UavWeight = UavWeight.LIMITED, geometry: Geometry = None, features = None):

 
        route_path = None

        try:
            header = {"Content-Type": "application/json", "Authorization": 'Bearer ' + self.__token, "x-api-key": self.__api_key}

            data = {
                "losType": losType, 
                "maxAltitude": maxAltitude, 
                "pilotControl": pilotControl,
                "resolution": resolution, 
                "returnCorridor": returnCorridor, 
                "returnNetwork": return_network, 
                "returnSurface": return_surface, 
                "uavType": uavType, 
                "uavWeight": uavWeight, 
                "geometry": geometry.to_json(), 
                "features": features
            }

            data = json.dumps(data)

            response = requests.post(
                url="https://airhub-api-dev.airspacelink.com/v1/route", 
                headers= header,
                data=data
            )

            response_data = response.json()
            
            print(response_data["message"])
            corridor = Corridor(response_data['data']['corridor'])
            network = Network(response_data['data']['network']['type'], response_data['data']['network']['coordinates'])
            route = RouteData(response_data['data']['route']['path']['type'], response_data['data']['route']['path']['coordinates'])
            # surface = Surface(response_data['data']['surface'])

            route_response = RouteResponse(response_data['statusCode'], 
                                           response_data['message'],
                                           corridor,
                                           network,
                                           route
                                          )

            return route_response

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

        



