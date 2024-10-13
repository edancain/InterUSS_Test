from Utility import utility
from typing import List
from uuid import UUID


class OperationalIntentReference:  
    """
    DSS Operational Intent Reference Retrieve response structure
    Retrieve: https://redocly.github.io/redoc/?url=https://raw.githubusercontent.com/astm-utm/Protocol/v1.0.0/utm.yaml#tag/Operational-intent-references/operation/getOperationalIntentReference
    """
    def __init__(self, data):
        if data == None or data == []:
            return 
        self.id = data["id"]
        self.manager = data["manager"]
        self.uss_availability = data["uss_availability"]
        self.version = data["version"]
        self.state = data["state"]
        self.ovn = data["ovn"]
        if data["time_start"] is not {}:
            self.time_start = utility.Time(data["time_start"])
        else:
            self.time_start = {}

        if data["time_end"] is not {}:
            self.time_end = utility.Time(data["time_end"])
        else:
            self.time_end = {}

        self.uss_base_url = data["uss_base_url"]
        self.subscription_id = data["subscription_id"]

    def to_json(self):
        return {
            "id": self.id,
            "manager": self.manager,
            "uss_availability": self.uss_availability,
            "version": self.version,
            "state": self.state,
            "ovn": self.ovn,
            "time_start": self.time_start.to_json() if isinstance(self.time_start, utility.Time) else {},
            "time_end": self.time_end.to_json() if isinstance(self.time_end, utility.Time) else {},
            "uss_base_url": self.uss_base_url,
            "subscription_id": self.subscription_id
        }
       

class OperationalIntentReferenceResponse:  # response structure for create, update, delete Operational Intent refs
    """
    DSS Operational Intent Reference response structure
    Create: https://redocly.github.io/redoc/?url=https://raw.githubusercontent.com/astm-utm/Protocol/v1.0.0/utm.yaml#tag/Operational-intent-references/operation/createOperationalIntentReference
    Update: https://redocly.github.io/redoc/?url=https://raw.githubusercontent.com/astm-utm/Protocol/v1.0.0/utm.yaml#tag/Operational-intent-references/operation/updateOperationalIntentReference
    Remove: https://redocly.github.io/redoc/?url=https://raw.githubusercontent.com/astm-utm/Protocol/v1.0.0/utm.yaml#tag/Operational-intent-references/operation/deleteOperationalIntentReference
    """
    
    def __init__(self, data):
        self.subscribers = [utility.Subscriber(opIntRef) for opIntRef in data["subscribers"]]
        self.operational_intent_reference = OperationalIntentReference(data["operational_intent_reference"])

    def to_json(self):
        return {
            "subscribers": [subscriber.to_json() for subscriber in self.subscribers],
            "operational_intent_reference": self.operational_intent_reference.to_json()
        }


class OperationalIntentReferences:  
    """
    DSS Query all Operational Intent References
    Query: https://redocly.github.io/redoc/?url=https://raw.githubusercontent.com/astm-utm/Protocol/v1.0.0/utm.yaml#tag/Operational-intent-references/operation/queryOperationalIntentReferences
    """

    def __init__(self, data):
        self.operational_intent_references = data.get("operational_intent_references", [])


class OperationalIntentReferenceRequest: # request structure for op int ref create and update
    """
    DSS Create Operational Intent Reference request structure
    Create: https://redocly.github.io/redoc/?url=https://raw.githubusercontent.com/astm-utm/Protocol/v1.0.0/utm.yaml#tag/Operational-intent-references/operation/createOperationalIntentReference
    Update: https://redocly.github.io/redoc/?url=https://raw.githubusercontent.com/astm-utm/Protocol/v1.0.0/utm.yaml#tag/Operational-intent-references/operation/updateOperationalIntentReference
    """

    def __init__(self, extents: [utility.Extent], key: [], state, uss_base_url, subscription_id, new_subscription: utility.NewSubscription):

        self.extents = extents 
        self.key = key # TODO find out what a key is and why its in an array
        self.state = state
        self.uss_base_url = uss_base_url
        self.subscription_id = subscription_id
        self.new_subscription = new_subscription

    def to_json(self):
        return {
            "extents": [extent.to_json() for extent in self.extents],
            "key": [key for key in self.key] if self.key else [], # explanation of what a key is below
            "state": self.state,
            "uss_base_url": self.uss_base_url,
            "subscription_id": self.subscription_id,
            "new_subscription": self.new_subscription.to_json()
        }

        # Key
        # Array of Key (strings)
        # Proof that the USS creating or mutating this operational intent was aware of the current state of the airspace, with the 
        # expectation that this operational intent is therefore deconflicted from all relevant features in the airspace. This field 
        # is not required when declaring an operational intent Nonconforming or Contingent, or when there are no relevant Entities 
        # in the airspace, but is otherwise required. OVNs for constraints are required if and only if the USS managing this operational 
        # intent is performing the constraint processing role, which is indicated by whether the subscription associated with this 
        # operational intent triggers notifications for constraints. The key does not need to contain the OVN for the operational intent being updated.
    
    @classmethod
    def from_json(cls, json_obj):
        extents = [utility.Extent.from_json(extent) for extent in json_obj.get("extents", [])]
        key = json_obj.get("key", [])
        state = json_obj.get("state")
        uss_base_url = json_obj.get("uss_base_url")
        subscription_id = json_obj.get("subscription_id")
        new_subscription = utility.NewSubscription.from_json(json_obj.get("new_subscription", {}))

        return cls(extents, key, state, uss_base_url, new_subscription) 

    

class OperationalIntentReferenceQueryRequest:
    """
    DSS Query Operational Intent References request structure
    Query: https://redocly.github.io/redoc/?url=https://raw.githubusercontent.com/astm-utm/Protocol/v1.0.0/utm.yaml#tag/Operational-intent-references/operation/queryOperationalIntentReferences
    """
    def __init__(self, area_of_interest: utility.AreaOfInterest):
        self.area_of_interest = area_of_interest

    def to_json(self):
        return {
            "area_of_interest": self.area_of_interest
        }


