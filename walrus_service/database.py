from abc import ABC, abstractmethod
from typing import List

from models import Walrus, WalrusDict


class UniqueWalrusException(Exception):
    def __init__(self, name: str):
        """Exception for unique walrus constraint.

        Args:
            name (str): Name of the walrus causing the exception.
        """
        super().__init__(f"Walrus with name '{name}' already exists.")
        self.name = name


class WalrusNotFoundException(Exception):
    def __init__(self, name: str):
        """Exception for walrus not found.

        Args:
            name (str): Name of the walrus causing the exception.
        """
        super().__init__(f"Walrus {name} not found")
        self.name = name


class WalrusUnchangedException(Exception):
    def __init__(self, name: str):
        """Exception for walrus unchanged.

        Args:
            name (str): Name of the walrus causing the exception
        """
        super().__init__(f"Walrus {name} has not been modified.")
        self.name = name


class WalrusRepository(ABC):
    @abstractmethod
    def add(self, walrus: Walrus) -> None:
        """Add a walrus to the repository.

        Args:
            walrus (Walrus): The walrus to be added.

        Raises:
            NotImplementedError: If the method is not implemented.
        """
        raise NotImplementedError

    @abstractmethod
    def get(self, name: str) -> Walrus:
        """Get a walrus by name from the repository.

        Args:
            name (str): The name of the walrus to retrieve

        Raises:
            NotImplementedError: If the method is not implemented.

        Returns:
            Walrus: The retrieved walrus
        """
        raise NotImplementedError

    @abstractmethod
    def modify(self, name: str, favourite_food: str) -> None:
        """Modify a walrus by name in the repository.

        Args:
            name (str): The name of the walrus to modify
            favourite_food (str): The new favorite food of the walrus

        Raises:
            NotImplementedError: If the method is not implemented.
        """
        raise NotImplementedError

    @abstractmethod
    def get_all(self) -> List[WalrusDict]:
        """Get all walruses from the repository.

        Raises:
            NotImplementedError:  If the method is not implemented.

        Returns:
            List[Walrus]: The list of all walruses
        """
        raise NotImplementedError

    @abstractmethod
    def delete(self, name: str) -> None:
        """Delete a walrus by name from the repository.

        Args:
            name (str): The name of the walrus to delete

        Raises:
            NotImplementedError: If the method is not implemented.
        """
        raise NotImplementedError
