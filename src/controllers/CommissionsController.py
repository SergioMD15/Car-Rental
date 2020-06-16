from model.Rental import Rental
from model.Payment import Payment
from controllers.ExtrasController import ExtrasController


class CommissionsController:
    """Controller to handle the commissions distribution."""

    def __init__(self, rentals_prices):
        self.rental_prices = rentals_prices
        self.extras_handler = ExtrasController()

    def compute_payments(self, rental):
        """Each actor has an amount of debited or credited money (in € cents)."""
        return {
            'driver': Payment(self.compute_driver(rental), 'debit'),
            'owner': Payment(self.compute_owner(rental),
                             'credit'),
            'insurance': Payment(self.compute_insurance(rental), 'credit'),
            'assistance': Payment(self.compute_assistance(rental), 'credit'),
            'drivy': Payment(self.compute_drivy(rental), 'credit')
        }

    def compute_driver(self, rental):
        """The driver debits the base price of the rental + the extras."""
        return (self.rental_prices[rental.id] +
                self.extras_handler.compute_all_extras_price(rental))

    def compute_owner(self, rental):
        """The owner credits a 70% of the rental base price + the extras."""
        return (self.rental_prices[rental.id] * 0.7 +
                self.extras_handler.compute_owner_extras(rental))

    def compute_insurance(self, rental):
        """The insurance credits half of the remaining 30%."""
        return (self.rental_prices[rental.id] * 0.3) // 2

    def compute_assistance(self, rental):
        """The assistance credits 1€ per day of rental."""
        return rental.get_days_rented() * 100

    def compute_drivy(self, rental):
        """What remains from the original 30% (after crediting insurance and
        assitance) is credited to drivy.
        """
        base = self.compute_insurance(rental) - self.compute_assistance(rental)
        return base + self.extras_handler.compute_drivy_extras(rental)
