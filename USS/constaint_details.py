from typing import List
from Utility import utility


# USS
class ConstraintDetails:  
    """
    USS A Constraint response includes a details structure. ConstraintDetails describes that structure
    Retrieve: https://redocly.github.io/redoc/?url=https://raw.githubusercontent.com/astm-utm/Protocol/v1.0.0/utm.yaml#tag/Constraint-details/operation/getConstraintDetails
    Notify: https://redocly.github.io/redoc/?url=https://raw.githubusercontent.com/astm-utm/Protocol/v1.0.0/utm.yaml#tag/Constraint-details/operation/notifyConstraintDetailsChanged
    """
    
    def __init__(self, volumes: List[utility.Volume], type, geozone: utility.Geozone = None):
        self.volumes = volumes
        self.type = type
        self.geozone = geozone

    def to_json(self):
        return {
            "volumes": [volume.to_json() for volume in self.volumes],
            "type": self.type,
            "geozone": self.geozone.to_json()
        }
    

class Constraint:
    """
    USS Constraint Details Retrieval response structure
    Retrieve: https://redocly.github.io/redoc/?url=https://raw.githubusercontent.com/astm-utm/Protocol/v1.0.0/utm.yaml#tag/Constraint-details/operation/getConstraintDetails
    """
    
    def __init__(self, reference: utility.Reference = None, details: ConstraintDetails = None):
        self.reference = reference
        self.details = details

    @classmethod
    def from_json(cls, data):
        reference = utility.Reference(data["reference"])
        details = utility.Details(data["details"])
        return cls(reference, details)

    def to_json(self):
        return {
            "reference": self.reference,
            "details": self.details
        }


class ConstraintRequest:
    """
    USS Constraint Details notify a peer USS of a changed constraint details response structure
    Notify: https://redocly.github.io/redoc/?url=https://raw.githubusercontent.com/astm-utm/Protocol/v1.0.0/utm.yaml#tag/Constraint-details/operation/notifyConstraintDetailsChanged
    """
    
    def __init__(self, constraint_id, constraint: Constraint, subscriptions: List[utility.Subscription]):
        self.constraint_id = constraint_id
        self.constraint = constraint
        self.subscriptions = subscriptions

    def to_json(self):
        return{
            "constraint_id": self.constraint_id,
            "constraint": self.constraint.to_json(),
            "subscriptions": [subscription.to_json() for subscription in self.subscriptions]
        }


class ConstraintResponse:
    """
    USS Constraint Details Retrieve Query response structure
    Retrieve: https://redocly.github.io/redoc/?url=https://raw.githubusercontent.com/astm-utm/Protocol/v1.0.0/utm.yaml#tag/Constraint-details/operation/getConstraintDetails
    """

    def __init__(self, data):
        self.constraint = Constraint.from_json(data["constraint"])



# Test
constraint_response_data = {
    "constraint": {
        "reference": {
              "id": "2f8343be-6482-4d1b-a474-16847e01af1e",
              "manager": "uss1",
              "uss_availability": "Unknown",
              "version": 1,
              "ovn": "9d158f59-80b7-4c11-9c0c-8a2b4d936b2d",
              "time_start": {
                "value": "1985-04-12T23:20:50.52Z",
                "format": "RFC3339"
              },
              "time_end": {
                "value": "1985-04-12T23:20:50.52Z",
                "format": "RFC3339"
              },
              "uss_base_url": "https://uss.example.com/utm"
            },
        "details": {
              "volumes": [
                {
                  "volume": {
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
                  },
                  "time_start": {
                    "value": "1985-04-12T23:20:50.52Z",
                    "format": "RFC3339"
                  },
                  "time_end": {
                    "value": "1985-04-12T23:20:50.52Z",
                    "format": "RFC3339"
                  }
                }
              ],
              "type": "com.example.non_utm_aircraft_operations",
              "geozone": {
                "identifier": "string",
                "country": "str",
                "zone_authority": [
                  {
                    "name": "string",
                    "service": "string",
                    "contact_name": "string",
                    "site_url": "string",
                    "email": "string",
                    "phone": "string",
                    "purpose": "AUTHORIZATION",
                    "interval_before": "string"
                  }
                ],
                "name": "string",
                "type": "COMMON",
                "restriction": "string",
                "restriction_conditions": [
                  "string"
                ],
                "region": 65535,
                "reason": [
                  "AIR_TRAFFIC"
                ],
                "other_reason_info": "string",
                "regulation_exemption": "YES",
                "u_space_class": "string",
                "message": "string",
                "additional_properties": None
              }
            }
    }
}


# Test script
def main():
    try:
        constraint_response = ConstraintResponse(constraint_response_data)
        print("ID:", constraint_response)
    except Exception as ex:
        print(ex)


if __name__ == '__main__':
    main()
