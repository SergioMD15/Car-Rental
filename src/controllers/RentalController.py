from model.Car import Car
from model.Rental import Rental
from controllers.IOController import IOController

class RentalController:

    def __init__(self):
        self.io = IOController()

    def read_input(self, filename: str):
        result = self.io.read_file(filename)
        self.cars = result[0]
        self.rentals = result[1]

    def compute_rental_price(self, rental) -> int:
        car = self.cars[rental.car_id]
        return (self.compute_km_price(car, rental) +
                self.compute_daily_price(car, rental.get_days_rented()))

    def compute_daily_price(self, car, rented_days) -> int:
        """Computes the total daily price for a given rental."""
        return car.price_per_day * rented_days

    def compute_km_price(self, car, rental) -> int:
        return car.price_per_km * rental.distance

    def output_rental_recipe(self, filename: str):
        """
        
        Creates the structure of the recipe for the IOController.
        Each rental is identified with its id and its price.
        
        """
        self.io.output_rental_recipe(
            {'rentals':
                [
                    {
                        'id': rental.id,
                        'price': self.compute_rental_price(rental)
                    }
                    for rental in self.rentals
                ]
             }, filename)
