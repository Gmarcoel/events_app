from abc import ABC, abstractmethod
from typing import List
from models.event import Event

class EventFilter(ABC):
    """
    This is an interface for event filters. Each specific filter should be a subclass of this class and implement the filter method.
    """

    @abstractmethod
    def filter(self, events: List[Event]) -> List[Event]:
        """
        Filter the events based on some criteria.

        Args:
        events: A list of Event objects to filter.

        Returns:
        A list of Event objects that pass the filter.
        """
        pass

