from collections import defaultdict
import os
import sys
import json

from model.Car import Car
from model.Rental import Rental
from model.Extra import Extra
from exceptions.WrongInputException import WrongInputException

EXTRAS_PARAMS = CARS_PARAMS = 3
RENTALS_PARAMS = 5


class IOController:

    def __init__(self):
        self.cars = {}
        self.rentals = {}

    def read_file(self, filename: str):
        if not os.path.exists(filename):
            raise FileNotFoundError()
        with open(filename, 'rb') as json_file:
            data = json.load(json_file)
            if not all(k in data for k in ('cars', 'rentals')):
                raise WrongInputException(
                    'There are missing fields in the input file')
            self.parse_cars(data['cars'])
            self.parse_rentals(data['rentals'])
            if 'options' in data:
                self.parse_extras(data['options'])
            return [self.cars, self.rentals.values()]

    def parse_cars(self, data):
        """Parses the raw data for cars and adds them to the collection"""
        for raw_car in data:
            if self.check_car(raw_car):
                self.cars[raw_car['id']] = Car(raw_car['id'],
                                               raw_car['price_per_day'],
                                               raw_car['price_per_km'])
            else:
                raise WrongInputException('Format not valid for cars input')

    def parse_rentals(self, data):
        for raw_rental in data:
            if self.check_rental(raw_rental):
                self.rentals[raw_rental['id']] = Rental(raw_rental['id'],
                                                        raw_rental['car_id'],
                                                        raw_rental['start_date'],
                                                        raw_rental['end_date'],
                                                        raw_rental['distance'])
            else:
                raise WrongInputException('Format not valid for rentals input')

    def parse_extras(self, data):
        extras = set()
        for raw_extra in data:
            if self.check_extra(raw_extra, extras):
                extras.add(raw_extra['id'])
                self.rentals[raw_extra['rental_id']].add_extra(
                    Extra(raw_extra['id'],
                          raw_extra['rental_id'],
                          raw_extra['type'])
                )
            else:
                raise WrongInputException('extras')

    def check_extra(self, raw_extra, extras) -> bool:
        """Checks whether the input defining an extra is valid or not.

        For the extra to be valid it must have an exact number of parameters,
        its rental id must exist in rentals structure, and its id must be unique.
        """
        return len(raw_extra) == EXTRAS_PARAMS \
            and raw_extra['rental_id'] in self.rentals \
            and raw_extra['id'] not in extras

    def check_rental(self, raw_rental) -> bool:
        """Checks whether the input defining a rental is valid or not.

        For the rental to be valid it must have an exact number of parameters,
        its car id must exist in cars structure, and its id must be unique.
        """
        return len(raw_rental) == RENTALS_PARAMS \
            and raw_rental['car_id'] in self.cars \
            and raw_rental['id'] not in self.rentals

    def check_car(self, raw_car) -> bool:
        """Checks whether the input defining a car is valid or not.

        For the car to be valid it must have an exact number of parameters and
        its id must be unique.
        """
        return (len(raw_car) == CARS_PARAMS) \
            and (raw_car['id'] not in self.cars)

    def output_rental_recipe(self, data, filename: str):
        with open(filename, 'w') as outfile:
            try:
                json.dump(data, outfile, indent=2)
            except:
                raise IOError('An error has occurred while writing the file.')
