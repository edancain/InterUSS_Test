from __future__ import annotations

# UTILITY to create objects for DSS interaction. 
# NB: Create the objects and serialize them for http request data

# NB: These objects are used to create the object response from the DSS server.
from typing import List
from enum import Enum
from datetime import datetime, timedelta


class Altitude:
    def __init__(self, value, reference, units):
        self.value = value
        self.reference = reference
        self.units = units

    @classmethod
    def from_json(cls, data):
        return cls(data["value"], data["reference"], data["units"])

    def to_json(self):
        return {"value": self.value, "reference": self.reference, "units": self.units}
 
class AltitudeRange:
    def __init__(self, lower: Altitude, upper: Altitude):
        self.lower = lower
        self.upper = upper

class AreaOfInterest:  #Used in Operational Intent ref request, 
    def __init__(self, volume, time_start, time_end):
        self.volume = volume
        self.time_start = time_start
        self.time_end = time_end

    def to_json(self):
        return {
            "area_of_interest": {
                "volume": self.volume.to_json() if self.volume else None,
                "time_start": self.time_start,
                "time_end": self.time_end
            }
        }
    
    @classmethod
    def from_json(cls, json_data):
        volume_data = json_data.get("area_of_interest", {}).get("volume")
        time_start = json_data.get("area_of_interest", {}).get("time_start")
        time_end = json_data.get("area_of_interest", {}).get("time_end")

        volume = Volume.from_json(volume_data) if volume_data else None

        return cls(volume, time_start, time_end)

# NB: Stupidly the InterUSS description has a   

class Center:
    def __init__(self, lng, lat):
        self.lng = lng
        self.lat = lat

    def to_json(self):
        return {"lng": self.lng, "lat": self.lat}


class Details:  # USS https://redocly.github.io/redoc/?url=https://raw.githubusercontent.com/astm-utm/Protocol/v1.0.0/utm.yaml#tag/p2p_utm/operation/notifyOperationalIntentDetailsChanged
    def __init__(self, data):
        self.volumes = data.get("volumes", [])
        self.off_nominal_volumes = data.get("off_nominal_volumes", [])
        self.priority = data.get("priority", 0)

    def to_json(self):
        return {
            "volumes": self.volumes,
            "off_nominal_volumes": self.off_nominal_volumes,
            "priority": self.priority
        }


class Extent: # stupidly the same as an area_of_interest in their description
    def __init__(self, volume: Volume, time_start: TimeMeasured, time_end: TimeMeasured):
        self.volume = volume
        self.time_start = time_start
        self.time_end = time_end

    def to_json(self):
        return {
            "volume": self.volume.to_json() if self.volume else None,
            "time_start": self.time_start.to_json() if self.time_start else None,
            "time_end": self.time_end.to_json() if self.time_end else None
        }
    
    def to_dict(self):
        return self.to_json()
    
    @classmethod
    def from_json(cls, json_obj):
        volume = json_obj.get("volume")
        time_start = json_obj.get("time_start")
        time_end = json_obj.get("time_end")

        volume_instance = Volume.from_json(volume) if volume else None
        time_start_instance = TimeMeasured.from_json(time_start)
        time_end_instance = TimeMeasured.from_json(time_end)

        return cls(volume_instance, time_start_instance, time_end_instance)

class Extents:
    def __init__(self, extents: List[Extent], uss_base_url: str):
        self.extents = extents
        self.uss_base_url = uss_base_url

    def to_json(self):
        return {
            "extents": [extent.to_json() for extent in self.extents] if self.extents else None,
            "uss_base_url": self.uss_base_url
        }

    def to_dict(self):
        return self.to_json()

    @classmethod
    def from_json(cls, json_obj):
        extents = json_obj.get("extents")
        uss_base_url = json_obj.get("uss_base_url")

        extents_instances = [Extent.from_json(extent) for extent in extents] if extents else None

        return cls(extents_instances, uss_base_url)

# https://redocly.github.io/redoc/?url=https://raw.githubusercontent.com/astm-utm/Protocol/v1.0.0/utm.yaml#tag/Constraint-details/operation/getConstraintDetails
class ZoneAuthority:
    def __init__(self, name: str, service: str, contact_name: str, site_url: str, email: str, phone: str, purpose: str, interval_before: str):
        self.name = name
        self.service = service
        self.contact_name = contact_name
        self.site_url = site_url
        self.email = email
        self.phone = phone
        self.purpose = purpose
        self.interval_before = interval_before
                              
    def from_json(self, data):
        self.name = data["name"]
        self.service = data["service"]
        self.contact_name = data["contact_name"]
        self.site_url = data["site_url"]
        self.email = data["email"]
        self.phone = data["phone"]
        self.purpose = data["purpose"]
        self.interval_before = data["interval_before"]

    def to_json(self):
        return {
            "name": self.name,
            "service": self.service,
            "contact_name": self.contact_name,
            "site_url": self.site_url,
            "email": self.email,
            "phone": self.phone,
            "purpose": self.purpose,
            "interval_before": self.interval_before
        }
        

class Geozone:
    def __init__(self, identifier: str, country: str, zone_authority: List[ZoneAuthority], name: str, type: str, restriction: str, restriction_conditions: List[str], region, reason: List[str],
                 other_reason_info: str, regulation_exemption: str, u_space_class: str, message: str, additional_properties):
        self.identifier = identifier
        self.country = country
        self.zone_authority = zone_authority
        self.name = name
        self.type = type
        self.restriction = restriction
        self.restriction_conditions = restriction_conditions
        self.region = region
        self.reason = reason
        self.other_reason_info = other_reason_info
        self.regulation_exception = regulation_exemption
        self.u_space_class = u_space_class
        self.message = message
        self.additional_properties = additional_properties   
                 
                 
    def from_json(self, data):
        self.identifier = data["identifier"]
        self.country = data["country"]
        self.zone_authority = ZoneAuthority(data.get("zone_authority"), [])
        self.name = data["name"]
        self.type = data["type"]
        self.restriction = data["restriction"]
        self.restriction_conditions = data.get("restriction_conditions", [])
        self.region = data["region"]
        self.reason = data.get("reason", [])
        self.other_reason_info = data["other_reason_info"]
        self.regulation_exception = data["regulation_exception"]
        self.u_space_class = data["u_space_class"]
        self.message = data["message"]
        self.additional_properties = data["additional_properties"]

    def to_json(self):
        return {
            "identifier": self.identifier,
            "country": self.country,
            "zone_authority": [zone_auth.to_json() for zone_auth in self.zone_authority],
            "name": self.name,
            "type": self.type,
            "restriction": self.restriction,
            "restriction_conditions": self.restriction_conditions,
            "region": self.region,
            "reason": self.reason,
            "other_reason_info": self.other_reason_info,
            "regulation_exception": self.regulation_exception,
            "u_space_class": self.u_space_class,
            "message": self.message,
            "additional_properties": self.additional_properties
        }


class NewSubscription:
    def __init__(self, uss_base_url: str, notify_for_constraints: bool):
        self.uss_base_url = uss_base_url
        self.notify_for_constraints = notify_for_constraints

    def to_json(self):
        return {
            "uss_base_url": self.uss_base_url,
            "notify_for_constraints": self.notify_for_constraints
        }
    
    @classmethod
    def from_json(cls, json_obj):
        uss_base_url = json_obj.get("uss_base_url")
        notify_for_constraints = json_obj.get("notify_for_constraints")

        return cls(uss_base_url, notify_for_constraints)
    

class NextTelemetryOpportunity:
    def __init__(self, data):
        if data == {}:
            return

        self.value = data["value"]
        self.format = data["format"]

    def to_json(self):
        return {"value": self.value, "format": self.format}


class OperationalIntentStatus(Enum):
    ACCEPTED = "Accepted"
    ACTIVATED = "Activated"
    NONCONFORMING = "Nonconforming"
    CONTINGENT = "Contingent"

    '''
    Enum: "Accepted" "Activated" "Nonconforming" "Contingent"
    State of an operational intent. 'Accepted': Operational intent is created and shared, 
    but not yet in use; see standard text for more details. The create or update request 
    for this operational intent reference must include a Key containing all OVNs for all 
    relevant Entities. 'Activated': Operational intent is in active use; see standard text 
    for more details. The create or update request for this operational intent reference 
    must include a Key containing all OVNs for all relevant Entities. 'Nonconforming': UA is 
    temporarily outside its volumes, but the situation is expected to be recoverable; see 
    standard text for more details. In this state, 
    the /uss/v1/operational_intents/{entityid}/telemetry USS-USS endpoint should respond, 
    if available, to queries from USS peers. The create or update request for this operational 
    intent may omit a Key in this case because the operational intent is being adjusted as 
    flown and cannot necessarily deconflict. 'Contingent': UA is considered unrecoverably 
    unable to conform with its coordinate operational intent; see standard text for more details. 
    This state must transition to Ended. In this state, the /uss/v1/operational_intents/{entityid}/telemetry 
    USS-USS endpoint should respond, if available, to queries from USS peers. The create or update request 
    for this operational intent may omit a Key in this case because the operational intent is being adjusted 
    as flown and cannot necessarily deconflict.
    '''


class OutlineCircle:
    def __init__(self, center_lng, center_lat, radius_value, radius_units):
        self.center = {'lng': center_lng, 'lat': center_lat}
        self.radius = {'value': radius_value, 'units': radius_units}

    def to_json(self):
        return {'center': self.center, 'radius': self.radius}

    @classmethod
    def from_json(cls, json_obj):
        center_lng = json_obj['center']['lng']
        center_lat = json_obj['center']['lat']
        radius_value = json_obj['radius']['value']
        radius_units = json_obj['radius']['units']

        return cls(center_lng, center_lat, radius_value, radius_units)



class OutlinePolygon:
    def __init__(self, vertices: Vertices):
        self.vertices = vertices

    def to_json(self):
        return self.vertices.to_json()# "vertices": self.vertices.to_json() if isinstance(self.vertices, Vertices) else []
        
    
    @classmethod
    def from_json(cls, json_obj):
        vertices = Vertices.from_json(json_obj.get("vertices", {}))  
        return cls(vertices)


class Position:
    def __init__(self, data):
        self.longitude = data["longitude"]
        self.latitude = data["latitude"]
        self.accuracy_h = data["accuracy_h"]
        self.accuracy_v = data["accuracy_v"]
        self.extrapolated = data["extrapolated"]
        self.altitude = Altitude(data["altitude"])

    def to_json(self):
        return {"longitude": self.longitude, "latitude": self.latitude, "accuracy_h": self.accuracy_h, "accuracy_v": self.accuracy_v, "extrapolated": self.extrapolated, "altitude": self.altitude}


class Radius:
    def __init__(self, value, units):
        self.value = value
        self.units = units

    def to_json(self):
        return {"value": self.value, "units": self.units}


class Reference:
    def __init__(self, data):
            self.id = data["id"]
            self.manager = data["manager"]
            self.uss_availability = data["uss_availability"]
            self.version = data["version"]
            self.state = data.get("state", None) # USS Retrieve Constraint Details doesn't have this parameter
            self.ovn = data["ovn"]

            self.time_start = Time(data["time_start"]) if data["time_start"] != {} else None
            self.time_end = Time(data["time_end"]) if data["time_end"] != {} else None

            self.uss_base_url = data["uss_base_url"]
            self.subscription_id = data.get("subscription_id", None) # USS Retrieve Constraint Details doesn't have this parameter

    def to_json(self):
            return {
                "id": self.id,
                "manager": self.manager,
                "uss_availability": self.uss_availability,
                "version": self.version,
                "state": self.state,
                "ovn": self.ovn,
                "time_start": self.time_start,
                "time_end": self.time_end,
                "uss_base_url": self.uss_base_url,
                "subscription_id": self.subscription_id
            }


class Subscriber:
    def __init__(self, data):
        # Assuming what a subscriber has re attributes, like id, name, etc.
        # Initialize them here. In the REDOC I cannot find reference to it, TODO look to the InterUSS examples for a description
        self.subscriptions = [Subscription(sub_data) for sub_data in data.get("subscriptions", [])]
        self.uss_base_url = data.get("uss_base_url", None)  

    def to_json(self):
        return{
        "subscriptions": [subscription.to_json() for subscription in self.subscriptions],
        "uss_base_url": self.uss_base_url
        }


class Subscription:
    def __init__(self, data):
        self.subscription_id = data.get("subscription_id", None)
        self.notification_index = data.get("notification_index", None)

    def to_json(self):
        return {
            "subscription_id": self.subscription_id,
            "notification_index": self.notification_index
        }


class Telemetry:
    def __init__(self, time_measured: TimeMeasured, position: Position, velocity: Velocity):
        self.time_measured = time_measured
        self.position = position
        self.velocity = velocity

    def to_json(self):
        return {
            "time_measured": self.time_measured.to_json(), 
            "position": self.position.to_json(),
            "velocity": self.velocity.to_json()
        }
    
    @classmethod
    def from_json(cls, data):
        time_measured = TimeMeasured(data.get("time_measured"))
        position = Position(data.get("position"))
        velocity = Velocity(data.get("velocity"))
    

class Time:
    def __init__(self, value: datetime):
        self.value = value
        self.format = "RFC3339"

    @classmethod   
    def from_json(cls, data):

        cls.value = data.get("value")
        cls.format = data.get("format")

    def to_json(self):
        return {"value": self.value, "format": self.format}
    

class TimeMeasured:
    def __init__(self, value: str, format: str):
        self.value = value
        self.format = format
    
    def to_json(self):
        return {"value": self.value, "format": self.format}
   
    @classmethod
    def from_json(cls, data):
        value = data.get("value")
        format = data.get("format")
        return cls(value, format)
    
from typing import List

class TimeRange:
    def __init__(self, start_time: TimeMeasured, end_time: TimeMeasured):
        self.start_time = start_time
        self.end_time = end_time


class StartEndTime:
    @classmethod
    def from_to_time(cls, from_time: datetime, duration: int)-> TimeRange:

        # Format the current time as a string
        formatted_now = from_time.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"

        # Calculate the time 5 minutes ahead
        time_ahead = from_time + timedelta(minutes=duration)

        # Format the time 5 minutes ahead as a string
        formatted_time_ahead = time_ahead.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"
        start_time = TimeMeasured(formatted_now, "RFC3339")
        end_time = TimeMeasured(formatted_time_ahead, "RFC3339")

        return TimeRange(start_time, end_time)


class Velocity:
    def __init__(self, data):
        self.speed = data["speed"]
        self.units_speed = data["units_speed"]
        self.track = data["track"]

    def to_json(self):
        return {"speed": self.speed, "units_speed": self.units_speed, "track": self.track}

class Vertex:
    def __init__(self, latitude, longitude) :
        self.latitude = latitude
        self.longitude = longitude

    def to_json(self):
        return {
            "lng": self.longitude,
            "lat": self.latitude
        }
    
    @classmethod
    def from_json(cls, json_obj):
        latitude = json_obj.get("lat")
        longitude = json_obj.get("lng")
        return cls(latitude, longitude)
    

class Vertices:
    def __init__(self, vertices: List[Vertex]):
        self.vertices = vertices

    def to_json(self):
        return {
            "vertices": [vertex.to_json() for vertex in self.vertices]
        }
    
    @classmethod
    def from_json(cls, json_obj):
        vertices = [Vertex.from_json(vertex) for vertex in json_obj]
        return cls(vertices)


class Volume:
    def __init__(self, outline_circle: OutlineCircle, outline_polygon: OutlinePolygon, altitude_lower: Altitude, altitude_upper: Altitude):
        self.outline_circle = outline_circle
        self.outline_polygon = outline_polygon
        self.altitude_lower = altitude_lower
        self.altitude_upper = altitude_upper

    # NB: Geometry is either a circle or polygon, not both
    def to_json(self):
        if self.outline_circle is None:
            return {
                "outline_polygon": self.outline_polygon.to_json() if self.outline_polygon else None,
                "altitude_lower": self.altitude_lower.to_json() if self.altitude_lower else None,
                "altitude_upper": self.altitude_upper.to_json() if self.altitude_upper else None
            }
        elif self.outline_polygon is None:
            return {
                "outline_circle": self.outline_circle.to_json() if self.outline_circle else None,
                "altitude_lower": self.altitude_lower.to_json() if self.altitude_lower else None,
                "altitude_upper": self.altitude_upper.to_json() if self.altitude_upper else None
            }
        else:
            return{
                "outline_circle": self.outline_circle.to_json() if self.outline_circle else None,
                "outline_polygon": self.outline_polygon.to_json() if self.outline_polygon else None,
                "altitude_lower": self.altitude_lower.to_json() if self.altitude_lower else None,
                "altitude_upper": self.altitude_upper.to_json() if self.altitude_upper else None
            }
        

    @classmethod
    def from_json(cls, json_obj):
        outline_circle = json_obj.get("outline_circle")
        outline_polygon = json_obj.get("outline_polygon")
        altitude_lower = json_obj.get("altitude_lower")
        altitude_upper = json_obj.get("altitude_upper")

        if outline_circle:
            return cls(
                OutlineCircle.from_json(outline_circle),
                None,  # Set outline_polygon to None since outline_circle is present
                Altitude.from_json(altitude_lower) if altitude_lower else None,
                Altitude.from_json(altitude_upper) if altitude_upper else None
            )
        elif outline_polygon:
            return cls(
                None,  # Set outline_circle to None since outline_polygon is present
                OutlinePolygon.from_json(outline_polygon),
                Altitude.from_json(altitude_lower) if altitude_lower else None,
                Altitude.from_json(altitude_upper) if altitude_upper else None
            )
        else:
            return cls(
                None,  # Set both outline_circle and outline_polygon to None if both are absent
                None,
                Altitude.from_json(altitude_lower) if altitude_lower else None,
                Altitude.from_json(altitude_upper) if altitude_upper else None
            )

class Message:
    def __init__(self, data):
        self.message = data["message"]


# Test script
def main():
    try:
        zone_auth = ZoneAuthority("Edan_Test", "aerial", "Edan Cain", "www.airspacelink.com", "edan.cain@airspacelink.com", "909-222-2442", "AUTHORIZATION", "interval before what?")
        geozone = Geozone("identifier_edan", "New Zealand", [zone_auth], "Edan Test", "Flight Authorization", "No Restriction", [], 65535, "Air_TRAFFIC", "no Other reason", "YES", "D", "this is a message", None)
        json = geozone.to_json()
        print(json)
    except Exception as ex:
        print(ex)


if __name__ == '__main__':
    main()