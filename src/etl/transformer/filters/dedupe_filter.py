import dedupe
from typing import List
from src.models.Event import Event

class DedupeFilter:
    """
    A filter that checks for similarity between events using dedupe library.
    """
    def __init__(self):
        """
        Initialize the DedupeFilter.
        """
        self.dedupe = dedupe.Dedupe({'title': {'type': 'String'}, 'description': {'type': 'String'}})

    def filter(self, events: List[Event]) -> List[Event]:
        """
        Filter the events based on similarity.

        Args:
        events: A list of Event objects to filter.

        Returns:
        A list of Event objects that pass the filter.
        """
        data_d = {idx: vars(event) for idx, event in enumerate(events)}
        self.dedupe.sample(data_d)
        threshold = self.dedupe.threshold(data_d, recall_weight=1)
        clustered_dupes = self.dedupe.match(data_d, threshold)

        filtered_events = [events[cluster[0][0]] for cluster in clustered_dupes]
        return filtered_events