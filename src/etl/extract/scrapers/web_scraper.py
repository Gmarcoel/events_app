from abc import ABC, abstractmethod


class WebScraper(ABC):
    base_url = None

    @abstractmethod
    def get_data(self):
        """
        Abstract method for getting data from a website.
        Returns:
                List[Dict[str, Any]]: A list of dictionaries containing the data.
        """
        pass

    @abstractmethod
    def get_event_pages_urls(self):
        """
        Gets the URLs of the events.
        Returns:
                List[str]: A list of event URLs.
        """
        pass
