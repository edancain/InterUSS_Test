#!/usr/bin/env python3
import json

class Layer:
    def __init__(self, code, risk):
        self.code = code
        self.risk = risk

    def to_json(self):
        return json.dumps({
            "code": self.code,
            "risk": self.risk
        })
    

class Layers:
    def __init__(self):
        self.layers = []

    def add_layer(self, new_layer: Layer):
        self.layers.append(new_layer)

    def to_json(self):
        layers_json = []
        for layer in self.layers:
            layers_json.append({
                "code": layer.code,
                "risk": layer.risk
            })
        return layers_json