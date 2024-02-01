from typing import Any, Dict, List
import json
import requests

from src.models.Event import Event
from src.models.Wrapper import Wrapper

class MadridEventAPI(Wrapper):
    def __init__(self):
        """
        A class representing an API wrapper for Madrid events.
        """
        self.api_url : str = "https://datos.madrid.es/egob/catalogo/206974-0-agenda-eventos-culturales-100.json"

    def get_data(self) -> List[Dict[str, Any]]:
        """
        Gets data from the Madrid events API.
        Returns:
                List[Dict[str, Any]]: A list of dictionaries containing the data.
        """
        try:
            response = requests.get(self.api_url)
            if response.status_code == 200:
                data = response.json()
                events = []

                for event_data in data['@graph']:
                    title = event_data.get('title', 'N/A')
                    price = event_data.get('offers', {}).get('price', 'N/A')
                    description = event_data.get('description', 'N/A')
                    dtstart = event_data.get('dtstart', 'N/A')
                    event_type = event_data.get(
                        '@type', '').split('/')[-1] if '@type' in event_data else 'N/A'
                    location = event_data.get('location', {})
                    latitude = location.get('latitude', 'N/A')
                    longitude = location.get('longitude', 'N/A')

                    event = Event(title, price, description, dtstart,
                                  event_type, latitude, longitude)
                    events.append(event)

                return events
            else:
                print(
                    f"Failed to retrieve data. Status code: {response.status_code}")
                return []
        except Exception as e:
            print(f"Failed to retrieve data. Exception: {e}")
            return []

    """
    Exports the data to a JSON file.
    Args:
            filename (str): The name of the file.
    """
    def export_to_json(self, filename):
        events = self.get_data()
        if events:
            with open(filename, 'w') as file:
                event_list = [vars(event) for event in events]
                json.dump(event_list, file, indent=2)

if __name__ == '__main__':
    madrid_api = MadridEventAPI("https://datos.madrid.es/egob/catalogo/206974-0-agenda-eventos-culturales-100.json")
    madrid_api.export_to_json("madrid_events.json")
