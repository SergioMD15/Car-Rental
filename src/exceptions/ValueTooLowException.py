class ValueTooLowException(Exception):
    
    def __init__(self, class_name, value, bound):
        self.message = f'Value {value} in {class_name} cannot be below {bound}'
        super().__init__(self.message)
