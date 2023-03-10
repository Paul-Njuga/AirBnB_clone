"""File Storage class
Contains the Storage class for the AirBnB clone console.
"""
import json
import os


class FileStorage:
    """Serializes instances to a JSON file,
    & deserializes JSON file to instances"""
    __file_path = "file.json"
    __objects = {}

    def all(self):
        """Returns the dictionary __objects"""
        return FileStorage.__objects

    def new(self, obj):
        """Sets in __objects the obj with key <obj class name>.id"""
        key = "{}.{}".format(type(obj).__name__, obj.id)
        FileStorage.__objects[key] = obj

    def save(self):
        """Serializes __objects to the JSON file (path: __file_path)"""
        with open(FileStorage.__file_path, 'w', encoding="utf-8") as f:
            dct = {k: v.to_dict() for k, v in FileStorage.__objects.items()}
            json.dump(dct, f)

    def classes(self):
        """Returns a dictionary of valid classes and their references."""
        from models.base_model import BaseModel

        classes = {"BaseModel": BaseModel}
        return classes

    def reload(self):
        """Deserializes the JSON file to __objects
        (only if the JSON file (__file_path) exists; otherwise, do nothing.
        If the file doesn’t exist, no exception should be raised)"""

        if not os.path.isfile(FileStorage.__file_path):
            return
        with open(FileStorage.__file_path, "r", encoding="utf-8") as f:
            obj_dict = json.load(f)
            FileStorage.__objects = {k: self.classes()[v["__class__"]](
                **v)for k, v in obj_dict.items()}
