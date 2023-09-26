from typing import List

from database import (
    UniqueWalrusException,
    WalrusNotFoundException,
    WalrusRepository,
    WalrusUnchangedException,
)
from models import Walrus, WalrusDict


class InMemoryWalrusRepository(WalrusRepository):
    def __init__(self) -> None:
        self.database: dict[str, Walrus] = dict()

    def add(self, walrus: Walrus) -> None:
        """Create a walrus record in the database.

        Args:
            walrus (Walrus): Walrus data

        Raises:
            UniqueWalrusException: Exception if the walrus name is not unique.
        """
        if walrus.name in self.database:
            raise UniqueWalrusException(walrus.name)
        self.database[walrus.name] = walrus

    def get(self, name: str) -> Walrus:
        """Get walrus from the db by name.

        Args:
            name (str): Name of the walrus to be found.

        Returns:
            Walrus: Walrus data.
        """
        if name in self.database:
            return self.database[name]
        raise WalrusNotFoundException(name)

    def get_all(self) -> List[WalrusDict]:
        """Get all walruses from the db.

        Returns:
            List[WalrusDict]: List of walrus data.
        """
        walruses_data: List[WalrusDict] = []
        for walrus in self.database.values():
            walrus_data: WalrusDict = {
                "name": walrus.name,
                "friends": walrus.friends,
                "favourite_food": walrus.favourite_food,
                "birth_date": walrus.birth_date,
            }
            walruses_data.append(walrus_data)
        return walruses_data

    def modify(self, name: str, favourite_food: str) -> None:
        """Update a walrus by name.

        Args:
            name (str): Name of the walrus to be modified.
            favourite_food (str): New favorite food for the walrus.

        Raises:
            WalrusNotFoundException: Exception if the walrus is not found.
            WalrusUnchangedException: Exception if the walrus data was not
            changed.
        """
        walrus = self.get(name)
        if walrus is not None:
            walrus.favourite_food = favourite_food
        else:
            raise WalrusNotFoundException(name)
        if walrus.favourite_food == favourite_food:
            raise WalrusUnchangedException(name)

    def delete(self, name: str) -> None:
        """Delete walrus data from the db.

        Args:
            name (str): Name of the walrus to be deleted.

        Raises:
            WalrusNotFoundException: Exception if the walrus is not found.
        """
        if name in self.database:
            del self.database[name]
        else:
            raise WalrusNotFoundException(name)


def get_database() -> WalrusRepository:
    """Get the WalrusRepository instance.

    Returns:
        WalrusRepository: Walrus repository instance.
    """
    return InMemoryWalrusRepository()
