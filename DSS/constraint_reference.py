import sys
from pathlib import Path
# Add the parent directory to sys.path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from typing import List
from Utility import utility


# DSS
class ConstraintReferenceRequest:  
    """
    Request structure:
    DSS Create Constraint Reference: https://redocly.github.io/redoc/?url=https://raw.githubusercontent.com/astm-utm/Protocol/v1.0.0/utm.yaml#tag/Constraint-references/operation/createConstraintReference
    DSS Update Constraint Reference: https://redocly.github.io/redoc/?url=https://raw.githubusercontent.com/astm-utm/Protocol/v1.0.0/utm.yaml#tag/Constraint-references/operation/updateConstraintReference
    """
    def __init__(self, extents: [utility.Extent], uss_base_url):
        self.extents = extents
        self.uss_base_url = uss_base_url

    def to_json(self):
        return {
            "extents": [extent.to_json() for extent in self.extents],
            "uss_base_url": self.uss_base_url
        }
    
    @classmethod
    def from_json(cls, json_data):
        extents = [utility.Extent.from_json(extent_data) for extent_data in json_data.get("extents", [])]
        uss_base_url = json_data.get("uss_base_url", "")
        return cls(extents=extents, uss_base_url=uss_base_url)


class ConstraintReferenceQueryRequest:  
    """
    DSS Constraint Query: https://redocly.github.io/redoc/?url=https://raw.githubusercontent.com/astm-utm/Protocol/v1.0.0/utm.yaml#tag/Constraint-references/operation/queryConstraintReferences
    """
    def __init__(self, area_of_interest: utility.AreaOfInterest):
        self.area_of_interest = area_of_interest

    def to_json(self):
        return {
            "area_of_interest": self.area_of_interest
        }

class ConstraintReference: 
    """
    DSS Constraint Reference Retrieve Response: https://redocly.github.io/redoc/?url=https://raw.githubusercontent.com/astm-utm/Protocol/v1.0.0/utm.yaml#tag/Constraint-references/operation/getConstraintReference 
    """
    def __init__(self, data):
        self.id = data["id"]
        self.manager = data["manager"]
        self.uss_availability = data["uss_availability"]
        self.version = data["version"]
        self.ovn = data['ovn']
        self.time_start = utility.Time(data["time_start"])
        self.time_end = utility.Time(data["time_end"])
        self.uss_base_url = data["uss_base_url"]


class ConstraintReferenceResponse: 
    """
    Create DSS Constraint Reference: https://redocly.github.io/redoc/?url=https://raw.githubusercontent.com/astm-utm/Protocol/v1.0.0/utm.yaml#tag/Constraint-references/operation/createConstraintReference
    Update: https://redocly.github.io/redoc/?url=https://raw.githubusercontent.com/astm-utm/Protocol/v1.0.0/utm.yaml#tag/Constraint-references/operation/updateConstraintReference
    Delete: https://redocly.github.io/redoc/?url=https://raw.githubusercontent.com/astm-utm/Protocol/v1.0.0/utm.yaml#tag/Constraint-references/operation/deleteConstraintReference
    """
    def __init__(self, data):
        self.subscribers = [utility.Subscriber(opIntRef) for opIntRef in data["subscribers"]]
        self.constraint_reference = ConstraintReference(data["constraint_reference"])


class ConstraintReferences:  
    """
    Query Constraints Structure:
    Query: https://redocly.github.io/redoc/?url=https://raw.githubusercontent.com/astm-utm/Protocol/v1.0.0/utm.yaml#tag/Constraint-references/operation/queryConstraintReferences
    """
    def __init__(self, data):
        self.constraint_references = [ConstraintReference(opIntRef) for opIntRef in data["constraint_references"]] # TODO, check that this is a list of ConstraintReferences, not a list of ConstraintReferenceResponses


constraint_ref_response_data = {  # creation, update, delete
    "subscribers": [],
    "constraint_reference": {
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
    }
}



# Test
constraint_ref_data = {  # Query
    "constraint_reference": {
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
    }
}


# Test script
def main():
    try:
        constraint_reference_response = ConstraintReferenceResponse(constraint_ref_response_data)
        constraint_reference = ConstraintReference(constraint_ref_data["constraint_reference"])
        print("ID:", constraint_reference_response.id)
    except Exception as ex:
        print(ex)


if __name__ == '__main__':
    main()
