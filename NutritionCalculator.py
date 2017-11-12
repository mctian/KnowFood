import numpy as np
import pandas as pd
from scipy.spatial import distance
from itertools import combinations
import re

h = 160
w = 80
g = "Male"
age = 18
activity = 3
dietRestriction = "None"

if g is "Male":
    calories = (int)(((10 * w + 6.25 * h - 5 * age + 5) * 1.2 + 300 * activity) / 3)
else:
    calories = (int)(((10 * w + 6.25 * h - 5 * age - 161) * 1.2 + 300 * activity) / 3)

tFat = 70 * calories / 2000
tCholesterol = 290 * calories / 2000
tSodium = 2350 * calories / 2000
tCarbs = 320 * calories / 2000
tProtein = 0.8 * w / 3
tMatrix = np.array([tFat, tCholesterol, tSodium, tCarbs, tProtein])

data = pd.read_csv("/Users/harry/Downloads/out.csv", encoding='latin-1')
filt = pd.read_csv("/Users/harry/Downloads/KnowFood-master/WilcoxLunch.csv", encoding='latin-1')
# dietaryFilter
try:
    other = data[data['Label'].isin(filt['Other'])]
except ValueError:
    other = pd.DataFrame({'Other': []})
try:
    vegetarian = data[data['Label'].isin(filt['Vegetarian'])]
except ValueError:
    vegetarian = pd.DataFrame({'Vegetarian': []})
try:
    vegan = data[data['Label'].isin(filt['Vegan'])]
except ValueError:
    vegan = pd.DataFrame({'Vegan': []})
try:
    pork = data[data['Label'].isin(filt['Pork'])]
except ValueError:
    pork = pd.DataFrame({'Pork': []})

if dietRestriction is "None":
    selection = pd.concat([vegetarian, vegan, pork, other], axis=0)
elif dietRestriction is "Vegan":
    selection = vegan
elif dietRestriction is "Vegetarian":
    selection = pd.concat([vegetarian, vegan], axis=0)
else:
    selection = pd.concat([vegetarian, vegan, other], axis=0)

selection = selection.drop_duplicates(subset='Label', keep='first')

rows = np.arange(selection.shape[0])
cases = np.array([10000000, 10000000, 10000000, 10000000])

for p in combinations(rows, 4):
    cases = np.array([10000000,10000000,10000000,10000000])
    row_0 = selection.iloc[p[0]]
    calories_0 = (int)(row_0['Calories'])
    row_1 = selection.iloc[p[1]]
    calories_1 = (int)(row_1['Calories'])
    row_2 = selection.iloc[p[2]]
    calories_2 = (int)(row_2['Calories'])
    row_3 = selection.iloc[p[3]]
    calories_3 = (int)(row_3['Calories'])

    for i in range(20):
        cases = np.vstack((cases, [np.random.randint(15, 35)/100*calories/calories_0,
                                   np.random.randint(15, 35)/100*calories/calories_1,
                                   np.random.randint(15, 35)/100*calories/calories_2,
                                   np.random.randint(15, 35)/100*calories/calories_3]))

    minimum = float('inf')
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

    for i in range(21):
        oMatrix = np.array([oFat_0*cases[i, 0]+oFat_1*cases[i, 1]+oFat_2*cases[i, 2]+oFat_3*cases[i, 3],
                            oCholesterol_0*cases[i, 0]+oCholesterol_1*cases[i, 1]+oCholesterol_2*cases[i, 2]+oCholesterol_3*cases[i, 3],
                            oSodium_0*cases[i, 0]+oSodium_1*cases[i, 1]+oSodium_2*cases[i, 2]+oSodium_3*cases[i, 3],
                            oCarbs_0*cases[i, 0]+oCarbs_1*cases[i, 1]+oCarbs_2*cases[i, 2]+oCarbs_3*cases[i, 3],
                            oProtein_0*cases[i, 0]+oProtein_1*cases[i, 1]+oProtein_2*cases[i, 2]+oProtein_3*cases[i, 3]])
        if distance.euclidean(tMatrix, oMatrix) < minimum:
            minimum = distance.euclidean(tMatrix, oMatrix)
            ideal = cases[i]
            idealFoods = p
food1 = selection.iloc[idealFoods[0]]
food2 = selection.iloc[idealFoods[1]]
food3 = selection.iloc[idealFoods[2]]
food4 = selection.iloc[idealFoods[3]]

label1 = food1['Label']
label2 = food2['Label']
label3 = food3['Label']
label4 = food4['Label']

amount1 = np.round((float)(re.findall(r'[\d\.\d]+', food1['Serving Size'])[0])*ideal[0])
amount2 = np.round((float)(re.findall(r'[\d\.\d]+', food2['Serving Size'])[0])*ideal[1])
amount3 = np.round((float)(re.findall(r'[\d\.\d]+', food3['Serving Size'])[0])*ideal[2])
amount4 = np.round((float)(re.findall(r'[\d\.\d]+', food4['Serving Size'])[0])*ideal[3])

unit1 = food1['Serving Size'].lstrip('0123456789.- ')
unit2 = food2['Serving Size'].lstrip('0123456789.- ')
unit3 = food3['Serving Size'].lstrip('0123456789.- ')
unit4 = food4['Serving Size'].lstrip('0123456789.- ')