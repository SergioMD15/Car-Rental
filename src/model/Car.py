from exceptions.ValueTooLowException import ValueTooLowException


class Car:
    def __init__(self, id, price_per_day, price_per_km):
        self.set_id(id)
        self.set_price_per_day(price_per_day)
        self.set_price_per_km(price_per_km)

    def set_id(self, i):
        if i > 0:
            self.id = i
        else:
            raise ValueTooLowException('Car', 'Id', 0)

    def set_price_per_day(self, p):
        if p > 0:
            self.price_per_day = p
        else:
            raise ValueTooLowException('Car', 'Price per day', 0)

    def set_price_per_km(self, p):
        if p > 0:
            self.price_per_km = p
        else:
            raise ValueTooLowException('Car', 'Price per kilometer', 0)
