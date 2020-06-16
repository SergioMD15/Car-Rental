import json
import sys
from controllers.RentalController import RentalController


def main(input_file: str, output_file: str):
    rent_controller = RentalController()
    rent_controller.read_input(input_file)
    rent_controller.output_rental_recipe(output_file)

if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
