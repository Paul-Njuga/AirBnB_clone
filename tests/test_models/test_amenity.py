#!/usr/bin/python3
"""
Unittests for amenity model
Classes:
    instatiation
    save
    to_dict
"""

import unittest
from models.amenity import Amenity
from datetime import datetime

class TestAmenity_instatiation(unittest.TestCase):
    """
    Unittest testing for the amenity instatiation
    """

    def test_no_args_instastiates(self):
        self.assertEqual(Amenity, type(Amenity()))
