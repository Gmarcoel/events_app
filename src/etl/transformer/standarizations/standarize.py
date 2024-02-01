class Standarize:
    @staticmethod
    def standarize_data(data):
        # Function to standardize data
        # Placeholder - Replace this with your standardization logic
        pass

class StandarizePrice(Standarize):
    @staticmethod
    def standarize_price(events):
        # Function to standardize prices within a list of events
        for event in events:
            if hasattr(event, 'price') and isinstance(event.price, str):
                # Check if 'event' has 'price' attribute and if 'price' is a string
                if event.price.strip() == '' or event.price.lower() == 'nan':
                    event.price = -1  # Change empty strings or 'NaN' to -1
                else:
                    try:
                        event.price = round(float(event.price), 2)  # Convert to float and round to 2 decimal places
                    except (ValueError, TypeError):
                        event.price = -1  # Set to -1 if conversion to float fails
            elif not hasattr(event, 'price'):
                # If 'price' attribute doesn't exist, set it to -1
                event.price = -1
        return events

# Example usage:
class Event:
    def __init__(self, price):
        self.price = price

events = [Event("10.567"), Event("15.321"), Event(""), Event("NaN"), Event(20)]

# Standardize prices in the list of events
standardized_events = StandarizePrice.standarize_price(events)

for event in standardized_events:
    print(event.price)
