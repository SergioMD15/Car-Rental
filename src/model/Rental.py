from exceptions.ValueTooLowException import ValueTooLowException
from exceptions.InvalidDateException import InvalidDateException
import datetime as dt


class Rental:
    def __init__(self, _id, car_id, start_date, end_date, distance):
        self.set_id(_id)
        self.set_car_id(car_id)
        self.set_start_date(start_date)
        self.set_end_date(end_date)
        self.set_distance(distance)

    def set_id(self, i):
        if i > 0:
            self.id = i
        else:
            raise ValueTooLowException('Rental', 'Id', 0)

    def set_car_id(self, i):
        if i > 0:
            self.car_id = i
        else:
            raise ValueTooLowException('Rental', 'Car id', 0)

    def set_distance(self, d):
        if d > 0:
            self.distance = d
        else:
            raise ValueTooLowException('Rental', 'Distance', 0)

    def set_start_date(self, date):
        if self.is_date_valid(date):
            self.start_date = self.parse_date(date)
        else:
            raise InvalidDateException(date, 'start')

    def set_end_date(self, date):
        if self.is_end_date_valid(date):
            self.end_date = self.parse_date(date)
        else:
            raise InvalidDateException(date, 'end')

    def parse_date(self, date_str):
        """Returns the datetime representation from the given date in string."""

        spl_date = date_str.split('-')
        return dt.datetime(int(spl_date[0]), int(spl_date[1]), int(spl_date[2]))

    def is_end_date_valid(self, date):
        """Checks if the end date is valid or not.

        For the end date to be valid it needs, at first, to be a well-formed
        date itself, and then it needs to be "greater" than the start date.
        """

        if self.is_date_valid(date):
            end = self.parse_date(date)
            return end >= self.start_date

    def is_date_valid(self, date: str) -> bool:
        """Checks using datetime library if some date is well-formed or not.
        
        For a date to be well-formed it needs to have the needed format in our
        system (YYYY-MM-DD) and the values within each field (year, month, day)
        must be consistent.
        """

        try:
            dt.datetime.strptime(date, "%Y-%m-%d").strftime('%Y-%m-%d')
            return True
        except ValueError:
            return False

    def get_days_rented(self) -> int:
        return (self.end_date - self.start_date).days + 1
