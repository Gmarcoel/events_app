from abc import ABC, abstractmethod

class Validator(ABC):
    @abstractmethod
    def validate(self, events):
        pass

class EventValidator(Validator):
    """
    Filter the events based on some criteria.

    Args:
    events: A list of Event objects to filter.

    Returns:
    A list of Event objects that pass the filter.
    """
    def validate(self, events):
        if not events:
            return []
        valid_events = []
        for event in events:
            if not event.title:
                continue
            if not event.description:
                continue
            try :
                longitude_float = float(event.coordinates[1])
                latitude_float = float(event.coordinates[0])
                if not longitude_float or not -180 <= latitude_float <= 180:
                    continue
            except ValueError:
                continue

            valid_events.append(event)

        return valid_events