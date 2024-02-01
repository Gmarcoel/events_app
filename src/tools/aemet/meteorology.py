import json
import requests
import math
from typing import Dict, Any

def _calculate_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Calculate the distance between two points given their latitudes and longitudes.
    
    @param lat1: Latitude of the first point.
    @param lon1: Longitude of the first point.
    @param lat2: Latitude of the second point.
    @param lon2: Longitude of the second point.
    @return: The distance between the two points.
    """
    return math.sqrt((lat1 - lat2)**2 + (lon1 - lon2)**2)

def _find_nearest_station(data: Dict[str, Any], latitude: float, longitude: float) -> Dict[str, Any]:
    """Find the nearest station to a given point.
    
    @param data: The data loaded from the JSON file.
    @param latitude: The latitude of the given point.
    @param longitude: The longitude of the given point.
    @return: The details of the nearest station.
    """
    min_distance = float('inf')
    nearest_station = None

    for station, details in data['stations'].items():
        distance = _calculate_distance(latitude, longitude, details['lat'], details['lng'])
        if distance < min_distance:
            min_distance    = distance
            nearest_station = details

    return nearest_station

def _get_api_response(api_link: str) -> Dict[str, Any]:
    """Send a GET request to an API link and get the response.
    
    @param api_link: The API link.
    @return: The response from the API as a dictionary.
    """
    response = requests.get(api_link)
    return response.json()



def get_precipitation_and_temperature(latitude, longitude):
    data            = coordinates
    nearest_station = _find_nearest_station(data, latitude, longitude)
    api_link        = data['link'] + nearest_station['link'] + '?api_key=' + data['key']

    response        = _get_api_response(api_link)

    if response['estado'] == 200:
        data_url        = response['datos']
        data_response   = _get_api_response(data_url)
        precipitation   = 0.0
        temperature     = 0.0
        if data_response:
            precipitation = data_response[0]['prec']
            temperature   = data_response[0]['ta']

            return precipitation, temperature
    return 0, 0

if __name__ == '__main__':
    latitude       = 40.0  # replace with given latitude
    longitude       = 3.0  # replace with given longitude
    get_precipitation_and_temperature(latitude, longitude)



coordinates = {
	"link": "https://opendata.aemet.es/opendata/api/observacion/convencional/datos/estacion/",
	"key": "XXXXXXXXXX",
	"stations": {
		"alcala": {
			"link": "3170Y/",
			"lat": 40.0305,
			"lng": 3.6041
		},
		"alpedrete": {
			"link": "3268C/",
			"lat": 40.6622,
			"lng": 4.0312
		},
		"aranjuez": {
			"link": "3100B",
			"lat": 40.0305,
			"lng": 3.6041
		},
		"arganda": {
			"link": "3182Y/",
			"lat": 40.3064,
			"lng": 3.4480
		},
		"buitrago": {
			"link": "3110C/",
			"lat": 40.9898,
			"lng": 3.6383
		},
		"colmenar": {
			"link": "3191E/",
			"lat": 40.6626,
			"lng": 3.7710
		},
		"madrid": {
			"link": "3195/",
			"lat": 40.4168,
			"lng": 3.7038
		},
		"pozuelo": {
			"link": "3194Y/",
			"lat": 40.4441,
			"lng": 3.8059
		},
		"puerto_alto": {
			"link": "3266A/",
			"lat": 40.7114,
			"lng": 4.1428
		},
		"puerto_navacerrada": {
			"link": "2462/",
			"lat": 40.7286,
			"lng": 4.0146
		},
		"rascafria": {
			"link": "3104Y/",
			"lat": 40.9050,
			"lng": 3.8795
		},
		"robledo": {
			"link": "3338/",
			"lat": 40.5050,
			"lng": 4.2345
		},
		"rozas_puerto_real": {
			"link": "3330Y/",
			"lat": 40.3092,
			"lng": 4.4922
		},
		"san_sebastian": {
			"link": "3125Y/",
			"lat": 40.5590,
			"lng": 3.6262
		},
		"somosierra": {
			"link": "3111D/",
			"lat": 41.1330,
			"lng": 3.5824
		},
		"tielmes": {
			"link": "3229Y/",
			"lat": 40.2476,
			"lng": 3.3125
		},
		"valdemorillo": {
			"link": "3343Y/",
			"lat": 40.4992,
			"lng": 4.0653
		}
	}
}