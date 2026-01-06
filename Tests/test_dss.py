import sys
from pathlib import Path
from Tests import dss_interaction
# Add the parent directory to sys.path
sys.path.append(str(Path(__file__).resolve().parent.parent))
from Utility import utility
from typing import List
from datetime import datetime, timedelta
import json

from DSS import authentication
from DSS import operational_intent_reference, constraint_reference, subscription

from Airspacelink import AirspaceLinkTest

import uuid

# ##################################### ######## #
# ########      DSS SERVER TESTDS       ######## #
# ##################################### ######## #

# ##################################### ######## #
# ######## OPERATIONAL INTENT REFERENCES ######## #
# ##################################### ######## #

def query_all_operational_intent_references():
    # Query All Operational Intent References
    # https://redocly.github.io/redoc/?url=https://raw.githubusercontent.com/astm-utm/Protocol/v1.0.0/utm.yaml#tag/Operational-intent-references/operation/queryOperationalIntentReferences

    # create test data
    outline_circle = utility.OutlineCircle(-118.456, 34.123, 300, "M")

    vertex1 = utility.Vertex(34.142604, -118.803964) 
    vertex2 = utility.Vertex(34.146256, -118.801505)
    vertex3 = utility.Vertex(34.143902, -118.800370)
    vertex4 = utility.Vertex(34.142604, -118.803964)
    vectices = utility.Vertices([vertex1, vertex2, vertex3])
    outline_polygon = utility.OutlinePolygon(vectices)

    altitude_lower = utility.Altitude(300, "W84", "M")
    altitude_upper = utility.Altitude(350, "W84", "M")

    # Current time in UTC with 'Z' format
    t_start = datetime.utcnow().replace(microsecond=0)
    t_start_str = t_start.isoformat() + 'Z'  # RFC3339 format string

    # Adding 20 minutes to t_start datetime object just for a test
    t_end = t_start + timedelta(minutes=20)
    t_end_str = t_end.isoformat() + 'Z'  # Convert t_end to RFC3339 format string
    
    time_start = utility.Time(t_start_str) 
    time_end = utility.Time(t_end_str)

    volume = utility.Volume(None, outline_polygon, altitude_lower, altitude_upper)
    areaofinterest = utility.AreaOfInterest(volume, time_start, time_end)        

    token = authentication.Authentication().get_token()
    dss_server = dss_interaction.DSS_Interaction("http://localhost:8082")
    op_intent_references = dss_server.query_all_operational_intent_references(areaofinterest, token)


def retrieve_operational_intent_reference(id):
    id = "2f8343be-6482-4d1b-a474-16847e01af1e"
    token = authentication.Authentication().get_token()
    dss_server = dss_interaction.DSS_Interaction("http://localhost:8082")
    opt_intent_reference = dss_server.retrieve_operational_intent_reference(id, token)


def create_operational_intent_reference(subscriptionId):
    asl_tests = AirspaceLinkTest.AirspacelinkTests()
    airspacelinkresponse = asl_tests.create_test_route()
    jj = airspacelinkresponse.polygon.to_json()

    # create test data
    outline_circle = utility.OutlineCircle(-118.456, 34.123, 300, "M")
    vertex1 = utility.Vertex(34.142604, -118.803964) 
    vertex2 = utility.Vertex(34.146256, -118.801505)
    vertex3 = utility.Vertex(34.143902, -118.800370)
    vertex4 = utility.Vertex(34.142604, -118.803964)
    vectices = utility.Vertices([vertex1, vertex2, vertex3])
    outline_polygon = utility.OutlinePolygon(vectices)

    altitude_lower = utility.Altitude(300, "W84", "M")
    altitude_upper = utility.Altitude(350, "W84", "M")

    # Current time in UTC with 'Z' format
    t_start = datetime.utcnow().replace(microsecond=0)
    t_start_str = t_start.isoformat() + 'Z'  # RFC3339 format string

    # Adding 20 minutes to t_start datetime object
    t_end = t_start + timedelta(minutes=20)
    t_end_str = t_end.isoformat() + 'Z'  # Convert t_end to RFC3339 format string
    
    # Assuming util.Time() accepts RFC3339 formatted string
    time_start = utility.Time(t_start_str) 
    time_end = utility.Time(t_end_str)

    volume = utility.Volume(None, outline_polygon, altitude_lower, altitude_upper) # can only send one geometryType. In this case sending a polygon as this would be closer to a ASL Operational Geometry.
    extents = [utility.Extent(volume, time_start, time_end)] # the interuss description for an extent is the same as an area_of_interest
    keys = []
    state = "Accepted"
    uss_base_url = "https://uss.example.com/utm"
    subscription_id = subscriptionId
    notify_for_constraints = False
    new_subscription = utility.NewSubscription(uss_base_url, notify_for_constraints)
    opt_intent_ref_request = operational_intent_reference.OperationalIntentReferenceRequest(extents, keys, state, uss_base_url, subscription_id, new_subscription)
    my_uuid = uuid.uuid4() # replace this with an actual operational_intent_reference_id

    token = authentication.Authentication().get_token()
    dss_server = dss_interaction.DSS_Interaction("http://localhost:8082")
    operational_intent_reference_response = dss_server.create_operational_intent_reference(opt_intent_ref_request, my_uuid, token)


def update_operational_intent_reference():

    # create test data
    outline_circle = utility.OutlineCircle(-118.456, 34.123, 300, "M")
    vertex1 = utility.Vertex(34.142604, -118.803964) 
    vertex2 = utility.Vertex(34.146256, -118.801505)
    vertex3 = utility.Vertex(34.143902, -118.800370)
    vertex4 = utility.Vertex(34.142604, -118.803964)
    
    vectices = utility.Vertices([vertex1, vertex2, vertex3])
    
    outline_polygon = utility.OutlinePolygon(vectices)
    altitude_lower = utility.Altitude(300, "W84", "M")
    altitude_upper = utility.Altitude(350, "W84", "M")
    volume = utility.Volume(outline_circle, outline_polygon, altitude_lower, altitude_upper)
    # Current time in UTC with 'Z' format
    t_start = datetime.utcnow().replace(microsecond=0)
    t_start_str = t_start.isoformat() + 'Z'  # RFC3339 format string

    # Adding 20 minutes to t_start datetime object
    t_end = t_start + timedelta(minutes=20)
    t_end_str = t_end.isoformat() + 'Z'  # Convert t_end to RFC3339 format string
    
    # Assuming util.Time() accepts RFC3339 formatted string
    time_start = utility.Time(t_start_str) 
    time_end = utility.Time(t_end_str)

    volume = utility.Volume(None, outline_polygon, altitude_lower, altitude_upper)
    extents = [utility.Extent(volume, time_start, time_end)] # the interuss description for an extent is the same as an area_of_interest
    keys = []
    state = "Accepted"
    uss_base_url = "https://uss.example.com/utm"
    subscription_id = "2f8343be-6482-4d1b-a474-16847e01af1e"
    notify_for_constraints = True
    new_subscription = utility.NewSubscription(uss_base_url, notify_for_constraints)
    opt_intent_ref_request = operational_intent_reference.OperationalIntentReferenceRequest(extents, keys, state, uss_base_url, subscription_id, new_subscription)
    ovn = ""

    token = authentication.Authentication().get_token()
    dss_server = dss_interaction.DSS_Interaction("http://localhost:8082")
    operational_intent_reference_response = dss_server.update_operational_intent_reference(opt_intent_ref_request, subscription_id, ovn, token)


def delete_operational_intent_reference():
    uuid = uuid.uuid4() # replace this with an actual operational_intent_reference_id
    ovn = ""

    token = authentication.Authentication().get_token()
    dss_server = dss_interaction.DSS_Interaction("http://localhost:8082")
    operational_intent_reference_response = dss_server.delete_operational_intent_reference(uuid,ovn,token )


# ##################################### ######## #
# ######## CONSTRAINT REFERENCES ######## #
# ##################################### ######## #
    
def query_all_constraint_references():
    # Query All Operational Intent References
    # https://redocly.github.io/redoc/?url=https://raw.githubusercontent.com/astm-utm/Protocol/v1.0.0/utm.yaml#tag/Operational-intent-references/operation/queryOperationalIntentReferences

    # create test data
    outline_circle = utility.OutlineCircle(-118.456, 34.123, 300, "M")

    vertex1 = utility.Vertex(34.142604, -118.803964) 
    vertex2 = utility.Vertex(34.146256, -118.801505)
    vertex3 = utility.Vertex(34.143902, -118.800370)
    vertex4 = utility.Vertex(34.142604, -118.803964)
    vectices = utility.Vertices([vertex1, vertex2, vertex3])
    outline_polygon = utility.OutlinePolygon(vectices)

    altitude_lower = utility.Altitude(300, "W84", "M")
    altitude_upper = utility.Altitude(350, "W84", "M")

    # Current time in UTC with 'Z' format
    t_start = datetime.utcnow().replace(microsecond=0)
    t_start_str = t_start.isoformat() + 'Z'  # RFC3339 format string

    # Adding 20 minutes to t_start datetime object just for a test
    t_end = t_start + timedelta(minutes=20)
    t_end_str = t_end.isoformat() + 'Z'  # Convert t_end to RFC3339 format string
    
    time_start = utility.Time(t_start_str) 
    time_end = utility.Time(t_end_str)

    volume = utility.Volume(None, outline_polygon, altitude_lower, altitude_upper)
    areaofinterest = utility.AreaOfInterest(volume, time_start, time_end)                   

    token = authentication.Authentication().get_token()
    dss_server = dss_interaction.DSS_Interaction("http://localhost:8082")
    constraint_references = dss_server.query_all_constraint_references(areaofinterest, token)


def retrieve_constraint_reference():
    id = "2f8343be-6482-4d1b-a474-16847e01af1e"
    token = authentication.Authentication().get_token()
    dss_server = dss_interaction.DSS_Interaction("http://localhost:8082")
    constraint_reference = dss_server.retrieve_constraint_reference(id, token)


def create_constraint_reference():
    # create test data
    outline_circle = utility.OutlineCircle(-118.456, 34.123, 300, "M")
    vertex1 = utility.Vertex(34.142604, -118.803964) 
    vertex2 = utility.Vertex(34.146256, -118.801505)
    vertex3 = utility.Vertex(34.143902, -118.800370)
    vertex4 = utility.Vertex(34.142604, -118.803964)
    vectices = utility.Vertices([vertex1, vertex2, vertex3])
    outline_polygon = utility.OutlinePolygon(vectices)

    altitude_lower = utility.Altitude(300, "W84", "M")
    altitude_upper = utility.Altitude(350, "W84", "M")

    # Current time in UTC with 'Z' format
    t_start = datetime.utcnow().replace(microsecond=0)
    t_start_str = t_start.isoformat() + 'Z'  # RFC3339 format string

    # Adding 20 minutes to t_start datetime object
    t_end = t_start + timedelta(minutes=20)
    t_end_str = t_end.isoformat() + 'Z'  # Convert t_end to RFC3339 format string
    
    # Assuming util.Time() accepts RFC3339 formatted string
    time_start = utility.Time(t_start_str) 
    time_end = utility.Time(t_end_str)

    volume = utility.Volume(None, outline_polygon, altitude_lower, altitude_upper) # can only send one geometryType. In this case sending a polygon as this would be closer to a ASL Operational Geometry.
    extents = [utility.Extent(volume, time_start, time_end)] # the interuss description for an extent is the same as an area_of_interest
    
    uss_base_url = "https://uss.example.com/utm"
    
    constraint_ref_request = constraint_reference.ConstraintReferenceRequest(extents, uss_base_url)
    uuid = uuid.uuid4() # replace this with an actual operational_intent_reference_id

    token = authentication.Authentication().get_token()
    dss_server = dss_interaction.DSS_Interaction("http://localhost:8082")
    constraint_reference_response = dss_server.create_constraint_reference(uuid, constraint_ref_request, token)


def update_constraint_reference():
 # create test data
    outline_circle = utility.OutlineCircle(-118.456, 34.123, 300, "M")
    vertex1 = utility.Vertex(34.142604, -118.803964) 
    vertex2 = utility.Vertex(34.146256, -118.801505)
    vertex3 = utility.Vertex(34.143902, -118.800370)
    vertex4 = utility.Vertex(34.142604, -118.803964)
    vectices = utility.Vertices([vertex1, vertex2, vertex3])
    outline_polygon = utility.OutlinePolygon(vectices)

    altitude_lower = utility.Altitude(300, "W84", "M")
    altitude_upper = utility.Altitude(350, "W84", "M")

    # Current time in UTC with 'Z' format
    t_start = datetime.utcnow().replace(microsecond=0)
    t_start_str = t_start.isoformat() + 'Z'  # RFC3339 format string

    # Adding 20 minutes to t_start datetime object
    t_end = t_start + timedelta(minutes=20)
    t_end_str = t_end.isoformat() + 'Z'  # Convert t_end to RFC3339 format string
    
    # Assuming util.Time() accepts RFC3339 formatted string
    time_start = utility.Time(t_start_str) 
    time_end = utility.Time(t_end_str)

    volume = utility.Volume(None, outline_polygon, altitude_lower, altitude_upper) # can only send one geometryType. In this case sending a polygon as this would be closer to a ASL Operational Geometry.
    extents = [utility.Extent(volume, time_start, time_end)] # the interuss description for an extent is the same as an area_of_interest
    
    uss_base_url = "https://uss.example.com/utm"
    
    constraint_ref_request = constraint_reference.ConstraintReferenceRequest(extents, uss_base_url)
    uuid = uuid.uuid4() # replace this with an actual operational_intent_reference_id
    ovn = ""

    token = authentication.Authentication().get_token()
    dss_server = dss_interaction.DSS_Interaction("http://localhost:8082")
    constraint_reference_response = dss_server.update_constraint_reference(uuid, ovn, constraint_ref_request, token)


def delete_constraint_reference():
    uuid = uuid.uuid4() # replace this with an actual operational_intent_reference_id
    ovn = ""

    token = authentication.Authentication().get_token()
    dss_server = dss_interaction.DSS_Interaction("http://localhost:8082")
    constraint_reference_response = dss_server.delete_constraint_reference(uuid,ovn,token )


# ##################################### ######## #
# ######## SUBSCRIPTIONS ######## #
# ##################################### ######## #
    
def query_all_subscriptions():
    # Query All Operational Intent References
    # https://redocly.github.io/redoc/?url=https://raw.githubusercontent.com/astm-utm/Protocol/v1.0.0/utm.yaml#tag/Operational-intent-references/operation/queryOperationalIntentReferences

    # create test data
    outline_circle = utility.OutlineCircle(-118.456, 34.123, 300, "M")

    vertex1 = utility.Vertex(34.142604, -118.803964) 
    vertex2 = utility.Vertex(34.146256, -118.801505)
    vertex3 = utility.Vertex(34.143902, -118.800370)
    vertex4 = utility.Vertex(34.142604, -118.803964)
    vectices = utility.Vertices([vertex1, vertex2, vertex3])
    outline_polygon = utility.OutlinePolygon(vectices)

    altitude_lower = utility.Altitude(300, "W84", "M")
    altitude_upper = utility.Altitude(350, "W84", "M")

    # Current time in UTC with 'Z' format
    t_start = datetime.utcnow().replace(microsecond=0)
    t_start_str = t_start.isoformat() + 'Z'  # RFC3339 format string

    # Adding 20 minutes to t_start datetime object just for a test
    t_end = t_start + timedelta(minutes=20)
    t_end_str = t_end.isoformat() + 'Z'  # Convert t_end to RFC3339 format string
    
    time_start = utility.Time(t_start_str) 
    time_end = utility.Time(t_end_str)

    volume = utility.Volume(None, outline_polygon, altitude_lower, altitude_upper)
    areaofinterest = utility.AreaOfInterest(volume, time_start, time_end)                 

    token = authentication.Authentication().get_token()
    dss_server = dss_interaction.DSS_Interaction("http://localhost:8082")
    subscriptions = dss_server.query_all_subscriptions(areaofinterest, token)
    # print(subscriptions)


def retrieve_subscription():
    id = "2f8343be-6482-4d1b-a474-16847e01af1e"
    token = authentication.Authentication().get_token()
    dss_server = dss_interaction.DSS_Interaction("http://localhost:8082")
    subscriptions = dss_server.retrieve_subscription(id, token)


def create_subscription():
    # create test data
    outline_circle = utility.OutlineCircle(-118.456, 34.123, 300, "M")
    vertex1 = utility.Vertex(34.142604, -118.803964) 
    vertex2 = utility.Vertex(34.146256, -118.801505)
    vertex3 = utility.Vertex(34.143902, -118.800370)
    vertex4 = utility.Vertex(34.142604, -118.803964)
    vectices = utility.Vertices([vertex1, vertex2, vertex3])
    outline_polygon = utility.OutlinePolygon(vectices)

    altitude_lower = utility.Altitude(300, "W84", "M")
    altitude_upper = utility.Altitude(350, "W84", "M")

    # Current time in UTC with 'Z' format
    t_start = datetime.utcnow().replace(microsecond=0)
    t_start_str = t_start.isoformat() + 'Z'  # RFC3339 format string

    # Adding 20 minutes to t_start datetime object
    t_end = t_start + timedelta(minutes=20)
    t_end_str = t_end.isoformat() + 'Z'  # Convert t_end to RFC3339 format string
    
    # Assuming util.Time() accepts RFC3339 formatted string
    time_start = utility.Time(t_start_str) 
    time_end = utility.Time(t_end_str)

    volume = utility.Volume(None, outline_polygon, altitude_lower, altitude_upper) # can only send one geometryType. In this case sending a polygon as this would be closer to a ASL Operational Geometry.
    extents = [utility.Extent(volume, time_start, time_end)] # the interuss description for an extent is the same as an area_of_interest
    
    uss_base_url = "https://uss.example.com/utm"
    notify_for_operational_intents = True
    notify_for_constraints = True
    
    subscription_request = subscription.SubscriptionRequest(extents, uss_base_url, notify_for_operational_intents, notify_for_constraints)
    uuid = uuid.uuid4() # replace this with an actual operational_intent_reference_id

    token = authentication.Authentication().get_token()
    dss_server = dss_interaction.DSS_Interaction("http://localhost:8082")
    subscription = dss_server.create_subscription(subscription_request, token)


def update_subscription():
 # create test data
    outline_circle = utility.OutlineCircle(-118.456, 34.123, 300, "M")
    vertex1 = utility.Vertex(34.142604, -118.803964) 
    vertex2 = utility.Vertex(34.146256, -118.801505)
    vertex3 = utility.Vertex(34.143902, -118.800370)
    vertex4 = utility.Vertex(34.142604, -118.803964)
    vectices = utility.Vertices([vertex1, vertex2, vertex3])
    outline_polygon = utility.OutlinePolygon(vectices)

    altitude_lower = utility.Altitude(300, "W84", "M")
    altitude_upper = utility.Altitude(350, "W84", "M")

    # Current time in UTC with 'Z' format
    t_start = datetime.utcnow().replace(microsecond=0)
    t_start_str = t_start.isoformat() + 'Z'  # RFC3339 format string

    # Adding 20 minutes to t_start datetime object
    t_end = t_start + timedelta(minutes=20)
    t_end_str = t_end.isoformat() + 'Z'  # Convert t_end to RFC3339 format string
    
    # Assuming util.Time() accepts RFC3339 formatted string
    time_start = utility.Time(t_start_str) 
    time_end = utility.Time(t_end_str)

    volume = utility.Volume(None, outline_polygon, altitude_lower, altitude_upper) # can only send one geometryType. In this case sending a polygon as this would be closer to a ASL Operational Geometry.
    extents = [utility.Extent(volume, time_start, time_end)] # the interuss description for an extent is the same as an area_of_interest
    
    uss_base_url = "https://uss.example.com/utm"
    uss_base_url = "https://uss.example.com/utm"
    notify_for_operational_intents = True
    notify_for_constraints = True

    subscription_id = ""
    version = 0
    
    subscription_request = subscription.SubscriptionRequest(extents, uss_base_url, notify_for_operational_intents, notify_for_constraints)
    uuid = uuid.uuid4() # replace this with an actual operational_intent_reference_id
    ovn = ""

    token = authentication.Authentication().get_token()
    dss_server = dss_interaction.DSS_Interaction("http://localhost:8082")
    subscription = dss_server.update_subscription(subscription_id, version, subscription_request, token)


def delete_subscription():
    uuid = uuid.uuid4() # replace this with an actual operational_intent_reference_id
    version = "1"

    token = authentication.Authentication().get_token()
    dss_server = dss_interaction.DSS_Interaction("http://localhost:8082")
    subscription = dss_server.delete_subscription(uuid, version, token )



if __name__ == '__main__':
    # OPERATIONAL INTENT REFERENCE
    create_operational_intent_reference()
    query_all_operational_intent_references()
    retrieve_operational_intent_reference()
    update_operational_intent_reference()
    delete_operational_intent_reference()

    # CONSTRAINT
    create_constraint_reference()
    query_all_constraint_references()
    retrieve_constraint_reference()
    update_constraint_reference()
    delete_constraint_reference()

    # SUBSCRIPTION
    create_subscription()
    query_all_subscriptions()
    retrieve_subscription()
    update_subscription()
    delete_subscription()