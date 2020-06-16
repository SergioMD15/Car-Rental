from exceptions.InvalidTypeException import InvalidTypeException
from exceptions.ValueTooLowException import ValueTooLowException


class Payment:

    def __init__(self, amount, payment_type):
        self.valid_payments = ['debit', 'credit']
        self.set_amount(amount)
        self.set_payment(payment_type)

    def set_payment(self, p_type):
        if p_type not in self.valid_payments:
            raise InvalidTypeException(p_type, self.valid_payments)
        else:
            self.payment_type = p_type

    def set_amount(self, amount):
        if amount < 0:
            raise ValueTooLowException('Payment', 'amount', '0')
        else:
            self.amount = int(amount)
