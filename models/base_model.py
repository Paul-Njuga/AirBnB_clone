#!/usr/bin/python3
"""Base Model class
Contains the Base class for the AirBnB clone console.
"""

import uuid
from datetime import datetime
from models import storage


class BaseModel:
    """Define the base for all other classes."""

    def __init__(self, *args, **kwargs):
        """Initialization of a Base instance.
        Attributes:
            *args: list of arguments
            **kwargs: dict of key-value arguments
        """
        if not kwargs:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
            storage.new(self)
        else:
            kwargs["created_at"] = datetime.strptime(
                kwargs["created_at"], "%Y-%m-%dT%H:%M:%S.%f"
            )
            kwargs["updated_at"] = datetime.strptime(
                kwargs["updated_at"], "%Y-%m-%dT%H:%M:%S.%f"
            )
            del kwargs["__class__"]
            self.__dict__.update(kwargs)

    def __str__(self):
        """Returns an informal and nicely printable string representation
        of a BaseModel instance."""

        return "[{}] ({}) {}".format(
            type(self).__name__, self.id, self.__dict__
        )

    def save(self):
        """Updates the public instance attribute updated_at
        with the current datetime"""

        self.updated_at = datetime.now()
        storage.save()

    def to_dict(self):
        """Returns the dictionary representation of a BaseModel."""

        my_dict = self.__dict__.copy()
        my_dict["__class__"] = type(self).__name__
        my_dict["created_at"] = my_dict["created_at"].isoformat()
        my_dict["updated_at"] = my_dict["updated_at"].isoformat()
        return my_dict
