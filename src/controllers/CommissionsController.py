from model.Rental import Rental
from model.Payment import Payment


class CommissionsController:
    """Controller to handle the commissions distribution."""

    def __init__(self, rentals_prices):
        self.rental_prices = rentals_prices

    def compute_payments(self, rental):
        """Each actor has an amount of debited or credited money (in € cents)."""
        return {
            'driver': Payment(int(self.compute_driver(rental)), 'debit'),
            'owner': Payment(int(self.compute_owner(rental)),
                             'credit'),
            'insurance': Payment(int(self.compute_insurance(rental)), 'credit'),
            'assistance': Payment(int(self.compute_assistance(rental)), 'credit'),
            'drivy': Payment(int(self.compute_drivy(rental)), 'credit')
        }

    def compute_driver(self, rental):
        """The driver debits the base price of the rental."""
        return self.rental_prices[rental.id]

    def compute_owner(self, rental):
        """The owner credits a 70% of the rental base price."""
        return self.rental_prices[rental.id] * 0.7

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
        return self.compute_insurance(rental) - self.compute_assistance(rental)
