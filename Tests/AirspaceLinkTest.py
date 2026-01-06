#!/usr/bin/env python3

import copy
from AirspaceLink_API.route import RouteRequest
from AirspaceLink_API.routeV2 import RouteV2Request, RouteV2Response
from AirspaceLink_API.layer import Layer, Layers
from AirspaceLink_API.operations import Operation
from AirspaceLink_API.aviation import Aviation
import datetime
from AirspaceLink_API.authentication import Authentication
from geopandas import GeoSeries
from shapely.geometry import shape, LineString, Polygon
import ast
import json
from AirspaceLink_API.test_utility import TestUtility
from AirspaceLink_API.stop import Stop
from AirspaceLink_API.advisories import Geometry, GeometryType, LineStringGeometry, PolygonGeometry
from AirspaceLink_API.operations import Operational_Feature, Operation_Properties


class AirspacelinkResponse:
    def __init__(self, route: LineStringGeometry, polygon: PolygonGeometry, routeV2Response: RouteV2Response, url, statusCode, message):
        self.route = route
        self.polygon = polygon
        self.url = url
        self.statusCode = statusCode
        self.message = message
        self.routeV2Response = routeV2Response

class AirspacelinkTests:
    def __init__(self):
        
        self.advisory = None
        self.advisory_data = None
        self.route = None
        self.route_data = None
        self.operation = None
        self.operation_guid = None
        self.aviation = None
        self.aviation_data = None
        self.hazard_risk = None
        self.hazard_risk_data = None
        self.aviation_features = None
        self.__client_id = "WxFWfnwgy0xieXdWws6OqMifV1nE9Ek6"
        self.__secret = "IFTBdP00Ta4mrHZFgpjP-n4i-G0eVG-OL42IFnfvGaK4qO_bYGUPGhnwFaeVWXXZ"
        self.__api_key = "f15b282e5bd6495eae4cafe2d42b72e5"


    def main(self):
        # self.create_test_route()
        pass

    def create_test_route(self, stops: []) -> AirspacelinkResponse:
        # stops = TestUtility().create_stops()
        if len(stops) == 0:
            return
        
        token = self.authentication()
        # token = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ild3dDk2SlJDTE9ER1pEeEpiRVVxdSJ9.eyJodHRwczovL2Fpcmh1Yi5haXJzcGFjZWxpbmsuY29tL3V0bSI6InZhbnRpcyIsImlzcyI6Imh0dHBzOi8vaWQtZGV2LmFpcnNwYWNlbGluay5jb20vIiwic3ViIjoiV3hGV2Zud2d5MHhpZVhkV3dzNk9xTWlmVjFuRTlFazZAY2xpZW50cyIsImF1ZCI6Imh0dHBzOi8vYXBpbS1lbmctZGV2LWN1cy5henVyZS1hcGkubmV0IiwiaWF0IjoxNzA4MTM4NTY1LCJleHAiOjE3MTA3MzA1NjUsImF6cCI6Ild4RldmbndneTB4aWVYZFd3czZPcU1pZlYxbkU5RWs2Iiwic2NvcGUiOiJpbnNpZ2h0cy5kZW1vIHRyYWZmaWM6cmVhZCBzeXN0ZW06YWRtaW4gaW5zaWdodHM6ZGVtbyBzeXN0ZW06cmVhZCB1c2VyOnJlYWQgYWR2aXNvcnk6cmVhZCByb3V0ZTpjcmVhdGUgYW5vbm9wczpyZWFkIHN1cmZhY2U6Y3JlYXRlIGZsaWdodGxvZzpyZWFkIGludml0ZTpyZWFkIGludml0ZTpjcmVhdGUgaW52aXRlOmRlbGV0ZSBvcmc6cmVhZCByb2xlOnVwZGF0ZSBjcmV3OnVwZGF0ZSBhZHZpc29yeTpjcmVhdGUgYWR2aXNvcnk6dXBkYXRlIGFkdmlzb3J5OmRlbGV0ZSBvcGVyYXRpb246cmVhZCBvcGVyYXRpb246Y3JlYXRlIG9wZXJhdGlvbjp1cGRhdGUgb3BlcmF0aW9uOmRlbGV0ZSBhaXJjcmFmdDpyZWFkIGFpcmNyYWZ0OmNyZWF0ZSBhaXJjcmFmdDp1cGRhdGUgYWlyY3JhZnQ6ZGVsZXRlIGZsaWdodGxvZzpjcmVhdGUgZmxpZ2h0bG9nOnVwZGF0ZSBmbGlnaHRsb2c6ZGVsZXRlIGF2aWF0aW9uOnJlYWQgdXNlcjpkZWxldGUgdXNlcjpyZW1vdmUgYjR1Zmx5OnRlc3RlciB1c2VyLXR5cGU6ZGlyZWN0b3IgdXNlci10eXBlOm1hbmFnZXIgdXNlci10eXBlOm9wZXJhdG9yIGhhemFyOnJlYWQgZWxldmF0aW9uOnJlYWQgd3g6YWR2YW5jZWQ6cmVhZCIsImd0eSI6ImNsaWVudC1jcmVkZW50aWFscyIsInBlcm1pc3Npb25zIjpbImluc2lnaHRzLmRlbW8iLCJ0cmFmZmljOnJlYWQiLCJzeXN0ZW06YWRtaW4iLCJpbnNpZ2h0czpkZW1vIiwic3lzdGVtOnJlYWQiLCJ1c2VyOnJlYWQiLCJhZHZpc29yeTpyZWFkIiwicm91dGU6Y3JlYXRlIiwiYW5vbm9wczpyZWFkIiwic3VyZmFjZTpjcmVhdGUiLCJmbGlnaHRsb2c6cmVhZCIsImludml0ZTpyZWFkIiwiaW52aXRlOmNyZWF0ZSIsImludml0ZTpkZWxldGUiLCJvcmc6cmVhZCIsInJvbGU6dXBkYXRlIiwiY3Jldzp1cGRhdGUiLCJhZHZpc29yeTpjcmVhdGUiLCJhZHZpc29yeTp1cGRhdGUiLCJhZHZpc29yeTpkZWxldGUiLCJvcGVyYXRpb246cmVhZCIsIm9wZXJhdGlvbjpjcmVhdGUiLCJvcGVyYXRpb246dXBkYXRlIiwib3BlcmF0aW9uOmRlbGV0ZSIsImFpcmNyYWZ0OnJlYWQiLCJhaXJjcmFmdDpjcmVhdGUiLCJhaXJjcmFmdDp1cGRhdGUiLCJhaXJjcmFmdDpkZWxldGUiLCJmbGlnaHRsb2c6Y3JlYXRlIiwiZmxpZ2h0bG9nOnVwZGF0ZSIsImZsaWdodGxvZzpkZWxldGUiLCJhdmlhdGlvbjpyZWFkIiwidXNlcjpkZWxldGUiLCJ1c2VyOnJlbW92ZSIsImI0dWZseTp0ZXN0ZXIiLCJ1c2VyLXR5cGU6ZGlyZWN0b3IiLCJ1c2VyLXR5cGU6bWFuYWdlciIsInVzZXItdHlwZTpvcGVyYXRvciIsImhhemFyOnJlYWQiLCJlbGV2YXRpb246cmVhZCIsInd4OmFkdmFuY2VkOnJlYWQiXX0.DiwHAQt5FGrGmbivzRK2WNiqKhzQkVkys0sRhvmGyFNrPX7BW5GSZ91tTSORF_f1gJtDm08gWwKgFUnxd5FjfJmS8Z3AmtTwYzxzMxMU60IpGrQn7DbyEeHiSKoITadWkl--nBpAox8je-x3yccxX6qvdtmHqhiICOJ3lr8b65YWtLudcrQb1ylVeb02uuE9kzeFSfR5CZjCjw92XlkIYPySvYpOsJ1AYW4A6E3YZz_0a1i-2aqbm9sBX6mMcIEZ6sVrXMT14uBP7Z4tpNmLJ9tKM9op-H5Wxysfs_SurFJPNry042ZytW0ihka1efpBKBLp7kt2JcnjVWzFNEFhJQ'
        if token is None:
            return None

        # aircraft_lon = -118.415045
        # aircraft_lat = 33.901701
        aircraft_lon = stops[0].get_longitude()
        aircraft_lat = stops[0].get_latitude()

        route = self.get_airspacelink_route(stops, aircraft_lat, aircraft_lon, "Edan TEST", token)
        return route


    def authentication(self):
        authentication = Authentication(self.__api_key, self.__client_id, self.__secret)
        token = authentication.request_token()
        if token is None:
            print("Something went wrong with getting an AirspaceLink token")
            return None
        elif token == 'HTTP Request failed':
            return None

        return token


    def get_airspacelink_route(self, stops, aircraft_latitude, aircraft_longitude, route_name, token) -> AirspacelinkResponse:
        # Returns an updated json collection if Airspacelink detects that we have to go around sensitive areas
        if stops is None:
            return None

        if len(stops) == 0:
            return None

        try:
            route_buffer = 10
            complete_airspacelink_route = []
            set_first_stop = True
            last_stop = None

            # route_data = self.airspace_route.request_route(route, route_buffer)
            #route = RouteRequest(self.__api_key, token)
            routeV2 = RouteV2Request(self.__api_key, token)

            # NB: A route in Airspacelink is a Multipoint consisting of a start and a stop
            # We iterate the collection of stops and build up our complete route due to this limitation, appending
            # the results to return the update route to Cheetah.
            # The last stop of each segment becomes the first of the next segment until we get to the end.

            count = 0
            coordinates = []
            for stop in stops:
                coordinates.append([float(stop.get_longitude()), float(stop.get_latitude())])

            # fly home
            coordinates.append([float(stops[0].get_longitude()), float(stops[0].get_latitude())])

            geometry = Geometry(GeometryType.MULTI_POINT, coordinates)

            l1 = Layer("helipads", 9)
            l2 = Layer("urgent_care", 9)
            l3 = Layer("fire_stations", 9)
            l4 = Layer("police_stations", 9)
            l5 = Layer("hospitals", 9)
            l6 = Layer("schools", 9)
            l7 = Layer("airports", 9)

            layers = Layers()
            layers.add_layer(l1)
            layers.add_layer(l2)
            layers.add_layer(l3)
            layers.add_layer(l4)
            layers.add_layer(l5)
            layers.add_layer(l6)
            layers.add_layer(l7)

            routeV2Response = routeV2.request_route(10, layers, geometry)
            if routeV2Response is None:
                return None
            '''
            for stop in stops:
                coordinates = []

                count += 1
                if count == 1:
                    continue

                if set_first_stop is True:  # this is the start, done once
                    # first stop is the location of the vehicle
                    coordinates = [[float(aircraft_longitude), float(aircraft_latitude)]] 
                    set_first_stop = False

                if last_stop is not None:
                    coordinates =[[float(last_stop.get_longitude()), float(last_stop.get_latitude())]]

                coordinates.append([float(stop.get_longitude()), float(stop.get_latitude())])

                geometry = Geometry(GeometryType.MULTI_POINT, coordinates)
                features = {"streams": {"weight": 0.5}}

                los_type = "BVLOS"
                max_altitude = 90
                pilot_control = "AUTOMATED_CONTROL"
                uav_type = "HYBRID"
                uav_weight = "LIMITED"
                return_surface = True
                return_network = True
                return_corridor = True
                resolution = 10

                route_response = route.request_route(los_type, max_altitude, pilot_control, resolution, return_corridor, return_network, return_surface, uav_type, uav_weight, geometry, features)
                error_data = json.loads(route_response)

                # Checking if the "error" key exists in the dictionary
                if "error" in error_data:
                    return route_response
                
                if last_stop is not None and route_response.route.coordinates is not None:
                    route_response.route.coordinates.pop(0)

                last_stop = copy.deepcopy(stop)

                if route_response == 'HTTP Request failed':
                    print('Airspacelink route request failed: %s' % route_response)
                    return None

                complete_airspacelink_route.append(route_response.route.coordinates)
                # break

            # now for the fly home section: 
            if len(stops) > 2:
                coordinates = []
                coordinates =[[float(last_stop.get_longitude()), float(last_stop.get_latitude())]]
                coordinates.append([float(aircraft_longitude), float(aircraft_latitude)]) 
                geometry = Geometry(GeometryType.MULTI_POINT, coordinates)

                route_data = route.request_route(los_type, max_altitude, pilot_control, resolution, return_corridor, return_network, return_surface, uav_type, uav_weight, geometry, features)

                if route_data.route.coordinates:
                    route_data.route.coordinates.pop(0)

                complete_airspacelink_route.append(route_data.route.coordinates)
            
            flattened_coordinates = [item for sublist in complete_airspacelink_route for item in sublist]

            #print(flattened_coordinates)
            '''     
            buffered_route = self.buffer_route(routeV2Response.path.coordinates)
            
            url = self.__create_operation(buffered_route, route_name, token)

            # self.__get_aviation(complete_airspacelink_route, token)

            # OPERATION V2 TESTING

            '''home = complete_airspacelink_route[len(complete_airspacelink_route) - 1]
            seclast = complete_airspacelink_route[len(complete_airspacelink_route) - 2]

            complete_airspacelink_route.remove(home)
            complete_airspacelink_route.remove(seclast)
            geojson_linestring = {"type": "LineString", "coordinates": complete_airspacelink_route}
            guid_v2 = self.__create_operation_v2(geojson_linestring, route_name, token)
            guid_v2 = None'''

            linestring = LineStringGeometry(routeV2Response.path.coordinates)
            airspacelink_response = AirspacelinkResponse(linestring, buffered_route, routeV2Response, url, 200, 'Success')

            return airspacelink_response
        except Exception as e:
            print(json.dumps(e))  # request_route() missing 5 required positional arguments: 'pilot_control', 'max_altitude', 'uav_weight', 'uav_type', and 'features'
            return json.loads({'statusCode': 400, 'message': 'Bad Request'})


    @staticmethod
    def buffer_simple_line(coordinates: [], distance: float) -> PolygonGeometry:
        line = LineString(coordinates)
        buffer = line.buffer(distance)
        try:
            geometry = None
            json_buffer = GeoSeries([buffer]).to_json()
            complete_json_geometry = json.loads(json_buffer)
            for feature in complete_json_geometry['features']:
                geometry = feature['geometry']

            polygon = None
            # remove any doughnuts
            for buf in geometry['coordinates']:
                polygon = PolygonGeometry(buf)
                break

            return polygon
        except Exception as ee:
                print(ee)
 

    def buffer_route(self, airspacelink_route) -> PolygonGeometry:
        try:
            # all_coordinates = []

            '''for route_data in airspacelink_route:
                try:
                    coordinates = route_data.data['route'].coordinates
                    for coordinate in coordinates:
                        # Append each coordinate to the flattened_coordinates list
                        all_coordinates.append(coordinate)

                except:
                    pass'''

            line = LineString(airspacelink_route)
            shapely_buffer = line.buffer(0.001)

            try:
                geometry = None
                json_buffer = GeoSeries([shapely_buffer]).to_json()
                complete_json_geometry = json.loads(json_buffer)
                for feature in complete_json_geometry['features']:
                    geometry = feature['geometry']


                polygon = None
                # remove any doughnuts
                for buf in geometry['coordinates']:
                    polygon = PolygonGeometry(buf)
                    break

                # print(polygon.to_json())

                return polygon

            except Exception as ee:
                print(ee)
        except Exception as eee:
            print(eee)


    def __create_operation(self, buffer, route_name, token):
        # california_time = datetime.datetime.now() - datetime.timedelta(hours=20)
        california_time = datetime.datetime.now() + datetime.timedelta(hours=7, minutes=5)  # pheonix
        current_datetime = california_time.strftime('%Y-%m-%dT%H:%M:%SZ')
        start_time = current_datetime  # '2022-10-21T12:15:23.040623Z'#

        operation_name = route_name

        timezone = "America/Los_Angeles"
        # timezone = "America/Phoenix"#Mountain Time - No Daylight Savings (MST)

        category = "107"  # {'Commercial Part 107' , 'Recreational Part 44809'}
        duration = 60
        max_altitude = 100

        # buffer = ast.literal_eval(buffer)
        operation_properties = Operation_Properties(operation_name, category, start_time, timezone, duration, max_altitude, True, "")

        self.operation = Operation(self.__api_key, token)
        operation_feature = Operational_Feature("Feature", operation_properties, buffer)
        url = self.operation_guid = self.operation.request_operation(operation_feature) # buffer, operation_name, category, duration, max_altitude, start_time, timezone)

        # Successfully creating an operation will return a guid that may be used to retrieve the operation within the
        # AirHub for Pilots LAANC application. Following is a sample deep-link url
        # (after the operation has been successfully generated):
        # https://airhub-api-sandbox.airspacelink.com/laanc?operation=<guid>

        
        return url


    def __create_operation_v2(self, linestring, route_name, token):
        # california_time = datetime.datetime.now() - datetime.timedelta(hours=20)
        california_time = datetime.datetime.now() + datetime.timedelta(hours=7, minutes=5) #pheonix
        current_datetime = california_time.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
        start_time = current_datetime  # '2022-10-21T12:15:23.040623Z'#

        operation_name = route_name

        timezone = "America/Los_Angeles"
        # timezone = "America/Phoenix"#Mountain Time - No Daylight Savings (MST)

        category = "107"  # {'Commercial Part 107' , 'Recreational Part 44809'}
        duration = 60
        max_alitude = 100

        # line = ast.literal_eval(linestring)

        self.operationV2 = OperationV2(self.__api_key, token)
        uuid = self.operation_guid = self.operationV2.request_operation(
            linestring, operation_name, category, duration, max_alitude,  # must be a polygon
            start_time, timezone)

        # Successfully creating an operation will return a guid that may be used to retrieve the operation within the
        # AirHub for Pilots LAANC application. Following is a sample deep-link url
        # (after the operation has been successfully generated):
        # https://airhub-api-sandbox.airspacelink.com/laanc?operation=<guid>

        url = ""
        if uuid is not None:
            url = "https://launch-sandbox.airspacelink.com?operation=%s" % uuid  # launch-sandbox.airspacelink.com
            # url = "https://airhub-sandbox.airspacelink.com/laanc/?operation=%s" % uuid
            # webbrowser.open(url)  # url[, new=0[, autoraise=True]])
        return url


    def __get_aviation(self, route, token):
        self.aviation = Aviation(self.__api_key, token)
        # TODO: REMOVE THIS ONCE TESTING IS DONE
        with open('/Users/edancain/PycharmProjects/AirSpaceLink_Flask/airspace_json_response_van_nuys.txt') as f:
            response_data = f.readlines()

        self.aviation_features = self.aviation.request_aviation(route, response_data)
        if len(self.aviation_features) > 0:
            self.__process_aviation_features()


    def __process_aviation_features(self):
        for feature in self.aviation_features:
            try:
                if feature.Type == "ceiling":
                    print(feature.ceiling)
            except Exception as ex:
                print(ex)

            # find out where our route intersects, get the mid-point, then add a waypoint to the route at that location
            # with a z value for that point polygon/feature


# TESTING
# def main():
#    asl_tests = AirspacelinkTests()
#    asl_tests.main()
    # asl_tests.buffer_route(None)

#if __name__ == '__main__':
#    main()
