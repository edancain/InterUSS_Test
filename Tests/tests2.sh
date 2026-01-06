def test_area():
    timestamp = "2023-11-16T21:00:00Z"
    if TimestampValidator.is_rfc3339(timestamp):
        print(f"The timestamp {timestamp} is in RFC 3339 format.")
    else:
        print(f"The timestamp {timestamp} is not in RFC 3339 format.")


def create_subscription(data): # json data
    # data = request.json
    subscription_id = str(uuid.uuid4())
    extent_id = str(uuid.uuid4())  # Generate a unique ID for the extent

    # Extract common extent data
    altitude_lower = data['extents']['volume']['altitude_lower']['value']
    altitude_upper = data['extents']['volume']['altitude_upper']['value']

    # Determine if the extent is a circle or a polygon and prepare geometry accordingly
    if 'outline_circle' in data['extents']['volume']:
        # Handle circle
        lng = data['extents']['volume']['outline_circle']['center']['lng']
        lat = data['extents']['volume']['outline_circle']['center']['lat']
        radius = data['extents']['volume']['outline_circle'].get('radius', {}).get('value', None)
        geom = f"ST_Buffer(ST_SetSRID(ST_Point({lng}, {lat}), 4326), {radius})"
    elif 'outline_polygon' in data['extents']['volume']:
        # Handle polygon
        vertices = data['extents']['volume']['outline_polygon']['vertices']

        # Debugging: print the vertices to check their structure
        print("Vertices:", vertices)

        polygon_points = [f"{vertex[0]} {vertex[1]}" for vertex in vertices]
        geom = f"ST_SetSRID(ST_PolygonFromText('POLYGON(({','.join(polygon_points)}))'), 4326)"
    else:
        return jsonify({"error": "Invalid extent shape"}), 400

    # Extract subscription-specific data
    time_start = data['extents']['time_start']['value']
    time_end = data['extents']['time_end']['value']
    uss_base_url = data['uss_base_url']
    notify_for_operational_intents = data['notify_for_operations']
    notify_for_constraints = data['notify_for_constraints']
    old_version = data.get('old_version', 0)  # Default to 0 if not provided
    user_id = 1  # Assuming a default user_id for now

    conn = get_db_connection()
    cur = conn.cursor()

    # Insert extent data into the extents table
    cur.execute(f"""
        INSERT INTO extents
        (id, geom, altitude_lower, altitude_upper)
        VALUES
        (%s, {geom}, %s, %s)
    """, (extent_id, altitude_lower, altitude_upper))

    # Insert subscription data into the subscriptions table
    cur.execute("""
        INSERT INTO subscriptions
        (id, user_id, extent_id, time_start, time_end, uss_base_url, notify_for_operational_intents, notify_for_constraints, old_version)
        VALUES
        (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, (subscription_id, user_id, extent_id, time_start, time_end, uss_base_url, notify_for_operational_intents, notify_for_constraints, old_version))

    conn.commit()

    cur.close()
    conn.close()
    return jsonify({"message": "Subscription created", "id": subscription_id}), 201


@app.route('/uss/v1/subscriptions/<subscription_id>', methods=['PUT'])
@token_required
def update_subscription(subscription_id):
    data = request.json
    # Logic to update subscription in the database using SQL
    return jsonify({"message": "Subscription updated", "id": subscription_id}), 200


@app.route('/uss/v1/subscriptions/<subscription_id>', methods=['GET'])
@token_required
def get_subscription(subscription_id):
    conn = get_db_connection()
    cur = conn.cursor()

    # Retrieve subscription data
    cur.execute("SELECT * FROM subscriptions WHERE id = %s", (subscription_id,))
    subscription = cur.fetchone()

    if subscription:
        # Construct response JSON
        #response = {
        #    "id": subscription[0],
        #    "user_id": subscription[1],
        #    "location": {
        #        "lng": subscription[2],  # Assuming geom is a Point
        #        "lat": subscription[3]
        #    },
        #    "altitude_lower": subscription[4],
        #    "altitude_upper": subscription[5],
        #    "time_start": subscription[6].isoformat(),
        #    "time_end": subscription[7].isoformat(),
        #    "uss_base_url": subscription[8],
        #    "notify_for_operations": subscription[9],
        #    "notify_for_constraints": subscription[10],
        #    "old_version": subscription[11],
        #    "created_at": subscription[12].isoformat(),  # Assuming timestamp
        #    "updated_at": subscription[13].isoformat()   # Assuming timestamp
        #}
        return jsonify(subscription), 200
    else:
        return jsonify({"error": "Subscription not found"}), 404


@app.route('/uss/v1/subscriptions/<subscription_id>', methods=['DELETE'])
@token_required
def delete_subscription(subscription_id):
    # Logic to delete a subscription from the database using SQL
    return jsonify({"message": "Subscription deleted", "id": subscription_id}), 200





# ######### OPERATIONAL INTENT ###############
set -eo pipefail
response=$(curl -s -S -X POST http://localhost:5000/uss/v1/operational_intents \
-H "Authorization: Bearer $token"  \
-H "Content-Type: application/json" \
-d '{
    "operational_intent_id": "2f8343be-6482-4d1b-a474-16847e01af1e",
    "operational_intent": {
        "reference": {
            "id": "2f8343be-6482-4d1b-a474-16847e01af1e",
            "manager": "uss1",
            "uss_availability": "Unknown",
            "version": 1,
            "state": "Accepted",
            "ovn": "9d158f59-80b7-4c11-9c0c-8a2b4d936b2d",
            "time_start": {
                "value": "1985-04-12T23:20:50.52Z",
                "format": "RFC3339"
            },
            "time_end": {
                "value": "1985-04-12T23:20:50.52Z",
                "format": "RFC3339"
            },
            "uss_base_url": "https://uss.example.com/utm",
            "subscription_id": "78ea3fe8-71c2-4f5c-9b44-9c02f5563c6f"
        },
        "details": {
            "volumes": [],
            "off_nominal_volumes": [],
            "priority": 0
        }
    },
    "subscriptions": [
        {
            "subscription_id": "78ea3fe8-71c2-4f5c-9b44-9c02f5563c6f",
            "notification_index": 0
        }
    ]
}'
)
echo "Operational Intent POST Response: $response"
echo
echo





"outline_circle" : {
              "center": {
                  "lng": -118.84376423,
                  "lat": 34.43463465
              },
              "radius": {
                  "value": 45,
                  "units": "m"
              }
          },
