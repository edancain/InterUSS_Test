import sys
from pathlib import Path
# Add the parent directory to sys.path
sys.path.append(str(Path(__file__).resolve().parent.parent))
from Utility.utility import Extent, AreaOfInterest
from typing import List

from DSS.operational_intent_reference import OperationalIntentReference, OperationalIntentReferences


class Subscription:
    """
    DSS Subscription, Retrieve specified subscription response structure
    Retrieve: https://redocly.github.io/redoc/?url=https://raw.githubusercontent.com/astm-utm/Protocol/v1.0.0/utm.yaml#tag/Subscriptions/operation/getSubscription 
    Delete: https://redocly.github.io/redoc/?url=https://raw.githubusercontent.com/astm-utm/Protocol/v1.0.0/utm.yaml#tag/Subscriptions/operation/deleteSubscription
    """
    
    def __init__(self, id=None, version=None, notification_index=None, time_start=None, time_end=None, uss_base_url=None, notify_for_operational_intents=None, notify_for_constraints=None, implicit_subscription=None, dependent_operational_intents=None):
        self.id = id
        self.version = version
        self.notification_index = notification_index
        self.time_start = time_start
        self.time_end = time_end
        self.uss_base_url = uss_base_url
        self.notify_for_operational_intents = notify_for_operational_intents
        self.notify_for_constraints = notify_for_constraints
        self.implicit_subscription = implicit_subscription
        self.dependent_operational_intents = dependent_operational_intents or []

    def to_json(self):
        return {
            "id": self.id,
            "version": self.version,
            "notification_index": self.notification_index,
            "time_start": self.time_start,
            "time_end": self.time_end,
            "uss_base_url": self.uss_base_url,
            "notify_for_operational_intents": self.notify_for_operational_intents,
            "notify_for_constraints": self.notify_for_constraints,
            "implicit_subscription": self.implicit_subscription,
            "dependent_operational_intents": self.dependent_operational_intents
        }

    @classmethod
    def from_json(cls, json_data):
        return cls(**json_data)

class Subscription_Response:
    def __init__(self, subscription: Subscription, operational_intent_references: [], constraint_references: []):
        self.subscription = subscription
        self.operational_intent_references = operational_intent_references or []
        self.constraint_references = constraint_references or []

    def to_json(self):
        return {
            "subscription": self.subscription.to_json() if self.subscription else None,
            "operational_intent_references": self.operational_intent_references,
            "constraint_references": self.constraint_references
        }

    @classmethod
    def from_json(cls, json_data):
        subscription_data = json_data.get("subscription")
        operational_intent_references = json_data.get("operational_intent_references", [])
        constraint_references = json_data.get("constraint_references", [])
        return cls(
            subscription=Subscription(**subscription_data) if subscription_data else None,
            operational_intent_references=operational_intent_references,
            constraint_references=constraint_references
        )

class USS_Subscription:
    """
    USS. Notify peer USS of changed constraint details requires a list of subscriptions, but each only needs a Subscription_id and Notification_index
    https://redocly.github.io/redoc/?url=https://raw.githubusercontent.com/astm-utm/Protocol/v1.0.0/utm.yaml#tag/p2p_utm/operation/notifyConstraintDetailsChanged
    """
    def __init__(self, subscription_id, notification_index):
        self.subscription_id = subscription_id
        self.notification_index = notification_index

    def to_json(self):
        return {
            "subscription_id": self.subscription_id,
            "notification_index": self.notification_index
        }

class SubscriptionRequest:
    """
    DSS Subscription Creation, and Update request structure
    Create: https://redocly.github.io/redoc/?url=https://raw.githubusercontent.com/astm-utm/Protocol/v1.0.0/utm.yaml#tag/Subscriptions/operation/createSubscription
    Update: https://redocly.github.io/redoc/?url=https://raw.githubusercontent.com/astm-utm/Protocol/v1.0.0/utm.yaml#tag/Subscriptions/operation/updateSubscription
    """

    def __init__(self, extents: Extent, uss_base_url, notify_for_operational_intents: bool, notify_for_constraints: bool):
        self.extents = extents
        self.uss_base_url = uss_base_url
        self.notify_for_operational_intents = notify_for_operational_intents
        self.notify_for_constraints = notify_for_constraints

    def to_json(self):
        return {
            "extents": self.extents.to_json(),
            "uss_base_url": self.uss_base_url,
            "notify_for_operations": self.notify_for_operational_intents,
            "notify_for_constraints": self.notify_for_constraints
        }
    
    @classmethod
    def from_json(cls, subscription_json):
        extents = subscription_json.get("extents", [])
        uss_base_url = subscription_json.get("uss_base_url", "")
        notify_for_operations = subscription_json.get("notify_for_operations", False)
        notify_for_constraints = subscription_json.get("notify_for_constraints", False)

        return cls(extents, uss_base_url, notify_for_operations, notify_for_constraints)

        

class Subscriptions: # Response
    """
    DSS Subscriptions Query response structure
    Query: https://redocly.github.io/redoc/?url=https://raw.githubusercontent.com/astm-utm/Protocol/v1.0.0/utm.yaml#tag/Subscriptions/operation/querySubscriptions
    """
    
    def __init__(self, data):
        # self.subscriptions = List[Subscription(data["subscriptions"])]
        self.subscriptions = [Subscription(sub_data) for sub_data in data.get("subscriptions", [])]


class SubscriptionsQueryRequest:
    """
    DSS Subscriptions Query request structure
    Query: https://redocly.github.io/redoc/?url=https://raw.githubusercontent.com/astm-utm/Protocol/v1.0.0/utm.yaml#tag/Subscriptions/operation/querySubscriptions
    """

    def __init__(self, area_of_interest: AreaOfInterest):
        self.area_of_interest = area_of_interest

    def to_json(self):
        return {
            "area_of_interest": self.area_of_interest
        }  
    

# Test data
subscription_data = {
        "id": "78ea3fe8-71c2-4f5c-9b44-9c02f5563c6f",
        "version": "string",
        "notification_index": 0,
        "time_start": {
            "value": "1985-04-12T23:20:50.52Z",
            "format": "RFC3339"
        },
        "time_end": {
            "value": "1985-04-12T23:20:50.52Z",
            "format": "RFC3339"
        },
        "uss_base_url": "https://uss.example.com/utm",
        "notify_for_operational_intents": False,
        "notify_for_constraints": False,
        "implicit_subscription": False,
        "dependent_operational_intents": []

}   


# Test script
def main():
    subscription = Subscription(subscription_data)
    print("ID:", subscription.id)


if __name__ == '__main__':
    main()
