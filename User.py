import pandas as pd
import csv


class User:
    def __init__(self, index, file):
        with open(file, 'rb') as csvfile:
            info = csv.reader(csvfile)
        self.name = info.iloc[index]['Name']
        self.sex = info.iloc[index]['Sex']
        self.age = info.iloc[index]['Age']
        self.height = info.iloc[index]['Height']
        self.weight = info.iloc[index]['Weight']
        self.vegetarian = info.iloc[index]['Vegetarian']
        self.vegan = info.iloc[index]['Vegan']
        self.canEatPork = info.iloc[index]['Pork']
        self.diningHall = 'Roma'

    def returnName(self):
        return self.name

    def returnSex(self):
        return self.sex

    def returnAge(self):
        return self.age

    def returnHeight(self):
        return self.height

    def returnWeight(self):
        return self.weight

    def returnRestrictions(self):
        return [self.vegetarian, self.vegan, self.canEatPork]

    def returnDiningHall(self):
        return self.diningHall

    def changeDiningHall(self, dh):
        self.diningHall = dh