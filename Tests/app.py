import threading

import sys
from pathlib import Path


sys.path.append(str(Path(__file__).resolve().parent.parent))
from USS.uss_interaction import USS_Interaction

import requests
import urllib3
from urllib3.exceptions import InsecureRequestWarning


# Disable SSL verification globally (dev only!)
urllib3.disable_warnings(InsecureRequestWarning)

# Make all requests ignore SSL by default
old_request = requests.Session.request
def patched_request(self, *args, **kwargs):
    kwargs.setdefault('verify', False)
    return old_request(self, *args, **kwargs)
requests.Session.request = patched_request

import json
import uuid
import os
from functools import wraps
from typing import List

from flask import Flask, render_template, request, jsonify
import psycopg2
import jwt
from datetime import datetime, timedelta

# import pdb
# import debugpy

from AirspaceLink_API.advisories import Geometry, GeometryType, PolygonGeometry
from AirspaceLink_API.operations import Operation, Operation_Properties, Operational_Feature
from AirspaceLink_API.authentication import Authentication
from DSS.subscription import USS_Subscription
from USS.constaint_details import Constraint, ConstraintDetails
from DSS.operational_intent_reference import OperationalIntentReference
from USS.operational_intent_details import OperationalIntentOffNominal, OperationalIntentDetails
from Utility.utility import Message, NewSubscription, OperationalIntentStatus, Reference, Subscription, Extent, TimeRange, Volume, OutlinePolygon, Vertex, Vertices, TimeMeasured, Altitude, StartEndTime, AltitudeRange
import TimestampValidator
import AirspaceLinkTest
from AirspaceLink_API.stop import Stop
from dss_interaction import MainProcessor
from DSS.authentication import Authentication, UtmScope
from dss_interaction import ApiException, DSS_Interaction, SubscriptionRequest

import logging
from logging.handlers import RotatingFileHandler

app = Flask(__name__)
app.logger.setLevel(logging.INFO)  # Set log level to INFO or DEBUG

# Create a file handler and set its log level
file_handler = RotatingFileHandler('flask.log', maxBytes=1024*1024, backupCount=10)
file_handler.setLevel(logging.INFO)  # Set log level to INFO or DEBUG

# Create a formatter and set it on the file handler
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)

# Add the file handler to the Flask app logger
app.logger.addHandler(file_handler)

lock = threading.Lock()
SECRET_KEY = "your_secret_key"  # Replace with your actual secret key
SECRET_KEY = os.environ.get("SECRET_KEY", "default_secret_key")

_operationa_intent_references = {}


@app.route('/')
def home():
    return "Welcome to the AirspaceLink InterUSS Web Application"


@app.route('/route_map')
def index():
    return render_template('index.html')


@app.route('/get_asl_route', methods=['POST'])
def get_route():
    data = request.get_json()

    print('\n' * 100) 

    if 'polyline' in data:
        stops = []
        polyline = data['polyline']
        use_asl = data['userASL']
        print('')
        print('')
        print("MAP RESPONSE")
        print(polyline)
        paths_list = polyline['paths']
        coords = []
        for index, path in enumerate(paths_list):
            for coordinates in path:
                longitude, latitude, value = coordinates
                stop = Stop(latitude, longitude)
                coords.append([longitude, latitude])
                stops.append(stop)

        url = "https://EdanTest.com"
        asl_tests = AirspaceLinkTest.AirspacelinkTests()

        print("")
        print("AirspaceLink Requests: Route, Operation")
        with lock:
            if use_asl:
                airspacelink_response = asl_tests.create_test_route(stops)
                url = airspacelink_response.url
                polygon = airspacelink_response.polygon
                route = airspacelink_response.route
                network = airspacelink_response.routeV2Response.network
                hexes = airspacelink_response.routeV2Response.hex_geojson

                print("")
                print("Hexes")
                print()
                print(hexes)
                response_data = {
                    'url': url,
                    'airspacelink_route': route.to_json(),
                    'operation_polygon': polygon.to_json(),
                    'network': network.to_json(),
                    'hexes': hexes
                }
                if airspacelink_response is None:
                    error_message = "An error occurred"
                    return jsonify(error=error_message, status_code=503), 503
        
            else:
                polygon = asl_tests.buffer_simple_line(coords, 0.001)
                response_data = {
                    'url': "",
                    'airspacelink_route': "",
                    'operation_polygon': polygon.to_json(),
                    'network': "",
                    'hexes': ""
                }

        try:
            json_data = jsonify(response_data)
        except Exception as ex:
            print(ex)

        return json_data

@app.route('/create_dss_subscription', methods=['POST'])
def dss_subscription():
    data = request.get_json()
    polygon_object = None
    start_time = None
    end_time = None
    flight_duration = None
    
    if 'polygon' in data:
        polygon_rings = data["polygon"]["rings"]
        polygon_object = PolygonGeometry(polygon_rings[0])
    else:
        return
    
    if 'start_time' in data:
        start_time = data['start_time']
        
    if 'end_time' in data:
        end_time = data['end_time']

    if 'flight_duration' in data:
        flight_duration = data['flight_duration']

    dss_instance = DSS_Interaction("http://localhost:8082")
    token = Authentication().get_token([UtmScope.STRATEGIC_COORDINATION.value, UtmScope.CONSTRAINT_PROCESSING.value, UtmScope.CONSTRAINT_MANAGEMENT.value, UtmScope.CONFORMANCE_MONITORING_SA.value])

    # uss_instance = USS_Interaction()
    date_time_obj = datetime.strptime(start_time, '%Y-%m-%dT%H:%M')
    time_range = StartEndTime.from_to_time(date_time_obj, flight_duration)
    altitude_range = AltitudeRange(Altitude(1897, "W84", "M"), Altitude(2000, "W84", "M"))
 
    uid = uuid.uuid4()
    url = "https://edantest.com"
    
    extent = MainProcessor.build_extent(polygon_object, time_range, altitude_range)
    subscription_response = MainProcessor.create_subscription(dss_instance, extent, uid, url, None, token)

    response_data = ''

    if isinstance(subscription_response, ApiException):
        response_data = {
            f"API error {subscription_response.status_code}: {subscription_response}",
            f"Message: {subscription_response.message}: {subscription_response}"
        }
    else:
        data = subscription_response.to_json()
        response_data = {
            'subscription_response': data
        }

    try:
        return jsonify(response_data)
    except Exception as ex:
        print(ex)

    return response_data

        
@app.route('/create_dss_constraint', methods=['POST'])
def dss_constaint():
    # Create Constraints
    data = request.get_json()
    polygon_object = None
    start_time = None
    end_time = None
    flight_duration = None
    ovns = []
    extents = []
    stops = []
    time_range = None
    altitude_range = AltitudeRange(Altitude(1897, "W84", "M"), Altitude(2000, "W84", "M"))
    
    if 'polyline' in data:
        polyline = data["polyline"]
    else:
        return
    
    if 'start_time' in data:
        start_time = data['start_time']
        
    if 'end_time' in data:
        end_time = data['end_time']

    if 'flight_duration' in data:
        flight_duration = data['flight_duration']

    dss_instance = DSS_Interaction("http://localhost:8082")
    token = Authentication().get_token([UtmScope.STRATEGIC_COORDINATION.value, UtmScope.CONSTRAINT_PROCESSING.value, UtmScope.CONSTRAINT_MANAGEMENT.value, UtmScope.CONFORMANCE_MONITORING_SA.value])

    date_time_obj = datetime.strptime(start_time, '%Y-%m-%dT%H:%M')
    time_range = StartEndTime.from_to_time(date_time_obj, flight_duration)

    extents = extents_from_route(polyline, time_range, altitude_range)

    uid = uuid.uuid4()
    url = "https://edantest.com"

    constraint_reference_response = MainProcessor.create_constraint_reference(dss_instance, None, extents, uid, url, token)
    ovns.append(constraint_reference_response.constraint_reference.ovn)

    if len(constraint_reference_response.subscribers) > 0:
        # DSS subscribers that this client now has the obligation to notify of the constraint changes just made. 
        # This client must call POST for each provided URL according to the USS-USS /uss/v1/constraints path API. The client's own subscriptions will also be included in this list.
        pass

def extents_from_route(polyline, time_range: TimeRange, altitude_range: AltitudeRange) -> []:
    extents = []
    paths_list = polyline['paths']
    for index, path in enumerate(paths_list):
        for i in range(len(path) - 1):
            coords = []
            for coordinates in path[i:i+2]:
                if len(coordinates) < 3:
                    continue
                    
                longitude, latitude, altitude = coordinates
                coords.append([longitude, latitude])

    polygon_geom = AirspaceLinkTest.AirspacelinkTests.buffer_simple_line(coords, 0.0005)
    waypoints_extent = MainProcessor.build_extent(polygon_geom, time_range, altitude_range)
    extents.append(waypoints_extent)

    return extents

@app.route('/create_dss_operational_intents', methods=['POST'])
def dss_operational_intent_references():
        # Create Constraints
    data = request.get_json()
    polygon_object = None
    start_time = None
    end_time = None
    flight_duration = None
    keys = [] # ovns maybe
    extents = []
    time_range = None
    altitude_range = AltitudeRange(Altitude(1897, "W84", "M"), Altitude(2000, "W84", "M"))
    
    if 'polyline' in data:
        polyline = data["polyline"]
    else:
        return
    
    if 'start_time' in data:
        start_time = data['start_time']
        
    if 'end_time' in data:
        end_time = data['end_time']

    if 'flight_duration' in data:
        flight_duration = data['flight_duration']

    if 'subscription_id' in data:
        subscription_id = None # data['subscription_id']

    if 'keys' in data:
        keys = data['keys']

    dss_instance = DSS_Interaction("http://localhost:8082")
    token = Authentication().get_token([UtmScope.STRATEGIC_COORDINATION.value, UtmScope.CONSTRAINT_PROCESSING.value, UtmScope.CONSTRAINT_MANAGEMENT.value, UtmScope.CONFORMANCE_MONITORING_SA.value])

    date_time_obj = datetime.strptime(start_time, '%Y-%m-%dT%H:%M')
    time_range = StartEndTime.from_to_time(date_time_obj, flight_duration)

    extents = extents_from_route(polyline, time_range, altitude_range)

    uid = uuid.uuid4()
    url = "https://www.edantest.com"

    new_subscription = NewSubscription(url, True)

    operational_intent_ref_response = MainProcessor.create_operational_intent_ref(dss_instance, extents, keys, OperationalIntentStatus.ACCEPTED.value, url, subscription_id, new_subscription, uid, token)
    response_data = ''
    
    if isinstance(operational_intent_ref_response, ApiException):
        if(operational_intent_ref_response.status_code == 409):
            message_json_str = operational_intent_ref_response.message
            message_data = json.loads(message_json_str)
            message_message = message_data.get('message', '')
            missing_operational_intents = message_data.get('missing_operational_intents', [])

            response_data = {
                "status_code": operational_intent_ref_response.status_code,
                "message": message_message,
                "missing operational intents": missing_operational_intents
            }
        else:
            response_data = {
                "status_code": operational_intent_ref_response.status_code,
                "message": operational_intent_ref_response.message,
                "missing operational intents": "Failed to create Operational Intent Reference"
            }
    else:
        add_operational_intent_ref(operational_intent_ref_response.operational_intent_reference)
        data = operational_intent_ref_response.to_json()
        response_data = {
            'operational_intent_ref_response': data,
            'extents': [extent.to_json() for extent in extents],
            'polyline': polyline
        }

    try:
        return jsonify(response_data)
    except Exception as ex:
        print(ex)
        print(response_data)

    return response_data

@app.route('/get_operational_intents', methods=['POST'])
def get_operational_intent_reference():
        # Create Constraints
    data = request.get_json()
    id = data["id"]
    operational_intent = get_operational_intent_ref(id)

    if operational_intent != None:
        response_data = {
            'operational_intent_ref_response': operational_intent.to_json()
        }

        try:
            return jsonify(response_data)
        except:
            print("exception here")
    else:
        return None
    

def add_operational_intent_ref(ref: OperationalIntentReference):
    _operationa_intent_references[ref.id] = ref

def get_operational_intent_ref(id) -> OperationalIntentReference:
    if id in _operationa_intent_references:
        desired_ref = _operationa_intent_references[id]
        return desired_ref
    else:
        return None

# Database connection
def get_db_connection():
    return psycopg2.connect(
        dbname=os.environ.get('DB_NAME', 'uss_postgres'),
        user=os.environ.get('DB_USER', 'root'),
        password=os.environ.get('DB_PASSWORD', 'root'),
        host=os.environ.get('DB_HOST', 'db'),
        port=os.environ.get('DB_PORT', '5432')
    )


# Token verification decorator
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'message': 'Token is missing!'}), 401

        try:
            jwt.decode(token.split(" ")[1], SECRET_KEY, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired!'}), 401
        except jwt.InvalidTokenError as e:
            print(f"Invalid token error: {e}")  # Debug print
            return jsonify({'message': 'Invalid token!'}), 401
        except Exception as e:
            print(f"General error: {e}")  # Debug print
            return jsonify({'message': 'Token error'}), 401

        return f(*args, **kwargs)
    return decorated


@app.route('/oauth/token', methods=['POST'])
def authenticate():
    username = request.json.get('username')
    password = request.json.get('password')

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
    user = cur.fetchone()
    cur.close()
    conn.close()

    if user:
        token = jwt.encode({
            'username': username,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
        }, SECRET_KEY, algorithm="HS256")

        return jsonify({'token': token}), 200
    else:
        return jsonify({"error": "Invalid credentials"}), 401

# Testing ASL Callbacks
    # +++++++++++++++++++++++++++++
@app.route('/aslCallback/<string:operation_id>', methods=['POST'])
def asl_callback(operation_id):
    # Retrieve the JSON data from the request
    json_data = request.get_json()

    # Process the received data as needed
    # For example, you can save it to a database, log it, etc.

    # Respond with a success message
    return jsonify({"message": f"Callback received for operation ID: {operation_id}"}), 200

@app.route('/request_operation', methods=['GET'])
def request_operation():
    # Create instances of Operational_Feature and Operation_Properties
    # Generate a unique ID for the operati    operation_id = str(uuid.uuid4())
    # Prepare the callback URL with the unique ID
    operation_id = str(uuid.uuid4())
    _callback_url = f"https://e271-2406-2d40-72ab-5910-902-dee6-d0a0-af4c.ngrok-free.app/aslCallback/{operation_id}"

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
    return response

    # +++++++++++++++++++++++++++++



# TEST Example protected route requiring a valid token
@app.route('/protected', methods=['GET'])
@token_required
def protected():
    return jsonify({'message': 'This is only available for people with valid tokens.'})


# ============ AirspaceLink
@app.route('/uss/v1/airspacelink_operations', methods=['POST'])  # TODO rename this
@token_required
def create_uss_subscription():
    data = request.json

    # Check if uas_id is provided and not empty
    uas_id = data.get('uas_id')
    if not uas_id:
        uas_id = str(uuid.uuid4())

    # Extracting other fields from the request
    pilot_name = data['pilot_name']
    pilot_phone = data['pilot_phone']
    start_time = data['time_start']['value']  # Extract the timestamp string
    end_time = data['time_end']['value']      # Extract the timestamp string
    altitude_upper = data['altitude_upper']['value']

    conn = get_db_connection()
    cur = conn.cursor()

    try:
        # Check if subscription_id already exists
        cur.execute("SELECT * FROM pilot_routes WHERE uas_id = %s", (uas_id,))
        if cur.fetchone():
            # Update the existing record
            cur.execute("""
                UPDATE pilot_routes SET 
                pilot_name = %s, 
                pilot_phone = %s,
                time_start = %s, 
                time_end = %s
                WHERE uas_id = %s
            """, (pilot_name, pilot_phone, start_time, end_time, uas_id))

            #CREATE A SUBSCRIPTION FOR DSS
            dss_token = Authentication.get_token()
            dss_subsciption_interaction = DSS_Subscription_Interaction("http://localhost:8085/token")
            subscription_response = dss_subsciption_interaction.create_subscription(uas_id, data, dss_token)
        else:
            # Insert a new record
            cur.execute("""
                INSERT INTO pilot_routes (
                    uas_id, 
                    pilot_name,       
                    pilot_phone, 
                    time_start, 
                    time_end
                ) VALUES (%s, %s, %s, %s, %s)
            """, (uas_id, pilot_name, pilot_phone, start_time, end_time))

        conn.commit()
        return jsonify({"AirspaceLink_message": "Airspacelink Operation successful", "subscription_id": uas_id, "Subscription_Response": subscription_response}), 200
    except psycopg2.Error as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        cur.close()
        conn.close()


# ========= USS STATUS ===========

@app.route('/uss/v1/status', methods=['GET'])
@token_required
def status():
    # Retrieves the status of the USS's automated testing interface for flight planning.
    return jsonify({"message": "AirspaceLink USS: Operational"})


# ========= Operational Intents ===================

@app.route('/uss/v1/operational_intents/<entity_id>', methods=['GET'])
@token_required
# The USS hosting this endpoint returns the details (and reference) of an operational intent it manages. While the USS has a pending request to change the operational intent
# in the DSS, the USS should report the most recent version the USS knows was accepted by the DSS. So, before a USS receives a response to create an operational intent
# reference in the DSS, it should return 404 if queried for that operational intent at this endpoint.
# https://redocly.github.io/redoc/?url=https://raw.githubusercontent.com/astm-utm/Protocol/v1.0.0/utm.yaml#tag/Operational-intent-details/operation/getOperationalIntentDetails

def get_operational_intent_details(entity_id):
    conn = get_db_connection()
    cur = conn.cursor()

    # Query the operational_intent table
    # SQL query to fetch the data
    query = """
    SELECT oir.*, t.time_start, t.time_end
    FROM OperationalIntentReference oir
    LEFT JOIN Time t ON oir.id = t.operational_intent_reference_id
    WHERE oir.id = %s;
    """

    cur.execute(query, (entity_id,))
    operational_intent_data = cur.fetchone()

    if not operational_intent_data:
        return jsonify({"error": "Operational intent not found"}), 404

    response = OperationalIntentDetails.build_operational_intent_json(operational_intent_data)

    cur.close()
    conn.close()

    return jsonify(response), 200


@app.route('/uss/v1/operational_intents/<entity_id>/telemetry', methods=['GET'])
@token_required
# Query detailed information on the position of an off-nominal operational intent from a USS.
# https://redocly.github.io/redoc/?url=https://raw.githubusercontent.com/astm-utm/Protocol/v1.0.0/utm.yaml#tag/Operational-intent-details/operation/getOperationalIntentTelemetry
def operational_intents_telemetry(entity_id):
    conn = get_db_connection()
    cur = conn.cursor()

    try:
        # Query OperationalIntent table
        cur.execute("SELECT * FROM OperationalIntent WHERE reference_id = %s", (entity_id,))
        operational_intent_data = cur.fetchone()

        if not operational_intent_data:
            return jsonify({"error": "Operational intent not found"}), 404

        # Query Telemetry table
        cur.execute("SELECT * FROM Telemetry WHERE operational_intent_id = %s", (entity_id,))
        telemetry_data = cur.fetchone()

        if not telemetry_data:
            return jsonify({"error": "Telemetry data not found"}), 404

        # Construct the response
        response = OperationalIntentOffNominal.build_operation_intent_off_nominal(entity_id, operational_intent_data, telemetry_data)

    except Exception as e:
        # Handle exceptions
        return jsonify({"error": str(e)}), 500
    finally:
        cur.close()
        conn.close()

    return jsonify(response), 200


@app.route('/uss/v1/operational_intents', methods=['POST'])
@token_required
# Notify a peer USS directly of changed operational intent details (usually as a requirement of previous interactions with the DSS).
# https://redocly.github.io/redoc/?url=https://raw.githubusercontent.com/astm-utm/Protocol/v1.0.0/utm.yaml#tag/Operational-intent-details/operation/notifyOperationalIntentDetailsChanged
def create_or_update_operational_intent():
    data = request.json
    operational_intent_id = data['operational_intent_id']  # ID of operational intent that has changed.
    operational_intent = OperationalIntentDetails(data['operational_intent'])
    subscriptions = List[USS_Subscription(data['subscriptions'])]

    # operational_intent_id, required
    # EntityID (UUIDv4Format (string)), ID of operational intent that has changed.

    # operational_intent	
    # OperationalIntent (object) Full information about the operational intent that has changed. If this field is omitted, the operational intent was deleted. The ovn field in the nested reference must be populated.

    # subscriptions, required. Array of objects (SubscriptionState) non-empty. Subscription(s) prompting this notification.
    # TODO, might need a check in here to make sure we have an alignment between subscriptions, the operational intent subscription and teh operational_intent_id. Seems wasteful to have this value in so many places.

    conn = get_db_connection()
    cur = conn.cursor()

    # Check if the subscription_id exists in the subscriptions table
    # TODO: iterate the subscriptions being asked for. The ISSUE is with the USS and DSS classification of a structure for a Subscription. I have added a request type structure for Subscriptions which is
    # an object containing ONLY the subscription_id and the notification_index. I am not going to create another table for this structure, we can pull the relevant pieces from the Subscription Table. 
    # Update OperationalIntent
    cur.execute("""
        UPDATE OperationalIntent
        SET manager = %s,
            uss_availability = %s,
            version = %s,
            state = %s,
            ovn = %s,
            time_start = %s,
            time_end = %s,
            uss_base_url = %s,
            subscription_id = %s
        WHERE id = %s;
        """,
        (
            operational_intent.reference.manager,
            operational_intent.reference.uss_availability,
            operational_intent.reference.version,
            operational_intent.reference.state,
            operational_intent.reference.ovn,
            operational_intent.reference.time_start.value,
            operational_intent.reference.time_end.value,
            operational_intent.reference.uss_base_url,
            operational_intent.reference.subscription_id,
            operational_intent_id
        )
    )

    conn.commit()
    cur.close()
    conn.close()

    return jsonify({"message": "New or updated full operational intent information received successfully."}), 204

# ======== Constraints =================

@app.route('/uss/v1/constraints', methods=['POST'])
@token_required
# Notify a peer USS of changed constraint details.
# Notify a peer USS directly of changed constraint details (usually as a requirement of previous interactions with the DSS).
# https://redocly.github.io/redoc/?url=https://raw.githubusercontent.com/astm-utm/Protocol/v1.0.0/utm.yaml#tag/Constraint-details/operation/notifyConstraintDetailsChanged
def constraints():
    data = request.json
    constraint_id = data['constraint_id']  # ID of constraint_id that has changed.
    constraint = Constraint(data['constraint']['reference'], data['constraint']['details'])
    
    subscriptions = List[USS_Subscription(data['subscriptions'])]

    conn = get_db_connection()
    cur = conn.cursor()

    # Process constraint data
    # Assuming you have a function to process and update constraint details
    cur.execute("""
        UPDATE constraints_table
        SET reference_id = %s, 
            details_id = %s,
            ...
        WHERE id = %s;
    """, (
        constraint.reference.id,
        constraint.reference.id,
        ...,
        constraint_id
    ))

    cur.execute("""
        UPDATE Reference
        SET manager = %s,
            uss_availability = %s,
            version = %s,
            ovn = %s,
            time_start = %s,
            time_end = %s,
            uss_base_url = %s
        WHERE id = %s;
    """, (
        constraint.reference.manager,
        constraint.reference.uss_availability,
        constraint.reference.version,
        constraint.reference.ovn,
        constraint.reference.time_start.value,
        constraint.reference.time_end.value,
        constraint.reference.uss_base_url,
        constraint.reference.id
    ))

    # Process subscriptions
    # for sub_data in subscriptions_data:
    #    process_subscription(cur, sub_data)

    conn.commit()
    cur.close()
    conn.close()

    return jsonify({"message": "New or updated full constraint information received successfully."}), 204
    



@app.route('/uss/v1/constraints/<entity_id>', methods=['GET'])
@token_required
# The USS hosting this endpoint returns the details (and reference) of a constraint it manages. While the USS has a pending request to change the constraint
# in the DSS, the USS should report the most recent version the USS knows was accepted by the DSS. So, before a USS receives a response to create a constraint
# reference in the DSS, it should return 404 if queried for that constraint at this endpoint.
# https://redocly.github.io/redoc/?url=https://raw.githubusercontent.com/astm-utm/Protocol/v1.0.0/utm.yaml#tag/Constraint-details/operation/getConstraintDetails
def get_constraints(entity_id):
    conn = get_db_connection()
    cur = conn.cursor()

    # Query the operational_intent table
    # SQL query to fetch the data
    query = """
    SELECT cr.*, t.time_start, t.time_end
    FROM ConstraintReference cr
    LEFT JOIN Time t ON oir.id = t.constraint_reference_id
    WHERE cr.id = %s;
    """

    cur.execute(query, (entity_id,))
    constraint_details_data = cur.fetchone()

    if not constraint_details_data:
        return jsonify({"error": "Operational intent not found"}), 404

    constraint_details = ConstraintDetails(constraint_details_data)
    response = constraint_details.to_json()

    cur.close()
    conn.close()

    return jsonify(response), 200


# ========= Reports =====================

@app.route('/uss/v1/reports', methods=['POST'])
@token_required
# Notify USS of an error encountered that might otherwise go unnoticed.
# Endpoint to provide feedback (errors, etc.) that might otherwise go unnoticed by this USS. This endpoint is used for all feedback related to operational intents and constraints.
# https://redocly.github.io/redoc/?url=https://raw.githubusercontent.com/astm-utm/Protocol/v1.0.0/utm.yaml#tag/Reports/operation/makeUssReport
def reports():
    data = request.json
    report_id = data["report_id"]



# ======== Logging =====================

@app.route('/uss/v1/log_sets/<log_set_id>', methods=['GET'])
@token_required
# Logging
# Pseudo-endpoints not intended to be implemented literally, but rather to illustrate logging data formats
# Get USS logs
# A USS will not usually implement this endpoint directly, but rather will be capable of exporting log data in a format equivalent to the response format of this pseudo-endpoint according to the requirements of the standard.
# https://redocly.github.io/redoc/?url=https://raw.githubusercontent.com/astm-utm/Protocol/v1.0.0/utm.yaml#tag/Logging
def get_uss_logs(log_set_id):
    test = ""




################ FOR DISCUSSION ##########################

# N.B:
# https://github.com/interuss/automated_testing_interfaces/tree/main

# ======== Flight Planning =============
# https://github.com/interuss/automated_testing_interfaces/tree/main/flight_planning

@app.route('/uss/v1/clear_area_requests', methods=['POST'])
@token_required
def clear_area_requests():
    # Requests that the USS cancel and remove all flight plans in a specified area.
    return jsonify({"message": "TODO: Requests that the USS cancel and remove all flight plans in a specified area"})


@app.route('/uss/v1/flight_plans/<flight_plan_id>', methods=['PUT'])
@token_required
def flight_plan(flight_plan_id):
    data = request.json

    if flight_plan_id is None:
        flight_plan_id = str(uuid.uuid4())

    conn = get_db_connection()
    cur = conn.cursor()

    # Check if the flight plan already exists
    cur.execute("SELECT * FROM basic_flight_plans WHERE flight_plan_id = %s", (flight_plan_id,))
    existing_plan = cur.fetchone()

    if existing_plan:
        # Update existing flight plan
        cur.execute("""
            UPDATE basic_flight_plans SET 
            uas_id = %s, operator_id = %s, plan_intent = %s, 
            start_time = %s, end_time = %s, flight_path = %s, 
            cruising_altitude = %s, cruising_speed = %s, communication_info = %s,
            usage_state = %s, uas_state = %s, flight_area = %s, 
            execution_style = %s, extent = %s, success = %s, 
            flight_plan_status = %s, planning_result = %s
            WHERE flight_plan_id = %s
        """, (
            data.get('uas_id'), data.get('operator_id'), data.get('plan_intent'),
            data.get('start_time'), data.get('end_time'), data.get('flight_path'),
            data.get('cruising_altitude'), data.get('cruising_speed'), data.get('communication_info'),
            data.get('usage_state'), data.get('uas_state'), data.get('flight_area'),
            data.get('execution_style'), data.get('extent'), data.get('success'),
            data.get('flight_plan_status'), data.get('planning_result'), flight_plan_id
        ))
    else:
        # Insert new flight plan
        cur.execute("""
            INSERT INTO basic_flight_plans (
                flight_plan_id, uas_id, operator_id, plan_intent, 
                start_time, end_time, flight_path, cruising_altitude, 
                cruising_speed, communication_info, usage_state, 
                uas_state, flight_area, execution_style, extent, 
                success, flight_plan_status, planning_result
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            flight_plan_id, data.get('uas_id'), data.get('operator_id'), data.get('plan_intent'),
            data.get('start_time'), data.get('end_time'), data.get('flight_path'),
            data.get('cruising_altitude'), data.get('cruising_speed'), data.get('communication_info'),
            data.get('usage_state'), data.get('uas_state'), data.get('flight_area'),
            data.get('execution_style'), data.get('extent'), data.get('success'),
            data.get('flight_plan_status'), data.get('planning_result')
        ))

    conn.commit()
    cur.close()
    conn.close()

    return jsonify({"message": "Flight plan processed", "flight_plan_id": flight_plan_id})


@app.route('/uss/v1/flight_plans/<flight_plan_id>', methods=['DELETE'])
@token_required
def delete_flight_plan(flight_plan_id):
    # Submits a new or updated flight plan (upserts a flight plan).

    conn = get_db_connection()
    cur = conn.cursor()

    # Check if the flight plan exists
    cur.execute("SELECT * FROM basic_flight_plans WHERE flight_plan_id = %s", (flight_plan_id,))
    flight_plan = cur.fetchone()

    if flight_plan:
        # Flight plan exists, proceed with deletion
        cur.execute("DELETE FROM basic_flight_plans WHERE flight_plan_id = %s", (flight_plan_id,))
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({"message": "Flight plan successfully deleted."})
    else:
        # Flight plan does not exist
        cur.close()
        conn.close()
        return jsonify({"message": "Flight plan for: " + str(flight_plan_id) + " does not exist"})

# ======== Geo-Awareness ==============
# https://github.com/interuss/automated_testing_interfaces/tree/main/geo-awareness

# ======== Geospatial Map =============
# https://github.com/interuss/automated_testing_interfaces/tree/main/geo-awareness

# ======== Remote ID ==================
# https://github.com/interuss/automated_testing_interfaces/tree/main/rid

# ======== Versioning =================
# https://github.com/interuss/automated_testing_interfaces/tree/main/versioning

# ======== End ==================

if __name__ == '__main__':
    #ptvsd.enable_attach(address=('localhost', 5679), redirect_output=False)
    # debugpy.listen(('0.0.0.0', 5678))
    app.run(debug=True, threaded=True) 
