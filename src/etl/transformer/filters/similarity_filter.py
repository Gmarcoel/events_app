from transformer.filters.event_filter import EventFilter
from models.event import Event

import difflib
import re
from typing import List

class SimilarityFilter(EventFilter):
    """
    A filter that checks for similarity between events based on a threshold.
    """
    def __init__(self, threshold: float = 0.8):
        """
        Initialize the SimilarityFilter with a threshold.

        Args:
        threshold: A float value that defines the similarity threshold.
        """
        self.threshold = threshold

    def filter(self, events: List[Event]) -> List[Event]:
        """
        Filter the events based on similarity.

        Args:
        events: A list of Event objects to filter.

        Returns:
        A list of Event objects that pass the filter.
        """
        if not events:
            return []
        filtered_events = []
        for event in events:
            if not self._is_similar(event, filtered_events):
                filtered_events.append(event)
        return filtered_events

    def _is_similar(self, event: Event, event_list: List[Event]) -> bool:
        """
        Check if an event is similar to any event in a list of events.

        Args:
        event: An Event object to check for similarity.
        event_list: A list of Event objects to compare with.

        Returns:
        True if the event is similar to any event in the list, False otherwise.
        """
        for existing_event in event_list:
            if self._calculate_similarity(event.title, existing_event.title) > self.threshold and \
               self._calculate_similarity(event.description, existing_event.description) > self.threshold:
                return True
        return False

    def _calculate_similarity(self, str1: str, str2: str) -> float:
        """
        Calculate the similarity between two strings.

        Args:
        str1, str2: The two strings to compare.

        Returns:
        A float value that represents the similarity ratio between the two strings.
        """
        str1 = self._normalize_string(str1)
        str2 = self._normalize_string(str2)
        return difflib.SequenceMatcher(None, str1, str2).ratio()

    def _normalize_string(self, s: str) -> str:
        """
        Normalize a string by converting it to lower case and removing certain substrings.

        Args:
        s: The string to normalize.

        Returns:
        The normalized string.
        """
        s = s.lower()
        s = re.sub(r'\b(c/|calle|av\.|avd\.|avda\.)\b', '', s)
        return s