class InvalidDateException(Exception):
    
    def __init__(self, value, type):
        self.message = f'Current {type} date {value} is not valid'
        super().__init__(self.message)
