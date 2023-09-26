from typing import List

from database import (
    UniqueWalrusException,
    WalrusNotFoundException,
    WalrusRepository,
    WalrusUnchangedException,
)
from models import Walrus, WalrusDict
from pymongo import MongoClient


class WalrusManager(WalrusRepository):
    def __init__(self) -> None:
        """Establish connection with MongoDB."""
        self.client: MongoClient = MongoClient("walrus-db", port=27017)
        self.collection = self.client["workshop"]["walruses"]

    def add(self, walrus: Walrus) -> None:
        """Create a walrus record in the database.

        Args:
            walrus (Walrus): Walrus data.

        Raises:
            UniqueWalrusException: Exception if the walrus name is not unique.
        """
        existing_walrus = self.collection.find_one({"name": walrus.name})
        if existing_walrus:
            raise UniqueWalrusException(walrus.name)
        walrus_dict = walrus.dict()
        walrus_dict["birth_date"] = str(walrus_dict["birth_date"])
        self.collection.insert_one(walrus_dict)

    def get(self, name: str) -> Walrus:
        """Get walrus from the database by name.

        Args:
            name (str): Name of the walrus to be found.

        Returns:
            Walrus: Walrus data.

        Raises:
            WalrusNotFoundException: Exception if the walrus is not found.
        """
        walrus = self.collection.find_one({"name": name}, {"_id": 0})
        if walrus:
            return Walrus(**walrus)
        raise WalrusNotFoundException(name)

    def get_all(self) -> List[WalrusDict]:
        """Get all walruses from the database.

        Returns:
            List[WalrusDict]: List of found walruses.
        """
        walruses = self.collection.find({}, {"_id": 0})
        return [
            WalrusDict(
                name=walrus["name"],
                friends=walrus["friends"],
                favourite_food=walrus["favourite_food"],
                birth_date=walrus["birth_date"],
            )
            for walrus in walruses
        ]

    def modify(self, name: str, favourite_food: str) -> None:
        """Update a walrus by name.

        Args:
            name (str): Name of the walrus to be updated.
            favourite_food (str): New favorite food of the walrus.

        Raises:
            WalrusNotFoundException: Exception if the walrus is not found.
            WalrusUnchangedException: Exception if the data was not changed.
        """
        walrus = self.collection.find_one({"name": name})
        if walrus and walrus.get("favourite_food") == favourite_food:
            raise WalrusUnchangedException(name)

        update_result = self.collection.update_one(
            {"name": name},
            {"$set": {"favourite_food": favourite_food}},
        )
        if update_result.modified_count == 0:
            raise WalrusNotFoundException(name)

    def delete(self, name: str) -> None:
        """Delete walrus data from the database.

        Args:
            name (str): Name of the walrus to be deleted.

        Raises:
            WalrusNotFoundException: Exception if the walrus is not found.
        """
        result = self.collection.delete_one({"name": name})
        if result.deleted_count == 0:
            raise WalrusNotFoundException(name)


def get_db():
    try:
        db = WalrusManager()
        yield db
    finally:
        db.client.close()
