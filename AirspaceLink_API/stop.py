#!/usr/bin/env python
import json


class Stop:

	def __init__(self, lat='0.00000', lon='0.00000'):
		self.lat = lat
		self.lon = lon


	def get_latitude(self) -> float:
		return self.lat


	def get_longitude(self) -> float:
		return self.lon


	def set_latitude(self, lat: float):
		self.lat = lat


	def set_longitude(self, lon: float):
		self.lon = lon


	def to_dict(self):
		return {'lat': self.lat, 'lon': self.lon}


	@classmethod
	def from_dict(cls, data):
		return cls(data['lat'], data['lon'])


	def to_json(self):
		return json.dumps(self.to_dict())
	

	@classmethod
	def from_json(cls, json_str):
		data = json.loads(json_str)
		return cls.from_dict(data)
