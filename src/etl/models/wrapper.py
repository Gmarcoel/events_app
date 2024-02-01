from abc import ABC, abstractmethod
from typing import List, Dict, Any, Union


class Wrapper(ABC):
    @abstractmethod
    def get_data(self) -> List[Dict[str, Any]]:
        """
        Abstract method for getting data from an API.
        Returns:
                List[Dict[str, Any]]: A list of dictionaries containing the data.
        """
        pass