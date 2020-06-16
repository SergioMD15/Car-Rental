from model.Car import Car
from model.Rental import Rental
from controllers.IOController import IOController
from controllers.CommissionsController import CommissionsController


class RentalController:

    def __init__(self):
        self.init_discounts()
        self.io = IOController()

    def init_discounts(self):
        self.discounts = {
            10: 0.5,
            4: 0.7,
            1: 0.9
        }

    def read_input(self, filename: str):
        result = self.io.read_file(filename)
        self.cars = result[0]
        self.rentals = result[1]
        self.c_handler = CommissionsController(
            {
                rental.id: int(self.compute_rental_price(rental))
                for rental in self.rentals
            })

    def compute_rental_price(self, rental) -> int:
        car = self.cars[rental.car_id]
        return (self.compute_km_price(car, rental) +
                self.compute_daily_price(car, rental.get_days_rented()))

    def compute_daily_price(self, car, rented_days) -> int:
        """Computes the total discounted daily price for a given rental.
        
        If the rental fulfills some temporal conditions, it receives a discount
        for some period of time (these periods and its associated discounts are
        stored in a class variable).
        """
        total_price = car.price_per_day
        for days, discount in self.discounts.items():
            if rented_days > days:
                discount_days = rented_days - days
                total_price += car.price_per_day * discount * (discount_days)
                rented_days -= discount_days
        return total_price

    def compute_km_price(self, car, rental) -> int:
        return car.price_per_km * rental.distance

    def get_actions(self, rental):
        """Returns the set of actions associated to some rental.
        
        An action defines the relation of an actor with an amount of money, i.e.
        if that actor owes money (debit) or instead, it is owed money (credit).
        """
        return [
            {
                'who': owner,
                'type': payment.payment_type,
                'amount': payment.amount
            }
            for owner, payment in self.c_handler.compute_payments(rental).items()
        ]

    def output_rental_recipe(self, filename: str):
        """Creates the structure of the recipe for the IOController
        
        After computing all the prices for the different rentals, we generate
        a receipt with a breakdown of the actions for each rental.
        Each rental is identified with its id and a detailed breakdown of the
        amount credited or debited to each actor.
        """
        self.io.output_rental_recipe(
            {'rentals':
                [
                    {
                        'id': rental.id,
                        'actions': self.get_actions(rental)
                    }
                    for rental in self.rentals
                ]
             }, filename)
