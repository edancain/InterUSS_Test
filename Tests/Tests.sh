# set -x
#!/usr/bin/env bash

# ############### AIRSPACELINK #########

#script_path="../Airspacelink-api/AirspaceLinkTest.py"

# Check if the script exists
#if [ -f "$script_path" ]; then
#    echo "Script exists. Running it now..."
#    # Run the script
#    json_output=$(../Airspacelink-api/AirspaceLinkTest.py)
#    echo "Output of route function: $json_output"
#else
#    echo "Script does not exist."
    # Handle the case where the script is missing
    # For example, exit the script or perform an alternative action
 #   exit 1
#fi

#echo
# Using the data from the calls above, lets create a Airpacelink operation and store it in the database.



# ############### DSS ##################

authentication_path="../DSS/authentication.py"
if [ -f $authentication_path ]; then
    # echo "Authentication script found. Fetching token..."
    ACCESS_TOKEN=$(python3 $authentication_path get_token)
    echo "$ACCESS_TOKEN"
else
    echo "Authentication script not found at $authentication_path"
    exit 1
fi


# ######### Subscription #####################


# create a subscription
# Check if the script exists
subscription_script_path="../DSS/subscription_interaction.py"
if [ -f "$subscription_script_path" ]; then
    echo "Subscription Script exists. Running creation_subscription now..."
    uuid=$(uuidgen)
    
    json_output=$(python3 "$subscription_script_path" create_subscription $uuid "" $ACCESS_TOKEN)
    echo "$json_response"
else
    echo "Subscription script does not exist."
    # Handle the case where the script is missing
    # For example, exit the script or perform an alternative action
    exit 1
fi

# ######################################################


# GET A SUBSCRIPTION BY VALUE!
echo ""
echo "GET A SUBSCRIPTION BY VALUE!"

json_response=$(python3 "$subscription_script_path" query_subscription $uuid $ACCESS_TOKEN)
echo "$json_response"

# ######################################################
# UPDATE A SUBSCRIPTION
# echo ""
# echo "GET A SUBSCRIPTION BY VALUE!"
# version=0
# data=None
# json_response=$(python3 dss_interaction.py query_subscription $uuid 0 "" $ACCESS_TOKEN) # def update_subscription(self, uuid_subscription_id, version, data, token):

# ######################################################
# DELETE A SUBSCRIPTION
echo ""
echo "DELETE A SUBSCRIPTION BY VALUE!"

json_response=$(python3 "$subscription_script_path" query_subscription $uuid $ACCESS_TOKEN)
echo "$json_response"

exit 1



 # ################ USS #################
 # ################ USS #################
 # ################ USS #################
 # ################ USS #################


# GET A TOKEN
set -eo pipefail

# Try to acquire a token with a name / password combination not in the database
# Send the authentication request and capture the response
response=$(curl -s -S -X POST http://localhost:5000/oauth/token \
-H "Content-Type: application/json" \
-d '{"username": "TestUser1", "password": "OneTwoThree"}')

token=$(echo $response | python -c "import sys, json; print(json.load(sys.stdin)['token'])")

# Check if the token variable is non-empty and print it
if [ -n "$token" ]; then
    echo
    echo "USS Token: $token"
    echo
else
    echo
    echo "Failed to get a token."
    echo
fi


# Create a USS Su




# CREATE AN AIRSPACELINK OPERATIONAL TABLE ENTRY
set -eo pipefail
echo "Create Operational data"
# AirspaceLink Operation Creation
response=$(curl -s -S -X POST http://localhost:5000/uss/v1/airspacelink_operations \
--write-out '%{http_code}' \
-H "Content-Type: application/json" \
-H "Authorization: Bearer $token" \
-d '{
    "uas_id": "",
    "route": {
        "type": "LineString",
        "coordinates": [
            [-83.237915,42.316416],
            [-83.23412143346106,42.313110874461174],
            [-83.22695599604445,42.31115564289149],
            [-83.22456763561581,42.31050380530632],
            [-83.21262672407333,42.30724391460332],
            [-83.21023871992755,42.30659179593648],
            [-83.205643,42.304991]
        ]
    },
    "pilot_name": "Edan Cain",
    "pilot_phone": "9092222442",
    "altitude_upper": {
        "value": 3000,
        "reference": "W84",
        "units": "M"
    },
    "time_start": {
        "value": "2023-11-15T00:00:00Z",
        "format": "RFC3339"
    },
    "time_end": {
        "value": "2023-11-16T00:00:00Z",
        "format": "RFC3339"
    }
}')

echo "Response from airspacelink_operations: $response"
echo
