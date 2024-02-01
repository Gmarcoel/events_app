from typing import List, Dict, Any, Union

class Event:
    def __init__(self, title: str, description: str, price: Union[str, int], address: str, date: str, categories: Union[str, List], latitude: Union[str, float], longitude: Union[str, float], language: str, portrait: str, images: List[str], data: Dict[str, Any] = {}, comments: List = []):
        """
        A class representing an event.
        Args:
                price (Union[str, int]): The price of the event.
                description (str): The description of the event.
                dtstart (str): The start date and time of the event.
                event_type (str): The type of the event.
                latitude (Union[str, float]): The latitude of the event location.
                longitude (Union[str, float]): The longitude of the event location.
        """
        self.title = title
        self.description = description
        self.price = price
        self.address = address
        self.coordinates = (latitude, longitude)
        self.date = date
        self.categories = categories
        self.language = language
        self.portrait = portrait
        self.images = images
        self.subcategories = {}
        self.data = data
        self.comments = comments

    def __str__(self):
        return f"{self.title} - {self.date} - {self.price} - {self.address} - {self.categories} - {self.language}"

    def __dict__(self):
        return {
            "title": self.title,
            "description": self.description,
            "price": self.price,
            "address": self.address,
            "coordinates": {
                "latitude": self.coordinates[0],
                "longitude": self.coordinates[1]
            },
            "date": self.date,
            "categories": self.categories,
            "language": self.language,
            "portrait": self.portrait,
            "images": self.images,
            "subcategories": self.subcategories,
            "data": self.data,
            "comments": self.comments
        }

    """
    A method to add subcategories to the event.
    Args:
        subcategories (Dict[str, float]): A dictionary with the subcategories and their scores.
    """
    def add_subcategories(self, subcategories: Dict[str, float]):
        self.subcategories.update(subcategories)


