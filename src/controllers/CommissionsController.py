from model.Rental import Rental


class CommissionsController:
    """Controller to handle the commissions distribution."""

    def __init__(self, rentals_prices):
        self.rental_prices = rentals_prices

    def compute_payments(self, rental):
        """Each actor along with the corresponding commission amount."""
        return {
            'insurance_fee': int(self.compute_insurance(rental)),
            'assistance_fee': int(self.compute_assistance(rental)),
            'drivy_fee': int(self.compute_drivy(rental))
        }

    def compute_insurance(self, rental):
        """The insurance credits half of the remaining 30%."""
        return (self.rental_prices[rental.id] * 0.3) // 2

    def compute_assistance(self, rental):
        """The assistance credits 1€ per day of rental."""
        return rental.get_days_rented() * 100

    def compute_drivy(self, rental):
        """What remains from the original 30% (after the commissions of
        insurance and assistance) belongs to drivy.
        """
        return max(self.compute_insurance(rental) - self.compute_assistance(rental), 0)
