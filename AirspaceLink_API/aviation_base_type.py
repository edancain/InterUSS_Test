#!/usr/bin/env python

class AviationBase:
    def __init__(self, typ: str, geometry_type: str, coordinates: []):
        self.Type = typ
        self.GeometryType = geometry_type
        self.Coordinates = coordinates
