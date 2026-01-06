import json
import traceback
import requests
from DSS.subscription import Subscriptions

from Tests.dss_interaction import ApiException
from USS.constaint_details import Constraint, ConstraintRequest
from USS.operational_intent_details import OperationalIntentDetails, OperationalIntentOffNominal


class USS_Interaction:
    def __init__(self) -> None:
        pass

    def __handle_api_error(self, response):
        # Default success message
        success_msg = "Request successful."

        # Check for different status codes
        if response.status_code == 200:
            pass
        elif response.status_code == 201:
            pass
        elif response.status_code == 400:
            return ApiException(400, "Bad Request: Invalid input parameters or disallowed mutation attempt.")
        elif response.status_code == 401:
            return ApiException(401, "Unauthorized: Bearer access token missing, undecodable, or invalid.")
        elif response.status_code == 403:
            return ApiException(403, "Forbidden: Token lacks appropriate scope for this endpoint.")
        elif response.status_code == 404: #entity can't be found
            pass
        elif response.status_code == 409:
            return ApiException(409, "Conflict: Issues with provided key or simultaneous changes in DSS.")
        elif response.status_code == 412:
            return ApiException(412, "Precondition Failed: Operational intent transition not allowed in current DSS state.")
        elif response.status_code == 413:
            return ApiException(413, "Payload Too Large: The area of operational intent is too large.")
        elif response.status_code == 429:
            return ApiException(429, "Too Many Requests: Slow down your request rate.")

    # #################### #
    #  CONSTRAINT DETAILS  #
    # #################### #

    def retrieve_constraint_details(self, peer_uss_url: str, constraint_request: ConstraintRequest, token) -> Constraint:
        header = {"Content-Type": "application/json", "Authorization": 'Bearer ' + str(token)}

        try:
            response = requests.get(
                url=f"{peer_uss_url}/dss/v1/constraints",
                headers=header
            )
            
            api_error = self.handle_api_error(response)
            if api_error:
                return api_error
            
            constraint_json = response.json()
            constraint_details_response = Constraint.from_json(constraint_json["constraint"])
            return constraint_details_response 
        except requests.exceptions.RequestException as e:
            tb = traceback.format_exc()
            print("An error occurred:", e)
            print("At line:", traceback.extract_tb(e.__traceback__)[-1].lineno)
            print("Full traceback:")
            print(tb)
            return None


    def notify_peer_uss_constraint_details(self, peer_uss_url: str, constraint_request: ConstraintRequest, token):
        header = {"Content-Type": "application/json", "Authorization": 'Bearer ' + str(token)}

        data = constraint_request.to_json()
        data = json.dumps(data)

        try:
            response = requests.post(
                url=f"{peer_uss_url}/uss/v1/constraints",
                data= data, 
                headers=header
            )
            
            api_error = self.handle_api_error(response)
            if api_error:
                return api_error
            
            json_response = response.json()
            return json_response 
        except requests.exceptions.RequestException as e:
            tb = traceback.format_exc()
            print("An error occurred:", e)
            print("At line:", traceback.extract_tb(e.__traceback__)[-1].lineno)
            print("Full traceback:")
            print(tb)
            return None 
    

    # ############################ #
    #  OPERATIONAL INTENT DETAILS  #
    # ############################ #

    def retrieve_operational_intent_details(self, peer_uss_url, entity_id, token) -> OperationalIntentDetails:
        header = {"Content-Type": "application/json", "Authorization": 'Bearer ' + str(token)}

        try:
            response = requests.get(
                url=f"{peer_uss_url}/uss/v1/operational_intents/{entity_id}",
                headers=header
            )
            
            api_error = self.handle_api_error(response)
            if api_error:
                return api_error
            
            operational_intent_details_json = response.json()
            operational_intent_details = OperationalIntentDetails.from_json(operational_intent_details_json)
            return operational_intent_details 
        except requests.exceptions.RequestException as e:
            tb = traceback.format_exc()
            print("An error occurred:", e)
            print("At line:", traceback.extract_tb(e.__traceback__)[-1].lineno)
            print("Full traceback:")
            print(tb)
            return None 
        
    
    def query_operational_intent_details(self, peer_uss_url, entity_id, token) -> OperationalIntentOffNominal:
        header = {"Content-Type": "application/json", "Authorization": 'Bearer ' + str(token)}

        try:
            response = requests.get(
                url=f"{peer_uss_url}/uss/v1/operational_intents/{entity_id}/telemetry", 
                headers=header
            )
            
            api_error = self.handle_api_error(response)
            if api_error:
                return api_error
            
            operational_intent_off_nominal_json = response.json()
            operational_intent_off_nominal = OperationalIntentOffNominal.from_json(operational_intent_off_nominal_json)
            return operational_intent_off_nominal 
        except requests.exceptions.RequestException as e:
            tb = traceback.format_exc()
            print("An error occurred:", e)
            print("At line:", traceback.extract_tb(e.__traceback__)[-1].lineno)
            print("Full traceback:")
            print(tb)
            return None 
        
    
    def notify_peer_uss_operational_intent_details(self, peer_uss_url: str, operational_intent: OperationalIntentDetails, subscriptions: Subscriptions, token):
        header = {"Content-Type": "application/json", "Authorization": 'Bearer ' + str(token)}

        data = operational_intent.to_json()
        data = json.dumps(data)

        try:
            response = requests.post(
                url=f"{peer_uss_url}/uss/v1/operational_intents", 
                data=data,
                headers=header
            )
            
            api_error = self.handle_api_error(response)
            if api_error:
                return api_error
            
            json_response = response.json()
            return json_response 
        except requests.exceptions.RequestException as e:
            tb = traceback.format_exc()
            print("An error occurred:", e)
            print("At line:", traceback.extract_tb(e.__traceback__)[-1].lineno)
            print("Full traceback:")
            print(tb)
            return None 