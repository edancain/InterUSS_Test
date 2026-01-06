#!/usr/bin/env python
import requests
from enum import Enum


class UtmScope(Enum):
    STRATEGIC_COORDINATION = "utm.strategic_coordination"        # Client may perform actions encompassed by the strategic coordination role including strategic conflict detection.
    CONSTRAINT_MANAGEMENT = "utm.constraint_management"          # Client may manage (create, edit, and delete) constraints according to the constraint management role.
    CONSTRAINT_PROCESSING = "utm.constraint_processing"          # Client may read constraint references from the DSS and details from the partner USSs according to the constraint processing role.
    CONFORMANCE_MONITORING_SA = "utm.conformance_monitoring_sa"  # Client may perform actions encompassed by the conformance monitoring for situational awareness role.
    AVAILABILITY_ARBITRATION = "utm.availability_arbitration"    # Client may set the availability state of USSs in the DSS.


class Authentication:
    @staticmethod
    def get_token(scopes):
        try:
            response = requests.get(
                "http://localhost:8085/token",
                params={
                    "grant_type": "client_credentials",
                    "scope": " ".join(scopes),
                    "intended_audience": "localhost",
                    "issuer": "localhost",
                    "sub": "check_scd"
                }
            )
            response.raise_for_status()
            return response.json().get('access_token')
        except requests.exceptions.RequestException as e:
            print(e)
            return "ERROR"


# test
if __name__ == "__main__":
    print(Authentication.get_token())
