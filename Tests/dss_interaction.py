#!/usr/bin/env python

import sys
from pathlib import Path

from Utility import utility
# Add the parent directory to sys.path
sys.path.append(str(Path(__file__).resolve().parent.parent))

import requests
import urllib
import json
import traceback

import sys
import os
from datetime import datetime, timedelta
import pytz
from typing import List
import uuid

from AirspaceLink_API.advisories import Geometry, GeometryType, PolygonGeometry
from DSS.subscription import Subscription, SubscriptionRequest, Subscriptions, Subscription_Response
from Utility.utility import Extents, OutlinePolygon, OutlineCircle, TimeMeasured, Vertex, Vertices, Volume, Altitude, Time, Extent, AreaOfInterest, OperationalIntentStatus, TimeRange, AltitudeRange
from DSS.operational_intent_reference import OperationalIntentReferenceRequest, OperationalIntentReferenceResponse, OperationalIntentReferences, OperationalIntentReference
from DSS.constraint_reference import ConstraintReference, ConstraintReferenceRequest, ConstraintReferenceResponse, ConstraintReferences
from DSS.authentication import Authentication, UtmScope


class ApiException(Exception):
    def __init__(self, status_code, message = ""):
        self.status_code = status_code
        self.message = message
        super().__init__(self.message)

    def to_json(self):
        return {
            "status_code": self.status_code,
            "message": self.message
        }

class DSS_Interaction:

    def __init__(self, dss_url):
        if dss_url is None:
            self.__dss_url = "http://localhost:8082"
        else:
            self.__dss_url = dss_url


    def __handle_api_error(self, response):
        # Default success message
        success_msg = "Request successful."

        # Check for different status codes
        if response.status_code == 200: # successful
            pass
        elif response.status_code == 201: # successful
            pass
        elif response.status_code == 204: # successful
            pass
        elif response.status_code == 400:
            return ApiException(400, response.text)
        elif response.status_code == 401:
            return ApiException(401, "Unauthorized: Bearer access token missing, undecodable, or invalid.")
        elif response.status_code == 403:
            return ApiException(403, "Forbidden: Token lacks appropriate scope for this endpoint.")
        elif response.status_code == 404: #entity can't be found
            pass
        elif response.status_code == 409:
            return ApiException(409, response.text)
        elif response.status_code == 412:
            return ApiException(412, "Precondition Failed: Operational intent transition not allowed in current DSS state.")
        elif response.status_code == 413:
            return ApiException(413, "Payload Too Large: The area of operational intent is too large.")
        elif response.status_code == 429:
            return ApiException(429, "Too Many Requests: Slow down your request rate.")


    # SUBSCRIPTIONS
    def query_all_subscriptions(self, area_of_interest: AreaOfInterest, token) -> Subscriptions:
        try:
            header = {"Content-Type": "application/json", "Authorization": 'Bearer ' + str(token)}
            json_data = json.dumps(area_of_interest.to_json())

            try:
                response = requests.post(
                    url=f"{self.__dss_url}/dss/v1/subscriptions/query",
                    headers= header,
                    data = json_data
                )

                api_error = self.__handle_api_error(response)
                if api_error:
                    return api_error
                
                subscriptions = Subscriptions(response.json())
            except requests.exceptions.RequestException as e:
                print(e)
                return 

            return subscriptions
        except Exception as e:
            tb = traceback.format_exc()
            print("An error occurred:", e)
            print("At line:", traceback.extract_tb(e.__traceback__)[-1].lineno)
            print("Full traceback:")
            print(tb)
            return "Error"


    def create_subscription(self, subscription_id, subscriptionRequest: SubscriptionRequest, token) -> Subscription_Response:
        try:
            header = {"Content-Type": "application/json", "Authorization": 'Bearer ' + str(token)}
            json_data = subscriptionRequest.to_json()
            data = json.dumps(json_data)
            print("")
            print("SUBSCRIPTION PAYLOAD")
            print(data)

            response = requests.put(
                url = f"{self.__dss_url}/dss/v1/subscriptions/{subscription_id}",
                headers = header,
                data = data
                )
            
            api_error = self.__handle_api_error(response)
            print("")
            print(response.text)
            if api_error:
                return api_error
                
            response_json = response.json()
            subscription_response = Subscription_Response.from_json(response_json)

            # TODO: WHAT HAPPENS IF THE SUBSCRIPTION ALREADY EXISTS

            return subscription_response 
        except Exception as e:
            tb = traceback.format_exc()
            print("An error occurred:", e)
            print("At line:", traceback.extract_tb(e.__traceback__)[-1].lineno)
            print("Full traceback:")
            print(tb)
            return "Error"


    def retrieve_subscription(self, uuid_subscription_id, token) -> Subscription: 
        try:
            header = {"Content-Type": "application/json", "Authorization": 'Bearer ' + str(token)}

            response = requests.get(
                url=f"{self.__dss_url}/dss/v1/subscriptions/{uuid_subscription_id}",
                headers=header
            )
            
            api_error = self.__handle_api_error(response)
            if api_error:
                return api_error
            
            subscription = Subscription(response.json())
            return subscription
        except requests.exceptions.RequestException as e:
            tb = traceback.format_exc()
            print("An error occurred:", e)
            print("At line:", traceback.extract_tb(e.__traceback__)[-1].lineno)
            print("Full traceback:")
            print(tb)
            return None


    def update_subscription(self, uuid_subscription_id, version, subscriptionRequest: SubscriptionRequest, token) -> Subscription:
       try:
            header = {"Content-Type": "application/json", "Authorization": 'Bearer ' + str(token)}
            data = json.dumps(subscriptionRequest.to_json())

            try:
                if version is None:
                    raise Exception("Version cannot be None")
                
                response = requests.put(
                    url=f"{self.__dss_url}/dss/v1/subscriptions/{uuid_subscription_id}/{version}",
                    headers= header,
                    data=data
                )
            
                api_error = self.__handle_api_error(response)
                if api_error:
                    return api_error
                
                subscription = Subscription(response.json())
            except requests.exceptions.RequestException as e:
                print(e)
                return "Error"

            return subscription
       except Exception as e:
            tb = traceback.format_exc()
            print("An error occurred:", e)
            print("At line:", traceback.extract_tb(e.__traceback__)[-1].lineno)
            print("Full traceback:")
            print(tb)
            return "Error"
       

    def delete_subscription(self, uuid_subscription_id, version, token) -> Subscription:
        try:
            header = {"Content-Type": "application/json", "Authorization": 'Bearer ' + str(token)}

            response = requests.delete(
                url = f"{self.__dss_url}/dss/v1/subscriptions/{uuid_subscription_id}/{version}",
                headers = header
            )
            
            api_error = self.__handle_api_error(response)
            if api_error:
                return api_error
            
            subscription = Subscription(response.json())
            return subscription 
        except requests.exceptions.RequestException as e:
            tb = traceback.format_exc()
            print("An error occurred:", e)
            print("At line:", traceback.extract_tb(e.__traceback__)[-1].lineno)
            print("Full traceback:")
            print(tb)
            return None
           

    # OPERATIONAL INTENT REFERENCES
    def create_operational_intent_reference(self, operationalIntentReferenceRequest: OperationalIntentReferenceRequest, entity_id: uuid, token) -> OperationalIntentReferenceResponse:
        # UUIDv4Format (string) (EntityID)
        # Example: 2f8343be-6482-4d1b-a474-16847e01af1e
        # EntityID of the operational intent. 
        try:
            header = {"Content-Type": "application/json", "Authorization": 'Bearer ' + str(token)}
            json_data = json.dumps(operationalIntentReferenceRequest.to_json())
            try:
                response = requests.put(
                    url=f"{self.__dss_url}/dss/v1/operational_intent_references/{str(entity_id)}",
                    headers= header,
                    data=json_data
                )

                api_error = self.__handle_api_error(response)
                if api_error:
                    return api_error
                
                operationalIntentRequest_response = OperationalIntentReferenceResponse(response.json())
  
            except Exception as e:# requests.exceptions.RequestException as e:
                print(response.text)
                return("ERROR")

            return operationalIntentRequest_response 
        except Exception as e:
            tb = traceback.format_exc()
            print("An error occurred:", e)
            print("At line:", traceback.extract_tb(e.__traceback__)[-1].lineno)
            print("Full traceback:")
            print(tb)
            return "Error"


    def retrieve_operational_intent_reference(self, entity_id, token) -> OperationalIntentReference:
        header = {"Content-Type": "application/json", "Authorization": 'Bearer ' + str(token)}

        try:
            response = requests.get(
                url=f"{self.__dss_url}/dss/v1/operational_intent_references/{entity_id}",
                headers=header
            )
            
            api_error = self.__handle_api_error(response)
            if api_error:
                return api_error
            
            if response.status_code == 404:
                return None # entity doesn't exist
            operational_intent_ref_json = response.json()
            operationalIntentReference_response = OperationalIntentReference(operational_intent_ref_json["operational_intent_reference"])
            return operationalIntentReference_response 
        except requests.exceptions.RequestException as e:
            tb = traceback.format_exc()
            print("An error occurred:", e)
            print("At line:", traceback.extract_tb(e.__traceback__)[-1].lineno)
            print("Full traceback:")
            print(tb)
            return None


    def update_operational_intent_reference(self, operationalIntentReferenceRequest: OperationalIntentReferenceRequest, entity_id: uuid, ovn, token) -> OperationalIntentReferenceResponse:
        try:
            header = {"Content-Type": "application/json", "Authorization": 'Bearer ' + str(token)}
            json_data = json.dumps(operationalIntentReferenceRequest.to_json())
            try:
                response = requests.put(
                    url=f"{self.__dss_url}/dss/v1/operational_intent_references/{entity_id}/{ovn}",
                    headers= header,
                    data=json_data
                )
            
                api_error = self.__handle_api_error(response)
                if api_error:
                    return api_error         
                     
                operationalIntentRequest_response = OperationalIntentReferenceResponse(response.json())
                
            except requests.exceptions.RequestException as e:
                print(e)
                return("ERROR")

            return operationalIntentRequest_response 
        except Exception as e:
            tb = traceback.format_exc()
            print("An error occurred:", e)
            print("At line:", traceback.extract_tb(e.__traceback__)[-1].lineno)
            print("Full traceback:")
            print(tb)
            return "Error"


    def query_all_operational_intent_references(self, area_of_interest: AreaOfInterest, token) -> [OperationalIntentReferences]:
        try:
            header = {"Content-Type": "application/json", "Authorization": 'Bearer ' + str(token)}
            json_data = json.dumps(area_of_interest.to_json())

            # http://localhost:8082/dss/v1/operational_intent_references
            try:
                response = requests.post(
                    url=f"{self.__dss_url}/dss/v1/operational_intent_references/query",
                    headers= header,
                    data=json_data
                )

                api_error = self.__handle_api_error(response)
                if api_error:
                    return api_error
                
                content = response.content.decode('utf-8')
                content = json.loads(content)
                print(content)
                operationalIntentReferences = OperationalIntentReferences(content)
            except requests.exceptions.RequestException as e:
                print(e)
                return("ERROR")

            return operationalIntentReferences
        except Exception as e:
            tb = traceback.format_exc()
            print("An error occurred:", e)
            print("At line:", traceback.extract_tb(e.__traceback__)[-1].lineno)
            print("Full traceback:")
            print(tb)
            return "Error"


    def delete_operational_intent_reference(self, entity_id, ovn, token) -> OperationalIntentReferenceResponse:
        try:
            header = {"Content-Type": "application/json", "Authorization": 'Bearer ' + str(token)}

            response = requests.delete(
                url=f"{self.__dss_url}/dss/v1/operational_intent_references/{entity_id}/{ovn}", 
                headers=header
            )
            
            api_error = self.__handle_api_error(response)
            if api_error:
                return api_error
            
            subscription_response = OperationalIntentReferenceResponse(response.json())
            return subscription_response 
        except requests.exceptions.RequestException as e:
            tb = traceback.format_exc()
            print("An error occurred:", e)
            print("At line:", traceback.extract_tb(e.__traceback__)[-1].lineno)
            print("Full traceback:")
            print(tb)
            return None
    

    # CONSTRAINT REFERENCES

    def query_all_constraint_references(self, area_of_interest: AreaOfInterest, token) -> ConstraintReferences: # Plural
        
        try:
            header = {"Content-Type": "application/json", "Authorization": 'Bearer ' + str(token)}
            json_data = json.dumps(area_of_interest.to_json())

            try:
                response = requests.post(
                    url=f"{self.__dss_url}/dss/v1/constraint_references/query",
                    headers= header,
                    data=json_data
                )
            
                api_error = self.__handle_api_error(response)
                if api_error:
                    return api_error
                
                constraint_references = ConstraintReferences(response.json())
            except requests.exceptions.RequestException as e:
                print(e)
                return("ERROR")

            return constraint_references 
        except Exception as e:
            tb = traceback.format_exc()
            print("An error occurred:", e)
            print("At line:", traceback.extract_tb(e.__traceback__)[-1].lineno)
            print("Full traceback:")
            print(tb)
            return "Error"


    def retrieve_constraint_reference(self, entity_id, token) -> ConstraintReference:
        header = {"Content-Type": "application/json", "Authorization": 'Bearer ' + str(token)}

        try:
            response = requests.get(
                url=f"{self.__dss_url}/dss/v1/constraint_references/{entity_id}",
                headers=header
            )
            
            api_error = self.__handle_api_error(response)
            if api_error:
                return api_error
            
            constraint_json = response.json()
            constraint_reference_response = ConstraintReference(constraint_json["constraint_reference"])
            return constraint_reference_response 
        except requests.exceptions.RequestException as e:
            tb = traceback.format_exc()
            print("An error occurred:", e)
            print("At line:", traceback.extract_tb(e.__traceback__)[-1].lineno)
            print("Full traceback:")
            print(tb)
            return None


    def create_constraint_reference(self, constraintReferenceRequest: ConstraintReferenceRequest, entity_id, token) -> ConstraintReferenceResponse:
        try:
            header = {"Content-Type": "application/json", "Authorization": 'Bearer ' + str(token)}
            json_data = json.dumps(constraintReferenceRequest.to_json())
            print(json_data)
            try:
                response = requests.put(
                    url = f"{self.__dss_url}/dss/v1/constraint_references/{entity_id}",
                    headers = header,
                    data = json_data
                )
            
                api_error = self.__handle_api_error(response)
                if api_error:
                    return api_error
            
                constraint_reference_response = ConstraintReferenceResponse(response.json())

                # TODO: WHAT HAPPENS IF THE SUBSCRIPTION ALREADY EXISTS
            except requests.exceptions.RequestException as e:
                print(e)
                return("ERROR")

            return constraint_reference_response 
        except Exception as e:
            tb = traceback.format_exc()
            print("An error occurred:", e)
            print("At line:", traceback.extract_tb(e.__traceback__)[-1].lineno)
            print("Full traceback:")
            print(tb)
            return "Error"


    def update_constraint_reference(self, constraintReferenceRequest: ConstraintReferenceRequest, entity_id, ovn, token) -> ConstraintReferenceResponse:
        try:
            header = {"Content-Type": "application/json", "Authorization": 'Bearer ' + str(token)}
            json_data = json.dumps(constraintReferenceRequest.to_json())

            try:
                response = requests.put(
                    url=f"{self.__dss_url}/dss/v1/constraint_references/{entity_id}/{ovn}",
                    headers = header,
                    data = json_data
                )
            
                api_error = self.__handle_api_error(response)
                if api_error:
                    return api_error
                
                constraint_reference_response = ConstraintReferenceResponse(response.json())

                # TODO: WHAT HAPPENS IF THE SUBSCRIPTION ALREADY EXISTS
            except requests.exceptions.RequestException as e:
                print(e)
                return("ERROR")

            return constraint_reference_response 
        except Exception as e:
            tb = traceback.format_exc()
            print("An error occurred:", e)
            print("At line:", traceback.extract_tb(e.__traceback__)[-1].lineno)
            print("Full traceback:")
            print(tb)
            return "Error"


    def delete_constraint_reference(self, entity_id, ovn, token) -> ConstraintReferenceResponse:
        header = {"Content-Type": "application/json", "Authorization": 'Bearer ' + str(token)}

        try:
            response = requests.delete(
                url=f"{self.__dss_url}/dss/v1/constraint_references/{entity_id}/{ovn}", 
                headers=header
            )
            
            api_error = self.__handle_api_error(response)
            if api_error:
                return api_error
            
            constraint_response = ConstraintReferenceResponse(response.json())
            return constraint_response 
        except requests.exceptions.RequestException as e:
            tb = traceback.format_exc()
            print("An error occurred:", e)
            print("At line:", traceback.extract_tb(e.__traceback__)[-1].lineno)
            print("Full traceback:")
            print(tb)
            return None



##################################
##################################
##################################
#           TESTS                #
##################################
##################################
##################################

# Get the current time
now = datetime.utcnow()

# Format the current time as a string
formatted_now = now.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"

# Print the current time
print("Current time:", formatted_now)

# Calculate the time 5 minutes ahead
time_ahead = now + timedelta(minutes=5)

# Format the time 5 minutes ahead as a string
formatted_time_ahead = time_ahead.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"

constraint_reference_payload_json = {
    "extents": [
        {
            "volume": {
                "outline_circle": {
                    "radius": {
                        "units": "M",
                        "value": 50
                    },
                    "center": {
                        "lng": -83.075811, 
                        "lat": 42.329048
                    }
                },
                "altitude_lower": {
                    "value": 20,
                    "reference": "W84",
                    "units": "M"
                },
                "altitude_upper": {
                    "value": 100,
                    "reference": "W84",
                    "units": "M"
                }
            },
            "time_start": {
                "value": formatted_now,
                "format": "RFC3339"
            },
            "time_end": {
                "value": formatted_time_ahead,
                "format": "RFC3339"
            }
        }
    ],
    "uss_base_url": "https://uss.example.com/utm"
}

operational_intent_payload_json = {
    "extents": [
        {
            "volume": {
                "altitude_upper": {
                    "units": "M",
                    "reference": "W84",
                    "value": 114
                },
                "altitude_lower": {
                    "units": "M",
                    "reference": "W84",
                    "value": -7
                },
                "outline_circle": {
                    "radius": {
                        "units": "M",
                        "value": 300
                    },
                    "center": {
                        "lat": 32.59415886402617,
                        "lng": -117.1035655786647
                    }
                }
            },
            "time_start": {
                "value": formatted_now,
                "format": "RFC3339"
            },
            "time_end": {
                "value": formatted_time_ahead,
                "format": "RFC3339"
            } 
        },
        {
            "volume": {
                "altitude_upper": {
                    "units": "M",
                    "reference": "W84",
                    "value": 114
                },
                "altitude_lower": {
                    "units": "M",
                    "reference": "W84",
                    "value": 98
                },
                "outline_polygon": {
                    "vertices": [
                        {
                            "lat": 32.629403155814224,
                            "lng": -117.07235209637365
                        },
                        {
                            "lat": 32.62913940035541,
                            "lng": -117.07227677467183
                        },
                        {
                            "lat": 32.61019036953776,
                            "lng": -117.15071909262814
                        },
                        {
                            "lat": 32.61045408389095,
                            "lng": -117.15079458449262
                        }
                    ]
                }
            },
            "time_start": {
                "value": formatted_now,
                "format": "RFC3339"
            },
            "time_end": {
                "value": formatted_time_ahead,
                "format": "RFC3339"
            }
        },
        {
            "volume": {
                "altitude_upper": {
                    "units": "M",
                    "reference": "W84",
                    "value": 114
                },
                "altitude_lower": {
                    "units": "M",
                    "reference": "W84",
                    "value": 98
                },
                "outline_polygon": {
                    "vertices": [
                        {
                            "lat": 32.63060966167485,
                            "lng": -117.09038826289287
                        },
                        {
                            "lat": 32.630365389882776,
                            "lng": -117.09026347832622
                        },
                        {
                            "lat": 32.60141106631151,
                            "lng": -117.15717622635013
                        },
                        {
                            "lat": 32.601655284082824,
                            "lng": -117.15730113575759
                        }
                    ]
                }
            },
            "time_start": {
                "value": formatted_now,
                "format": "RFC3339"
            },
            "time_end": {
                "value": formatted_time_ahead,
                "format": "RFC3339"
            }
        },
        {
            "volume": {
                "altitude_upper": {
                    "units": "M",
                    "reference": "W84",
                    "value": 115
                },
                "altitude_lower": {
                    "units": "M",
                    "reference": "W84",
                    "value": 10
                },
                "outline_polygon": {
                    "vertices": [
                        {
                            "lat": 32.63712,
                            "lng": -117.1102
                        },
                        {
                            "lat": 32.63696,
                            "lng": -117.11003
                        },
                        {
                            "lat": 32.58489,
                            "lng": -117.15104
                        },
                        {
                            "lat": 32.58504,
                            "lng": -117.15127
                        }
                    ]
                }
            },
            "time_start": {
                "value": formatted_now,
                "format": "RFC3339"
            },
            "time_end": {
                "value": formatted_time_ahead,
                "format": "RFC3339"
            }
        },
        {
            "volume": {
                "altitude_upper": {
                    "units": "M",
                    "reference": "W84",
                    "value": 15
                },
                "altitude_lower": {
                    "units": "M",
                    "reference": "W84",
                    "value": -20
                },
                "outline_polygon": {
                    "vertices": [
                        {
                            "lat": 32.580378,
                            "lng": -117.1329
                        },
                        {
                            "lat": 32.58037,
                            "lng": -117.13324
                        },
                        {
                            "lat": 32.6354,
                            "lng": -117.133249
                        },
                        {
                            "lat": 32.63542,
                            "lng": -117.13297
                        }
                    ]
                }
            },
            "time_start": {
                "value": formatted_now,
                "format": "RFC3339"
            },
            "time_end": {
                "value": formatted_time_ahead,
                "format": "RFC3339"
            }
        }
    ],
    "key": [ ],
    "state": OperationalIntentStatus.ACCEPTED.value,
    "uss_base_url": "https://uss.example.com/utm",
    "new_subscription": { "uss_base_url": "https://uss.example.com/utm", "notify_for_constraints": True}
}

operational_intent_payload_json2 = {
    "extents": [
        {
            "volume": {
                "altitude_upper": {
                    "units": "M",
                    "reference": "W84",
                    "value": 114
                },
                "altitude_lower": {
                    "units": "M",
                    "reference": "W84",
                    "value": 0
                },
                "outline_circle": {
                    "radius": {
                        "units": "M",
                        "value": 300
                    },
                    "center": {
                        "lat": 32.59415886402617,
                        "lng": -117.1035655786647
                    }
                }
            },
            "time_start": {
                "value": formatted_now,
                "format": "RFC3339"
            },
            "time_end": {
                "value": formatted_time_ahead,
                "format": "RFC3339"
            } 
        },
        {
            "volume": {
                "altitude_upper": {
                    "units": "M",
                    "reference": "W84",
                    "value": 114
                },
                "altitude_lower": {
                    "units": "M",
                    "reference": "W84",
                    "value": 98
                },
                "outline_polygon": {
                    "vertices": [
                        {
                            "lat": 32.629403155814224,
                            "lng": -117.07235209637365
                        },
                        {
                            "lat": 32.62913940035541,
                            "lng": -117.07227677467183
                        },
                        {
                            "lat": 32.61019036953776,
                            "lng": -117.15071909262814
                        },
                        {
                            "lat": 32.61045408389095,
                            "lng": -117.15079458449262
                        }
                    ]
                }
            },
            "time_start": {
                "value": formatted_now,
                "format": "RFC3339"
            },
            "time_end": {
                "value": formatted_time_ahead,
                "format": "RFC3339"
            }
        },
        {
            "volume": {
                "altitude_upper": {
                    "units": "M",
                    "reference": "W84",
                    "value": 114
                },
                "altitude_lower": {
                    "units": "M",
                    "reference": "W84",
                    "value": 98
                },
                "outline_polygon": {
                    "vertices": [
                        {
                            "lat": 32.63060966167485,
                            "lng": -117.09038826289287
                        },
                        {
                            "lat": 32.630365389882776,
                            "lng": -117.09026347832622
                        },
                        {
                            "lat": 32.60141106631151,
                            "lng": -117.15717622635013
                        },
                        {
                            "lat": 32.601655284082824,
                            "lng": -117.15730113575759
                        }
                    ]
                }
            },
            "time_start": {
                "value": formatted_now,
                "format": "RFC3339"
            },
            "time_end": {
                "value": formatted_time_ahead,
                "format": "RFC3339"
            }
        },
        {
            "volume": {
                "altitude_upper": {
                    "units": "M",
                    "reference": "W84",
                    "value": 114
                },
                "altitude_lower": {
                    "units": "M",
                    "reference": "W84",
                    "value": 0
                },
                "outline_polygon": {
                    "vertices": [
                        {
                            "lat": 32.63712150700819,
                            "lng": -117.1102585196023
                        },
                        {
                            "lat": 32.636969253183054,
                            "lng": -117.11003035210928
                        },
                        {
                            "lat": 32.58489223521358,
                            "lng": -117.15104910529122
                        },
                        {
                            "lat": 32.5850444653223,
                            "lng": -117.15127729146461
                        }
                    ]
                }
            },
            "time_start": {
                "value": formatted_now,
                "format": "RFC3339"
            },
            "time_end": {
                "value": formatted_time_ahead,
                "format": "RFC3339"
            }
        },
        {
            "volume": {
                "altitude_upper": {
                    "units": "M",
                    "reference": "W84",
                    "value": 70
                },
                "altitude_lower": {
                    "units": "M",
                    "reference": "W84",
                    "value": -20
                },
                "outline_polygon": {
                    "vertices": [
                        {
                            "lat": 32.58037888894311,
                            "lng": -117.13297510795468
                        },
                        {
                            "lat": 32.58037888894311,
                            "lng": -117.13324941122436
                        },
                        {
                            "lat": 32.635427303056666,
                            "lng": -117.13324941122436
                        },
                        {
                            "lat": 32.635427303056666,
                            "lng": -117.13297510795468
                        }
                    ]
                }
            },
            "time_start": {
                "value": formatted_now,
                "format": "RFC3339"
            },
            "time_end": {
                "value": formatted_time_ahead,
                "format": "RFC3339"
            }
        }
    ],
    "key": [ ],
    "state": OperationalIntentStatus.ACCEPTED.value,
    "uss_base_url": "https://uss.example.com/utm",
    "new_subscription": { "uss_base_url": "https://uss.example.com/utm", "notify_for_constraints": True}
}

subscription_payload_json = {
    "extents": {
        "volume": {
            "outline_circle": {
                "center": { #NewLab Detroit
                    "lng": -83.075811, 
                    "lat": 42.329048
                },
                "radius": {
                    "value": 3000.00,
                    "units": "M"
                }
            },
            "altitude_lower": {
                "value": 0,
                "reference": "W84",
                "units": "M"
            },
            "altitude_upper": {
                "value": 120,
                "reference": "W84",
                "units": "M"
            }
        },
        "time_start": {
            "value": formatted_now,
            "format": "RFC3339"
        },
        "time_end": {
            "value": formatted_time_ahead,
            "format": "RFC3339"
        }
    },
    "old_version": 0,
    "uss_base_url": "https://exampleuss.com/utm",
    "notify_for_operational_intents": True,
    "notify_for_constraints": True
}

area_of_interest_json = {
    "area_of_interest": {
        "volume": {
            "outline_circle": {
                "center": {
                    "lng": -83.075811, 
                    "lat": 42.329048
                },
                "radius": {
                    "value": 300.183,
                    "units": "M"
                }
            },
            "altitude_lower": {
                "value": 10,
                "reference": "W84",
                "units": "M"
            },
            "altitude_upper": {
                "value": 100,
                "reference": "W84",
                "units": "M"
            }
        },
        "time_start": {
            "value": formatted_now,
            "format": "RFC3339"
        },
        "time_end": {
            "value": formatted_time_ahead,
            "format": "RFC3339"
        }
    }
}            

# Test


class MainProcessor:
    @staticmethod
    def build_extent(polygon: PolygonGeometry, time_range: TimeRange, altitude_range: AltitudeRange)->Extent:
        vertices = []
        coordinates_set = set()

        for i in polygon.coordinates:
            latitude, longitude = i[1], i[0]
            # Check for duplicates before adding, don't have to close the polygon with a start and finish vertex at the same place either.
            if (latitude, longitude) in coordinates_set:
                print(f"Duplicate vertex: ({latitude}, {longitude})")
            else:
                vertex = Vertex(latitude, longitude)
                vertices.append(vertex)
                coordinates_set.add((latitude, longitude))

        vertices_object = Vertices(vertices)
        outline_polygon = OutlinePolygon(vertices_object)

        volume = Volume(None, outline_polygon, altitude_range.lower, altitude_range.upper)
        return Extent(volume, time_range.start_time, time_range.end_time)

    # ###### SUBSCRIPTIONS ####### #
    @staticmethod
    def create_subscription(
            dss_instance: DSS_Interaction, 
            extent: Extent = None,
            uuid_subscription_id: uuid = None, 
            base_url: str = None, 
            subscription_request: SubscriptionRequest = None, 
            token: str = None) -> Subscription_Response:

        if subscription_request is not None:
            subscription_response = dss_instance.create_subscription(uuid_subscription_id, subscription_request, token)
        else:
            # TODO: URL will have to be something other than the Operation URL created above:  'url': 'https://portal-dev.airspacelink.com/plan/operations/F636C859/claim'	
            payload = SubscriptionRequest(extents = extent, uss_base_url=base_url, notify_for_operational_intents=True, notify_for_constraints=True)

            subscription_response = dss_instance.create_subscription(uuid_subscription_id, payload, token)

        return subscription_response


    @staticmethod
    def retrieve_subscription(dss_instance: DSS_Interaction, uuid_subscription_id, token)->Subscription:
        if uuid_subscription_id is not None:
            subscription_result = dss_instance.retrieve_subscription(uuid_subscription_id, token)
            return subscription_result
  
    @staticmethod
    def update_subscription(dss_instance: DSS_Interaction, uuid_subscription_id, version, subscriptionRequest: SubscriptionRequest, token, )->Subscription:
        if uuid_subscription_id is not None:
            subscription_result = dss_instance.update_subscription(uuid_subscription_id, version, subscriptionRequest, token)
            return subscription_result

    @staticmethod
    def delete_subscription(dss_instance: DSS_Interaction, token, uuid_subscription_id)->Subscription:
        if uuid_subscription_id is not None:
            subscription_result = dss_instance.delete_subscription(uuid_subscription_id, 0, token)
            return subscription_result

    @staticmethod
    def query_subscriptions(dss_instance: DSS_Interaction, token)->Subscriptions:
        area_of_interest = AreaOfInterest.from_json(area_of_interest_json)
        subscriptions_results = dss_instance.query_all_subscriptions(area_of_interest, token)
        return subscriptions_results

    # ####### CONSTRAINTS ###### #
    @staticmethod
    def create_constraint_reference(dss_instance: DSS_Interaction, constraint_reference_request: ConstraintReferenceRequest, extents: [Extent], entity_id: uuid = None, base_url: str = None, token: str = None) -> ConstraintReferenceResponse:
        if constraint_reference_request is not None:
            constraint_reference_response = dss_instance.create_constraint_reference(constraint_reference_request, entity_id, token)
        else:
            constraint_reference_request = ConstraintReferenceRequest(extents, base_url)
            constraint_reference_response = dss_instance.create_constraint_reference(constraint_reference_request, entity_id, token)

        return constraint_reference_response

    @staticmethod
    def retrieve_constraint_reference(dss_instance: DSS_Interaction, entity_id, token) -> ConstraintReference:
        constraint_reference = dss_instance.retrieve_constraint_reference(entity_id, token)
        return constraint_reference

    @staticmethod
    def query_constraint_references(dss_instance: DSS_Interaction, token) -> ConstraintReferences:
        area_of_interest = AreaOfInterest.from_json(area_of_interest_json)
        constraint_references_response = dss_instance.query_all_constraint_references(area_of_interest, token)
        return constraint_references_response
    
    @staticmethod
    def update_constraint_reference(dss_instance: DSS_Interaction, entity_id, ovn, token) -> ConstraintReferenceResponse:
        constraint_reference_request = ConstraintReferenceRequest.from_json(constraint_reference_payload_json)
        constraint_reference_response = dss_instance.update_constraint_reference(constraint_reference_request, entity_id, ovn, token)
        return constraint_reference_response
    
    @staticmethod
    def delete_constraint_reference(dss_instance: DSS_Interaction, entity_id, ovn, token) -> ConstraintReferenceResponse:
        constraint_reference_response = dss_instance.delete_constraint_reference(entity_id, ovn, token)
        return constraint_reference_response


    # ####### OPERATIONAL_INTENT_REFERENCES ###### #

    @staticmethod
    def create_operational_intent_ref(dss_instance: DSS_Interaction, extents: [utility.Extent], keys: [], state: OperationalIntentStatus, uss_base_url: str, subscription_id, new_subscription: utility.NewSubscription, entity_id: str, token) -> OperationalIntentReferenceResponse:
        operational_intent_payload_object = OperationalIntentReferenceRequest(extents, keys, state, uss_base_url, subscription_id, new_subscription)
        operational_intent_reference_response = dss_instance.create_operational_intent_reference(operational_intent_payload_object, entity_id, token)
        return operational_intent_reference_response

    @staticmethod
    def retieve_operational_intent_ref(dss_instance: DSS_Interaction, entity_id, token)->OperationalIntentReference:
        operational_intent_reference = dss_instance.retrieve_operational_intent_reference(entity_id, token)
        return operational_intent_reference

    @staticmethod
    def query_operational_intent_refs(dss_instance: DSS_Interaction, token)->[OperationalIntentReferences]:
        area_of_interest = AreaOfInterest.from_json(area_of_interest_json)
        operational_intent_references_response = dss_instance.query_all_operational_intent_references(area_of_interest, token)
        return operational_intent_references_response
    
    @staticmethod
    def update_operational_intent_ref(dss_instance: DSS_Interaction, subscriptionID, entity_id, ovn, constraint_ovn, token)->OperationalIntentReferenceResponse:
        operational_intent_payload_object = OperationalIntentReferenceRequest.from_json(operational_intent_payload_json)
        operational_intent_payload_object.key = [constraint_ovn]
        operational_intent_payload_object.subscription_id = subscriptionID
        operational_intent_reference_response = dss_instance.update_operational_intent_reference(operational_intent_payload_object, entity_id, ovn, token)
        return operational_intent_reference_response
    
    @staticmethod
    def delete_operational_intent_ref(dss_instance: DSS_Interaction, entity_id, ovn, token)->OperationalIntentReferenceResponse:
        operational_intent_reference_response = dss_instance.delete_operational_intent_reference(entity_id, ovn, token)
        return operational_intent_reference_response
   
        

def main(actions):
    dss_instance = DSS_Interaction("http://localhost:8082")
    token = Authentication().get_token([UtmScope.STRATEGIC_COORDINATION.value, UtmScope.CONSTRAINT_PROCESSING.value, UtmScope.CONSTRAINT_MANAGEMENT.value, UtmScope.CONFORMANCE_MONITORING_SA.value])

    subscription_response = None
    subscriptions = None
    constraint_reference_response = None
    constraint_subscribers = None
    constraint_refs = None
    operational_intent_reference_response = None
    operational_intent_reference = None

    for action in actions:
        if action == 'create_subscription':
            uuid_subscription_id = uuid.uuid4()
            payload = SubscriptionRequest.from_json(subscription_payload_json)
            response = MainProcessor.create_subscription(dss_instance, payload, uuid_subscription_id, token)
            if isinstance(response, ApiException):
                print(f"API error {response.status_code}: {response}")
                print(f"Message: {response.message}: {response}")
            else:
                subscription_response = response

        elif action == 'query_subscription':
            response = MainProcessor.query_subscriptions(dss_instance, token)
            if isinstance(response, ApiException):
                print(f"API error {response.status_code}: {response}")
                print(f"Message: {response.message}: {response}")
            else:
                subscriptions = response

        elif action == 'retrieve_subscription':
            response = MainProcessor.retrieve_subscription(dss_instance, subscription_response.subscription.id, token)
            if isinstance(response, ApiException):
                print(f"API error {response.status_code}: {response}")
                print(f"Message: {response.message}: {response}")
            else:
                subscription = response
            
        elif action == 'delete_subscription':
            response = MainProcessor.delete_subscription(dss_instance, token, subscription_response.subscription.id)
            if isinstance(response, ApiException):
                print(f"API error {response.status_code}: {response}")
                print(f"Message: {response.message}: {response}")
            else:
                subscription = response

        elif action == 'create_constraint':
            uid = uuid.uuid4()
            constraint_reference_request = ConstraintReferenceRequest.from_json(constraint_reference_payload_json)
            response = MainProcessor.create_constraint_reference(dss_instance, constraint_reference_request, uid, token)
            if isinstance(response, ApiException):
                print(f"API error {response.status_code}: {response}")
                print(f"Message: {response.message}: {response}")
            else:
                constraint_reference_response = response
                constraint_subscribers = constraint_reference_response.subscribers

        elif action == 'retrieve_constraint':
            if constraint_reference_response.constraint_reference.id is not None:
                response = MainProcessor.retrieve_constraint_reference(dss_instance, constraint_reference_response.constraint_reference.id, token)
                if isinstance(response, ApiException):
                    print(f"API error {response.status_code}: {response}")
                    print(f"Message: {response.message}: {response}")
                else:
                    constraint_ref = response

        elif action == 'query_constraint_refs':
            response = MainProcessor.query_constraint_references(dss_instance, token)
            if isinstance(response, ApiException):
                print(f"API error {response.status_code}: {response}")
                print(f"Message: {response.message}: {response}")
            else:
                constraint_refs = response

        elif action == 'update_constraint':
            if constraint_reference_response.constraint_reference.id is not None and constraint_reference_response.constraint_reference.ovn is not None:
                response = MainProcessor.update_constraint_reference(dss_instance, constraint_reference_response.constraint_reference.id, 
                                                                                     constraint_reference_response.constraint_reference.ovn, token)
                if isinstance(response, ApiException):
                    print(f"API error {response.status_code}: {response}")
                    print(f"Message: {response.message}: {response}")
                else:
                    constraint_ref_response = response

        elif action == 'delete_constraint':
            if constraint_reference_response.constraint_reference.id is not None and constraint_reference_response.constraint_reference.ovn is not None:
                response = MainProcessor.delete_constraint_reference(dss_instance, constraint_reference_response.constraint_reference.id, 
                                                                                     constraint_reference_response.constraint_reference.ovn, token)
                if isinstance(response, ApiException):
                    print(f"API error {response.status_code}: {response}")
                    print(f"Message: {response.message}: {response}")
                else:
                    constraint_ref_response = response

        elif action == 'create_operational_intent':
            uid = uuid.uuid4()
            response = MainProcessor.create_operational_intent_ref(dss_instance, uid, token)
            if isinstance(response, ApiException):
                print(f"API error {response.status_code}: {response}")
                print(f"Message: {response.message}: {response}")
            else:
                operational_intent_reference_response = response

        elif action == 'retrieve_operation_intent':
            if operational_intent_reference_response.operational_intent_reference.id is not None:
                response = MainProcessor.retieve_operational_intent_ref(dss_instance, operational_intent_reference_response.operational_intent_reference.id, token)
                if isinstance(response, ApiException):
                    print(f"API error {response.status_code}: {response}")
                    print(f"Message: {response.message}: {response}")
                else:
                    op_intent_ref = response
                

        elif action == 'query_operational_intent_refs':
            op_intent_refs = MainProcessor.query_operational_intent_refs(dss_instance, token)

        elif action == 'update_op_intent_ref':
            if operational_intent_reference_response.operational_intent_reference.id is not None and operational_intent_reference_response.operational_intent_reference.ovn is not None:
                response = MainProcessor.update_operational_intent_ref(dss_instance, subscription_response.subscription.id, 
                                                                                      operational_intent_reference_response.operational_intent_reference.id, 
                                                                                      constraint_reference_response.constraint_reference.ovn, 
                                                                                      operational_intent_reference_response.operational_intent_reference.ovn, token)
                if isinstance(response, ApiException):
                    print(f"API error {response.status_code}: {response}")
                    print(f"Message: {response.message}: {response}")
                else:
                    op_intent_ref_response = response

        elif action == 'delete_op_intent_ref':
            if operational_intent_reference_response.operational_intent_reference.id is not None and operational_intent_reference_response.operational_intent_reference.ovn is not None:
                response = MainProcessor.delete_operational_intent_ref(dss_instance, operational_intent_reference_response.operational_intent_reference.id, 
                                                             operational_intent_reference_response.operational_intent_reference.ovn, token)
                if isinstance(response, ApiException):
                    print(f"API error {response.status_code}: {response}")
                    print(f"Message: {response.message}: {response}")
                else:
                    operational_intent_reference = response


if __name__ == "__main__":
    main([
        'create_subscription', 
        'create_constraint', 
        'retrieve_subscription',
        'create_operational_intent', 
        'query_subscription',  
        'retrieve_constraint', 
        'query_constraint_refs',
        'update_constraint',
        'retrieve_operation_intent',
        'query_operational_intent_refs',
        'update_op_intent_ref',
        'delete_op_intent_ref',
        'delete_constraint',
        'delete_subscription']
        )
