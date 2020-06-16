class ExtrasController:

    def __init__(self):
        self.init_extras()

    def init_extras(self):
        """Initialization of the extras' associated prices."""

        self.owner_extras = {
            1: 500,
            2: 200
        }
        self.drivy_extras = {
            3: 1000
        }

    def compute_extras(self, rental, extras_collection) -> int:
        """Compute the price of the extras for a given rental.
        
        We take the sum of the extras' prices that are included in a given
        rental. These prices are taken from the corresponding collection of
        extras if they either belong to those that credit the owner, or drivy
        instead.
        """
        return sum([
            extras_collection[extra.id]
            for extra in rental.extras.values()
            if extra.id in extras_collection
        ])
        
    def compute_drivy_extras(self, rental):
        return self.compute_extras(rental,
                                   self.drivy_extras) * rental.get_days_rented()

    def compute_owner_extras(self, rental):
        return self.compute_extras(rental,
                                   self.owner_extras) * rental.get_days_rented()


    def compute_all_extras_price(self, rental):
        return (self.compute_drivy_extras(rental) +
                self.compute_owner_extras(rental))
