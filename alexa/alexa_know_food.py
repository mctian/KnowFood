from flask import Flask, render_template
from flask_ask import Ask, statement, question, session, convert_errors
#import NutritionCalculator
import numpy as np
import pandas as pd
from scipy.spatial import distance
from itertools import combinations
import re


app = Flask(__name__)
ask = Ask(app, "/")

@ask.intent("CreateNewUser", convert={'height': int, 'weight': int, 'age': int, 'activity': int})
def setCalories(height, weight, age, activity, gender):
    global calories

    if gender is "Male":
        calories = (10*weight+6.25*height-5*age+5)*1.2+300*activity
    else:
        calories = (10*weight+6.25*height-5*age-161)*1.2+300*activity

    tFat = 60*calories/2000
    tCholesterol = 290*calories/2000
    tSodium = 2350*calories/2000
    tCarbs = 320*calories/2000
    tProtein = 0.8*weight
    global tMatrix
    tMatrix = np.array([tFat, tCholesterol, tSodium, tCarbs, tProtein])

    rows = np.arange(6)
    nums = np.array([0,0,0,0])
    cases = nums

    ideal = np.array([0,0,0,0])
    idealFoods = np.array([0,0,0,0])


# Optional
@app.route('/')
def homepage():
    return "this is working"

@ask.launch
def start_skill():
    start_message = 'welcome to know food. would you like to know what to eat today?'
    return question(start_message)

@ask.intent("YesIntent")
@ask.intent("RequestMealPlan")
def suggested_meal(location, meal):
    data = pd.read_csv("/Users/nicolelin/Documents/GitHub/KnowFood/" + str(location) + str(meal) + ".csv", encoding = 'latin-1')
    if (location is None):
        reprompt_location = "i didn't catch where you wanted to eat. where would you like to go?"
        return question(reprompt_location)

    if (meal is None):
        reprompt_meal = "i can show you options for lunch or dinner. what meal would you like to eat?"
        return question(reprompt_meal)

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

    label1 = food1['Label']
    label2 = food2['Label']
    label3 = food3['Label']
    label4 = food4['Label']

    amount1 = (float)(re.findall(r'[\d\.\d]+', food1['Serving Size'])[0])*ideal[0]
    amount2 = (float)(re.findall(r'[\d\.\d]+', food2['Serving Size'])[0])*ideal[1]
    amount3 = (float)(re.findall(r'[\d\.\d]+', food3['Serving Size'])[0])*ideal[2]
    amount4 = (float)(re.findall(r'[\d\.\d]+', food4['Serving Size'])[0])*ideal[3]

    unit1 = food1['Serving Size'].lstrip('0123456789.- ')
    unit2 = food2['Serving Size'].lstrip('0123456789.- ')
    unit3 = food3['Serving Size'].lstrip('0123456789.- ')
    unit4 = food4['Serving Size'].lstrip('0123456789.- ')

    filler1 = str(amount1) + " " + str(unit1) + " of " + str(label1)
    filler2 = str(amount2) + " " + str(unit2) + " of " + str(label2)
    filler3 = str(amount3) + " " + str(unit3) + " of " + str(label3)
    filler4 = str(amount4) + " " + str(unit4) + " of " + str(label4)

    suggestion_message = f'to meet your daily nutritional needs, you should eat {filler1}, {filler2}, {filler3}, and {filler4} for {meal} at {location}'
    return question(suggestion_message)


@ask.intent("NoIntent")
def no_intent():
  no_message = "okay bye"
  return statement(no_message)

if __name__ == '__main__':
    app.run(debug=True)
