class InvalidTypeException(Exception):
    
    def __init__(self, value, valid_types):
        self.message = f'Current payment type ({value}) is not a valid type {valid_types}'
        super().__init__(self.message)
