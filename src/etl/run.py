import json
import time
import os

from typing                                 import List, Dict, Any, Union

from models.event                           import Event
from transformer.filters.similarity_filter  import SimilarityFilter
from transformer.validators.validator       import EventValidator
from extract.scrapers.atrapalo_scraper      import AtrapaloScraper
from extract.scrap                          import scrape_activities

from tools.text_cls                         import EventClassifier
from tools.loader                           import MongoLoader as Database



def search_event(event_name: str) -> None:
    """
    Searches for an event in the database.

    Args:
    event_name: A string representing the name of the event to search for.
    """
    db = Database()
    results = db.search_event(event_name)

    print(f"Found {len(results)} results:")
    for result in results:
        print(result)


def add_events(events: List[Union[Event, Dict[str, Any]]]) -> None:
    """
	Adds array of events to database

    Args:
    events: A list of Event objects or dicrs to add to the database.    
    """

    db = Database()
    db.insert_data(events)
    db.close()

def clean_events() -> None:
    """
    Deletes all events from the database.
    """
    db = Database()
    db.delete_data()
    db.close()


def main() -> None:
    """
    The main ETL function.
    """

    # measure time
    start_time = time.time()

    # Check if the database is empty
    db = Database()
    if db.is_empty():
        if not os.path.exists("public/database.json"):
            print("Database is empty and no database file exists.")
        else:
            with open("public/database.json", "r") as f:
                data = json.load(f)
                if not isinstance(data, dict):
                    raise ValueError("Database file is not a dictionary.")
                events = data["events"]
                print(f"Found {len(events)} events in database file.")
                add_events(events)
                return

    else:
        if not os.path.exists("public/database.json"):
            print("Database is not empty but no database file exists. Exporting database.")
            db.export_database("public/database.json")
        else:
            print("Database is not empty. Exiting etl.")
        return



    # Wrapp all events from the APIs
    events = scrape_activities()
    print(f"Found {len(events)} events.")

    filter = SimilarityFilter()
    events = filter.filter(events)
    print(f"Found {len(events)} events after filtering.")

    # Validate the data to remove events without key elements
    validator = EventValidator()
    events = validator.validate(events)
    print(f"Found {len(events)} events after validation.")

    # Add subcategories to each event
    classifier = EventClassifier()
    events = classifier.classify_events(events)

    # Delete all documents in the database
    db.db.collection.delete_many({})
    
    # Add all events to the database
    print(f"Adding {len(events)} events to the database.")
    clean_events()
    add_events(events)

    print("--- %s seconds ---" % (time.time() - start_time))

    # Export the database to a file
    db.export_database("public/database.json")

    return


if __name__ == "__main__":
    main()
