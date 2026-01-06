# USS USE
import sys
from pathlib import Path
# Add the parent directory to sys.path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from Utility import utility
from DSS import subscription
from typing import List
import json


# USS
class OperationalIntentDetails:  
    """
    USS Operational Intent Details Retrieve response structure
    Retrieve: https://redocly.github.io/redoc/?url=https://raw.githubusercontent.com/astm-utm/Protocol/v1.0.0/utm.yaml#tag/Operational-intent-details/operation/getOperationalIntentDetails
    """
    
    def __init__(self, reference: utility.Reference, details: utility.Details):
        self.reference = reference
        self.details = details

    def to_json(self):
        return {
            "reference": self.reference.to_json(),
            "details": self.details.to_json()
        }
    
    @classmethod
    def from_json(cls, data):
        reference = utility.Reference(data.get("operational_intent", {}).get("reference", {}))
        details = utility.Details(data.get("operational_intent", {}).get("details", {}))


class OperationalIntentOffNominal: 
    """
    USS Operational Intent Details Query detailed information on the position of an off-nominal operational intent from a USS response
    Query: https://redocly.github.io/redoc/?url=https://raw.githubusercontent.com/astm-utm/Protocol/v1.0.0/utm.yaml#tag/Operational-intent-details/operation/getOperationalIntentTelemetry
    """
    
    def __init__(self, operational_intent_id: str, telemetry: utility.Telemetry, next_telemetry_opportunity: utility.NextTelemetryOpportunity):
        self.operational_intent_id = operational_intent_id
        self.telemetry = telemetry
        self.next_telemetry_opportunity = next_telemetry_opportunity

    def to_json(self):
        return {
            "operational_intent_id": self.operational_intent_id,
            "telemetry": self.telemetry.to_json(),
            "next_telemetry": self.next_telemetry_opportunity.to_json()
        }
    
    @classmethod
    def from_json(cls, data):
        operational_intent_id = data.get("operational_intent_id")
        telemetry = utility.Telemetry(data.get("telemetry"))
        next_telemetry_opportunity = utility.NextTelemetryOpportunity(data.get("next_telemetry_opportunity"))
        
    


class OperationalIntentDetailsChanged: 
    """
    USS Operational Intent Details Notify a peer USS of changed operational Intent request structure
    Notify: https://redocly.github.io/redoc/?url=https://raw.githubusercontent.com/astm-utm/Protocol/v1.0.0/utm.yaml#tag/Operational-intent-details/operation/notifyOperationalIntentDetailsChanged
    """
    
    def __init__(self, operational_intent_id, operational_intent: OperationalIntentDetails, subscriptions: List[utility.Subscription]):
        self.operational_intent_id = operational_intent_id
        self.operational_intent = operational_intent
        self.subscriptions = subscriptions
    
    @classmethod
    def from_json(cls, data):
        operational_intent_id = data["operational_intent_id"]
        operational_intent = OperationalIntentDetails(data["operational_intent"])
        subscriptions = [utility.Subscription(subscription) for subscription in data["subscriptions"]]
        return cls(operational_intent_id, operational_intent, subscriptions)

    def to_json(self):
        return {
            "operational_intent_id": self.operational_intent_id,
            "operational_intent": self.operational_intent,
            "subscriptions": self.subscriptions
        }


op_intent = {
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
            "volumes": [{
                    "outline_circle": {
                    "center": {
                    "lng": -118.456,
                    "lat": 34.123
                    },
                    "radius": {
                    "value": 300.183,
                    "units": "M"
                    }
                    },
                    "outline_polygon": {
                    "vertices": [
                    {
                    "lng": -118.456,
                    "lat": 34.123
                    },
                    {
                    "lng": -118.456,
                    "lat": 34.123
                    },
                    {
                    "lng": -118.456,
                    "lat": 34.123
                    }
                    ]
                    },
                    "altitude_lower": {
                        "value": -8000,
                        "reference": "W84",
                        "units": "M"
                    },
                    "altitude_upper": {
                        "value": -8000,
                        "reference": "W84",
                        "units": "M"
                    }
            }],
            "off_nominal_volumes": [],
            "priority": 0
        }
    }
}   

off_nominal = {
  "operational_intent_id": "2f8343be-6482-4d1b-a474-16847e01af1e",
  "telemetry": {
    "time_measured": {
      "value": "1985-04-12T23:20:50.52Z",
      "format": "RFC3339"
    },
    "position": {
      "longitude": -118.456,
      "latitude": 34.123,
      "accuracy_h": "HAUnknown",
      "accuracy_v": "VAUnknown",
      "extrapolated": False,
      "altitude": {
        "value": -8000,
        "reference": "W84",
        "units": "M"
      }
    },
    "velocity": {
      "speed": 200.1,
      "units_speed": "MetersPerSecond",
      "track": 120
    }
  },
  "next_telemetry_opportunity": {
    "value": "1985-04-12T23:20:50.52Z",
    "format": "RFC3339"
  }
}
    
    
    # Test script

changed_op_intent = {
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
}


def main():
    try:
        response = OperationalIntentDetails(op_intent)
        print("ID:", response.reference.id)

        offnom = OperationalIntentOffNominal(off_nominal)
        print("Off Nominal:", offnom.telemetry.position.latitude)

        start_time = utility.Time("1985-04-12T23:20:50.52Z", "RFC3339")
        end_time = utility.Time("1985-04-12T23:20:50.52Z", "RFC3339")
        reference = utility.Reference("2f8343be-6482-4d1b-a474-16847e01af1e", "uss1","Unknown", 1, "Accepted", "9d158f59-80b7-4c11-9c0c-8a2b4d936b2d", start_time, end_time, "https://uss.example.com/utm", "78ea3fe8-71c2-4f5c-9b44-9c02f5563c6f")
        
        deets = utility.Details(volumes, offnominalVolumes, priority)
        
        sub = subscription.USS_Subscription("78ea3fe8-71c2-4f5c-9b44-9c02f5563c6f", 0)
        opintent_details = OperationalIntentDetails(reference, )
        opintent_details = OperationalIntentDetailsChanged()
    except Exception as ex:
        print(ex)


if __name__ == '__main__':
    main()