import sys
from pathlib import Path
# Add the parent directory to sys.path
sys.path.append(str(Path(__file__).resolve().parent.parent))
from Utility import utility
from typing import List
from datetime import datetime, timedelta
import json


import uuid

# ##################################### ######## #
# ########      USS SERVER TESTS       ######## #
# ##################################### ######## #

# ##################################### ######## #
# ######## OPERATIONAL INTENT DETAILS ######## #
# ##################################### ######## #
def query_detailed_positional_info_off_nominal_operational_intent_details(id):
    # Query detailed information on the position of an off-nominal operational intent from a USS
    # https://redocly.github.io/redoc/?url=https://raw.githubusercontent.com/astm-utm/Protocol/v1.0.0/utm.yaml#tag/p2p_utm/operation/getOperationalIntentTelemetry

    # token = authentication.Authentication().get_token()
    # uss_server = uss_interaction.USS_Interaction("http://localhost:8082")
    # op_intent_details = uss_server.query_all_operational_intent_references(areaofinterest, token)
    pass


def retrieve_operational_intent_details(id):
    # https://redocly.github.io/redoc/?url=https://raw.githubusercontent.com/astm-utm/Protocol/v1.0.0/utm.yaml#tag/p2p_utm/operation/getOperationalIntentDetails
    id = "2f8343be-6482-4d1b-a474-16847e01af1e"
    token = authentication.Authentication().get_token()
    # uss_server = dss_interaction.DSS_Interaction("http://localhost:8082")
    # opt_intent_details = sss_server.retrieve_operational_intent_reference(id, token)


def notify_peer_uss_changed_operational_intent_details():
    # https://redocly.github.io/redoc/?url=https://raw.githubusercontent.com/astm-utm/Protocol/v1.0.0/utm.yaml#tag/p2p_utm/operation/notifyOperationalIntentDetailsChanged
    pass

# ##################################### ######## #
# ######## CONSTRAINT DETAILS ######## #
# ##################################### ######## #

def retrieve_constraint_details(id):
    # https://redocly.github.io/redoc/?url=https://raw.githubusercontent.com/astm-utm/Protocol/v1.0.0/utm.yaml#tag/p2p_utm/operation/getConstraintDetails
    pass


def notify_peer_changed_constraint_details():
    # https://redocly.github.io/redoc/?url=https://raw.githubusercontent.com/astm-utm/Protocol/v1.0.0/utm.yaml#tag/p2p_utm/operation/notifyConstraintDetailsChanged
    pass


# ######################################## ######## #
# ######## NOTIFY USS OF ERROR ENCOUNTERED ######## #
# ######################################## ######## #


def notify_uss_error_encountered():
    # https://redocly.github.io/redoc/?url=https://raw.githubusercontent.com/astm-utm/Protocol/v1.0.0/utm.yaml#tag/p2p_utm/operation/makeUssReport
    pass