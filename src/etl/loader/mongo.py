from pymongo import MongoClient
from typing import List

from src.models.Event import Event


class Database:
    def __init__(self, uri: str, db_name: str, collection_name: str):
        """
        Initializes a new instance of the Database class.

        Args:
        uri: A string representing the MongoDB connection URI.
        db_name: A string representing the name of the database.
        collection_name: A string representing the name of the collection.
        """
        self.client = MongoClient(uri)
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]

    def search_event(self, event_name: str) -> List[dict]:
        """
        Searches for an event in the collection.

        Args:
        event_name: A string representing the name of the event to search for.

        Returns:
        A list of dictionaries representing the events that match the search criteria.
        """
        return list(self.collection.find({"title": event_name}))

    def add_event(self, event: Event) -> None:
        """
        Adds an event to the collection.

        Args:
        event: A dictionary representing the event to add.
        """

        # Event to json
        event_json = event.toJson()
        self.collection.insert_one(event_json)


    def close(self) -> None:
        """
        Closes the database connection.
        """
        self.client.close()
