import numpy as np
import pandas as pd
from scipy.spatial import distance
from itertools import combinations
import re

data = pd.read_csv("/Users/masontian/Documents/GitHub/KnowFood/out.csv", encoding = 'latin-1')
h = 160
w = 80
g = "Male"
age = 18
activity = 3

if g is "Male":
    calories = (10*w+6.25*h-5*age+5)*1.2+300*activity
else:
    calories = (10*w+6.25*h-5*age-161)*1.2+300*activity

tFat = 60*calories/2000
tCholesterol = 290*calories/2000
tSodium = 2350*calories/2000
tCarbs = 320*calories/2000
tProtein = 0.8*w
tMatrix = np.array([tFat, tCholesterol, tSodium, tCarbs, tProtein])

rows = np.arange(6)
nums = np.array([0,0,0,0])
cases = nums

ideal = np.array([0,0,0,0])
idealFoods = np.array([0,0,0,0])


for p in combinations(rows, 4):
    minimum = float('inf')
    row_0 = data.iloc[p[0]]
    calories_0 = (int)(row_0['Calories'])
    row_1 = data.iloc[p[1]]
    calories_1 = (int)(row_1['Calories'])
    row_2 = data.iloc[p[2]]
    calories_2 = (int)(row_2['Calories'])
    row_3 = data.iloc[p[3]]
    calories_3 = (int)(row_3['Calories'])
    while nums[0]*calories_0 < calories:
        nums[0] = nums[0]+1
        while nums[0]*calories_0 + nums[1]*calories_1 < calories:
            nums[1] = nums[1]+1
            while nums[0]*calories_0 + nums[1]*calories_1 + nums[2]*calories_2< calories:
                nums[2] = nums[2]+1
                while nums[0]*calories_0 + nums[1]*calories_1 + nums[2]*calories_2 + nums[3]*calories_3 < calories:
                    nums[3] = nums[3]+1
                cases = np.vstack((cases, nums))
                nums[3] = 0
            cases = np.vstack((cases, nums))
            nums[2] = 0
        cases = np.vstack((cases, nums))
        nums[1] = 0
    cases = np.vstack((cases, nums))
    nums[0] = 0
    oFat_0 = (float)(row_0['Fat'])
    oFat_1 = (float)(row_1['Fat'])
    oFat_2 = (float)(row_2['Fat'])
    oFat_3 = (float)(row_3['Fat'])
    oCholesterol_0 = (float)(row_0['Cholesterol'])
    oCholesterol_1 = (float)(row_1['Cholesterol'])
    oCholesterol_2 = (float)(row_2['Cholesterol'])
    oCholesterol_3 = (float)(row_3['Cholesterol'])
    oSodium_0 = (float)(row_0['Sodium'])
    oSodium_1 = (float)(row_1['Sodium'])
    oSodium_2 = (float)(row_2['Sodium'])
    oSodium_3 = (float)(row_3['Sodium'])
    oCarbs_0 = (float)(row_0['Carbs'])
    oCarbs_1 = (float)(row_1['Carbs'])
    oCarbs_2 = (float)(row_2['Carbs'])
    oCarbs_3 = (float)(row_3['Carbs'])
    oProtein_0 = (float)(row_0['Protein'])
    oProtein_1 = (float)(row_1['Protein'])
    oProtein_2 = (float)(row_2['Protein'])
    oProtein_3 = (float)(row_3['Protein'])
    for i in range(0, cases.shape[0]-1):
        oMatrix = np.array([oFat_0*cases[i, 0]+oFat_1*cases[i, 1]+oFat_2*cases[i, 2]+oFat_3*cases[i, 3],
                           oCholesterol_0*cases[i, 0]+oCholesterol_1*cases[i, 1]+oCholesterol_2*cases[i, 2]+oCholesterol_3*cases[i, 3],
                           oSodium_0*cases[i, 0]+oSodium_1*cases[i, 1]+oSodium_2*cases[i, 2]+oSodium_3*cases[i, 3],
                           oCarbs_0*cases[i, 0]+oCarbs_1*cases[i, 1]+oCarbs_2*cases[i, 2]+oCarbs_3*cases[i, 3],
                           oProtein_0*cases[i, 0]+oProtein_1*cases[i, 1]+oProtein_2*cases[i, 2]+oProtein_3*cases[i, 3]])
        if distance.euclidean(tMatrix, oMatrix) < minimum:
            minimum = distance.euclidean(tMatrix, oMatrix)
            ideal = cases[i]
            idealFoods = p

food1 = data.iloc[idealFoods[0]]
food2 = data.iloc[idealFoods[1]]
food3 = data.iloc[idealFoods[2]]
food4 = data.iloc[idealFoods[3]]
amount1 = re.findall(r'[\d\.\d]+', food1['Serving Size'])
amount2 = re.findall(r'[\d\.\d]+', food2['Serving Size'])
amount3 = re.findall(r'[\d\.\d]+', food3['Serving Size'])
amount4 = re.findall(r'[\d\.\d]+', food4['Serving Size'])