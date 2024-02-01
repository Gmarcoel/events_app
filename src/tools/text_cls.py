from typing import List, Dict
from transformers import pipeline
from etl.models.event import Event

class EventClassifier:
    """
    A class used to classify events into categories.

    ...

    Attributes
    ----------
    classifier : Pipeline
        an instance of the zero-shot-classification pipeline
    categories : List[str]
        a list of categories to classify events into

    Methods
    -------
    classify_events(events: List[Dict[str, str]]) -> Dict[str, List[float]]:
        Classifies the events into categories and returns a dictionary mapping event titles to category scores.
    """

    def __init__(self):
        """
        Constructs all the necessary attributes for the EventClassifier object.
        """
        self.classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")
        self.categories = ['with children', 'outdoors', 'exciting', 'calm', 'funny', 'energic']
        # categories en español
        self.categorias = ['con niños', 'al aire libre', 'emocionante', 'tranquilo', 'divertido', 'energico']

    def classify_events(self, events: List[Event]) -> List[Event]:
        """
        Classifies the events into categories.

        @param events: a list of events where each event is a dictionary with a 'title' key
        @return: events with subcategories added
        """
        for event in events:
            for index, categoria in enumerate(self.categorias):
                res = self.classifier(event.title + ' ' + event.description, [categoria, 'no ' + categoria])
                event.subcategories[self.categories[index]] = res['scores'][0]
            
            # categories = self.classifier(event.title + ' ' + event.description, self.categories)
            # output = {'sequence': sequence, 'labels': labels, 'scores': scores}
            # event.categories = {category: score, ...}
            # event.subcategories = dict(zip(categories['labels'], categories['scores']))
        
        return events

"""
start_time = time.time()

classifier = pipeline("zero-shot-classification",
                      model="facebook/bart-large-mnli")

sequence_to_classify = "one day I will see the world"
candidate_labels = ['travel', 'cooking', 'dancing']
output = classifier(sequence_to_classify, candidate_labels)

print(output)


print("--- %s seconds ---" % (time.time() - start_time))
"""