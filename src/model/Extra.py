from exceptions.ValueTooLowException import ValueTooLowException


class Extra:
    def __init__(self, id, rental_id, extra_type):
        self.set_id(id)
        self.set_rental_id(rental_id)
        self.name = extra_type

    def set_id(self, i):
        if i > 0:
            self.id = i
        else:
            raise ValueTooLowException('Extra', 'Id', 0)

    def set_rental_id(self, i):
        if i > 0:
            self.rental_id = i
        else:
            raise ValueTooLowException('Extra', 'Rental id', 0)
