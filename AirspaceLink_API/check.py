import json
import re
import requests

from authentication import Authentication
from authentication import CheckAirspace_Response

class AirspaceChecker:
    def __init__(self, api_key, access_token):
        self.base_url = 'https://airhub-api-dev.airspacelink.com/v1/check/airspace'
        self.access_token = access_token
        self.api_key = api_key

    def validate_jwt(self):
        pattern = '^[^.]+\.[^.]+\.[^.]+$'
        if re.match(pattern, self.access_token):
            return 'Valid JWT'
        else:
            return 'Invalid JWT'


    # Checks the airspace based on the provided geometry and time range.
    # Returns:
    #CheckAirspace_Response: An object containing boolean values indicating if the airspace is controlled, enabled, and restricted.
    def check_airspace(self) -> CheckAirspace_Response: 
       
        header = {
            'Content-Type': 'application/json;charset=UTF-8',
            'Authorization': 'Bearer ' + self.access_token,
            'x-api-key': self.api_key
        }
        data = {
            "geometry": {
                "type": "Polygon",
                "coordinates": [
                    [
                        -112.02512913435557,
                        43.47753185851303
                    ],
                    [
                        -112.02512913435557,
                        43.47466874495615
                    ],
                    [
                        -112.02118361183014,
                        43.47466874495615
                    ],
                    [
                        -112.02118361183014,
                        43.47753185851303
                    ],
                    [
                        -112.02512913435557,
                        43.47753185851303
                    ]
                ]
            },
            "startTime": "2024-04-22T14:00:00.00Z",
            "endTime": "2024-04-22T15:00:00.00Z"
        }

        data = json.dumps(data)
        response = requests.post(
            url=self.base_url, 
            headers=header, 
            data=data
        )

        # the response is a json object that we will deserialize into an object type CheckAirspace_Response. The data content will have boolean returns named "controlled", "enabled", "restricted"
        check_air_response = CheckAirspace_Response.from_json(response.json())
        return check_air_response


class CheckAirspace_Response:
    def __init__(self, controlled, enabled, restricted):
        self.controlled = controlled
        self.enabled = enabled
        self.restricted = restricted

    @classmethod
    def from_json(cls, json_data):
        controlled = json_data.get('controlled')
        enabled = json_data.get('enabled')
        restricted = json_data.get('restricted')
        return cls(controlled, enabled, restricted)

    response_data = response.json()
    check_response = CheckAirspace_Response.from_json(response_data)
    print(check_response.controlled)
    print(check_response.enabled)
    print(check_response.restricted)
        



if __name__ == '__main__':
    api_key = "f15b282e5bd6495eae4cafe2d42b72e5"
    client_id = "WxFWfnwgy0xieXdWws6OqMifV1nE9Ek6"
    client_secret = "IFTBdP00Ta4mrHZFgpjP-n4i-G0eVG-OL42IFnfvGaK4qO_bYGUPGhnwFaeVWXXZ"
    authentication = Authentication(api_key, client_id, client_secret)
    access_token = authentication.request_token()
    access_token = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ild3dDk2SlJDTE9ER1pEeEpiRVVxdSJ9.eyJodHRwczovL2Fpcmh1Yi5haXJzcGFjZWxpbmsuY29tL3V0bSI6InZhbnRpcyIsImlzcyI6Imh0dHBzOi8vaWQtZGV2LmFpcnNwYWNlbGluay5jb20vIiwic3ViIjoiV3hGV2Zud2d5MHhpZVhkV3dzNk9xTWlmVjFuRTlFazZAY2xpZW50cyIsImF1ZCI6Imh0dHBzOi8vYXBpbS1lbmctZGV2LWN1cy5henVyZS1hcGkubmV0IiwiaWF0IjoxNzEwOTU1Mzg2LCJleHAiOjE3MTM1NDczODYsInNjb3BlIjoiaW5zaWdodHMuZGVtbyB0cmFmZmljOnJlYWQgc3lzdGVtOmFkbWluIGluc2lnaHRzOmRlbW8gc3lzdGVtOnJlYWQgdXNlcjpyZWFkIGFkdmlzb3J5OnJlYWQgcm91dGU6Y3JlYXRlIGFub25vcHM6cmVhZCBzdXJmYWNlOmNyZWF0ZSBmbGlnaHRsb2c6cmVhZCBpbnZpdGU6cmVhZCBpbnZpdGU6Y3JlYXRlIGludml0ZTpkZWxldGUgb3JnOnJlYWQgcm9sZTp1cGRhdGUgY3Jldzp1cGRhdGUgYWR2aXNvcnk6Y3JlYXRlIGFkdmlzb3J5OnVwZGF0ZSBhZHZpc29yeTpkZWxldGUgb3BlcmF0aW9uOnJlYWQgb3BlcmF0aW9uOmNyZWF0ZSBvcGVyYXRpb246dXBkYXRlIG9wZXJhdGlvbjpkZWxldGUgYWlyY3JhZnQ6cmVhZCBhaXJjcmFmdDpjcmVhdGUgYWlyY3JhZnQ6dXBkYXRlIGFpcmNyYWZ0OmRlbGV0ZSBmbGlnaHRsb2c6Y3JlYXRlIGZsaWdodGxvZzp1cGRhdGUgZmxpZ2h0bG9nOmRlbGV0ZSBhdmlhdGlvbjpyZWFkIHVzZXI6ZGVsZXRlIHVzZXI6cmVtb3ZlIGI0dWZseTp0ZXN0ZXIgdXNlci10eXBlOmRpcmVjdG9yIHVzZXItdHlwZTptYW5hZ2VyIHVzZXItdHlwZTpvcGVyYXRvciBoYXphcjpyZWFkIGVsZXZhdGlvbjpyZWFkIHd4OmFkdmFuY2VkOnJlYWQgdHJhZmZpYzpjcmVhdGUiLCJndHkiOiJjbGllbnQtY3JlZGVudGlhbHMiLCJhenAiOiJXeEZXZm53Z3kweGllWGRXd3M2T3FNaWZWMW5FOUVrNiIsInBlcm1pc3Npb25zIjpbImluc2lnaHRzLmRlbW8iLCJ0cmFmZmljOnJlYWQiLCJzeXN0ZW06YWRtaW4iLCJpbnNpZ2h0czpkZW1vIiwic3lzdGVtOnJlYWQiLCJ1c2VyOnJlYWQiLCJhZHZpc29yeTpyZWFkIiwicm91dGU6Y3JlYXRlIiwiYW5vbm9wczpyZWFkIiwic3VyZmFjZTpjcmVhdGUiLCJmbGlnaHRsb2c6cmVhZCIsImludml0ZTpyZWFkIiwiaW52aXRlOmNyZWF0ZSIsImludml0ZTpkZWxldGUiLCJvcmc6cmVhZCIsInJvbGU6dXBkYXRlIiwiY3Jldzp1cGRhdGUiLCJhZHZpc29yeTpjcmVhdGUiLCJhZHZpc29yeTp1cGRhdGUiLCJhZHZpc29yeTpkZWxldGUiLCJvcGVyYXRpb246cmVhZCIsIm9wZXJhdGlvbjpjcmVhdGUiLCJvcGVyYXRpb246dXBkYXRlIiwib3BlcmF0aW9uOmRlbGV0ZSIsImFpcmNyYWZ0OnJlYWQiLCJhaXJjcmFmdDpjcmVhdGUiLCJhaXJjcmFmdDp1cGRhdGUiLCJhaXJjcmFmdDpkZWxldGUiLCJmbGlnaHRsb2c6Y3JlYXRlIiwiZmxpZ2h0bG9nOnVwZGF0ZSIsImZsaWdodGxvZzpkZWxldGUiLCJhdmlhdGlvbjpyZWFkIiwidXNlcjpkZWxldGUiLCJ1c2VyOnJlbW92ZSIsImI0dWZseTp0ZXN0ZXIiLCJ1c2VyLXR5cGU6ZGlyZWN0b3IiLCJ1c2VyLXR5cGU6bWFuYWdlciIsInVzZXItdHlwZTpvcGVyYXRvciIsImhhemFyOnJlYWQiLCJlbGV2YXRpb246cmVhZCIsInd4OmFkdmFuY2VkOnJlYWQiLCJ0cmFmZmljOmNyZWF0ZSJdfQ.E0D9tGGXlnYopDmdugInHaJ8qze7cPv_b-VSEltlQtkEwZx1S5cMuNxlYZ58nX-rh_xdrxclBxAo_3RuAA0e1ftUxsu6cwY_sqlqXXi_pql_BlZG_YMlrHOEaENbmOX_VC8-JwE6ILVSdNUW2aiGNXGDmo2n18Jv63wLZTxU3fWm-Y3Aer56iI1TPS8fwQ_cMBIVWxwucKeDzmh5GKlFcLGmP8QunOyVQPr646X5i6FslBWXvZAmUYAbfFnsp7z-f6FGS9yv4jyrchdZkCvA6ipIsDdiyCW2ou02qcf_hQ-dSjOvOIia_-oy3LiK2nNKK5WgygXoKdWbzfc-RUFvNw'
    check1 = AirspaceChecker(api_key, access_token)
    success = check1.validate_jwt()

    
    response = check1.check_airspace()
    print("")
    print("")
    print("Response from Airspace Checker:")
    print(response.content)