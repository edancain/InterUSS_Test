from AirspaceLink_API.stop import Stop
import json
import logging

class TestUtility:

    def __init__(self):
        self.stops = []

    def create_stops(self):
        # Manhattan Beach
        stop = Stop(0)
        stop.set_longitude(-118.417851)
        stop.set_latitude(33.900570)
        stop1 = Stop(1)
        stop1.set_longitude(-118.419803)
        stop1.set_latitude(33.903175)
        stop2 = Stop(2)
        stop2.set_longitude(-118.419310)
        stop2.set_latitude(33.904609)
        stop3 = Stop(3)
        stop3.set_longitude(-118.421037)
        stop3.set_latitude(33.905664)
        stop4 = Stop(4)
        stop4.set_longitude(-118.421214)
        stop4.set_latitude(33.903705)
        stop5 = Stop(5)
        stop5.set_longitude(-118.420088)
        stop5.set_latitude(33.901399)

        self.stops.append(stop)
        self.stops.append(stop1)
        self.stops.append(stop2)
        self.stops.append(stop3)
        self.stops.append(stop4)
        self.stops.append(stop5)
        

        try:
            # Convert each Stop object to a dictionary
            stops_as_dicts = [stop.to_json() for stop in self.stops]

            js = json.dumps(stops_as_dicts)
            # print(js)  # Optional: print the serialized JSON string
        except json.JSONEncodeError as ex:
            logging.error(f"Serialization Error: {ex}")
        except Exception as ex:
            logging.error(f"An unexpected error occurred: {ex}")

        return self.stops
