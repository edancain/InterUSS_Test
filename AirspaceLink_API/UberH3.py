import requests
import h3

class GetH3():        
    @classmethod
    def get_hex_geojson_from_h3(cls, hex_id):
        value = h3.h3_to_geo_boundary(hex_id, True)
        value_with_brackets = [[list(coord) for coord in value]]
        print()
        print(value_with_brackets)
        return value_with_brackets

'''
if __name__ == '__main__':

    # Example list of hex IDs
    hex_values = ['8a2989908177fff', '8a2989908157fff', '8a298990802ffff', '8a298990800ffff', '8a29899080e7fff', '8a29899080f7fff', '8a29899080d7fff', '8a29899080dffff', '8a2989908767fff', '8a2989908747fff', '8a298990874ffff', '8a29899082b7fff', '8a29899082a7fff', '8a2989908217fff']

    for hex_id in hex_values:
        hex_geojson = GetH3.get_hex_geojson_from_h3(hex_id)
        if hex_geojson:
            print(hex_geojson)
'''