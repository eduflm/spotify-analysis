import random

from database import Database
from pandas as pd


TRAINING_PORCENTAGE = 0.7

class DataPreparation:

    def __init__(self):
        self.x_training = []
        self.y_training = []

        self.x_test = []
        self.y_test = []

        self.database = Database()

        self.prepare_data()
        self.get_training_set()


if __name__ == "__main__":
    DataPreparation()

