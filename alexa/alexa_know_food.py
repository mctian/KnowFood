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

#@ask.intent("CreateNewUser", convert={'height': int, 'weight': int, 'age': int, 'activity': int})
#def setCalories(height, weight, age, activity, gender):
#    global calories

height = 160
weight = 80
gender = "Male"
age = 18
activity = 3
dietRestriction = "None"

if gender is "Male":
    calories = (int)(((10 * weight + 6.25 * height - 5 * age + 5) * 1.2 + 300 * activity) / 3)
else:
    calories = (int)(((10 * weight + 6.25 * height - 5 * age - 161) * 1.2 + 300 * activity) / 3)

tFat = 70 * calories / 2000
tCholesterol = 290 * calories / 2000
tSodium = 2350 * calories / 2000
tCarbs = 320 * calories / 2000
tProtein = 0.8 * weight / 3
tMatrix = np.array([tFat, tCholesterol, tSodium, tCarbs, tProtein])

def clarify(loc):
    CJL = ["see jay L", "see jay l", "see jay el", "cjl", "the center for Jewish life", "center for Jewish life"]
    wilcox = ["butler wilson", "will"]
    whitman = ["whitman"]
    forbes = ["forbes", "Forbes dining hall"]
    roma = ["rockymattie dining hall", "rockymattie", "rocky Maddy", "rockymatty"]
    for i in range(0,len(CJL)):
        if loc == CJL[i]:
            return 'CJL'

    for i in range(0,len(wilcox)):
        if loc == CJL[i]:
            return 'Wilcox'

    for i in range(0,len(whitman)):
        if loc == whitman[i]:
            return 'Whitman'

    for i in range(0,len(forbes)):
        if loc == forbes[i]:
            return 'Forbes'

    for i in range(0,len(roma)):
        if loc == roma[i]:
            return 'Roma'
    return loc

# Optional
@app.route('/')
def homepage():
    return "this is working"

@ask.launch
def start_skill():
    start_message = 'welcome to know food. would you like to know what to eat today?'
    return question(start_message)

@ask.intent("RequestMealPlan")
def suggested_meal(location, meal):
    #data = pd.read_csv("/Users/nicolelin/Documents/GitHub/KnowFood/" + str(location) + str(meal) + ".csv", encoding = 'latin-1')
    #if (location is None):
    #    reprompt_location = "i didn't catch where you wanted to eat. where would you like to go?"
    #    return question(reprompt_location)

    #if (meal is None):
    #    reprompt_meal = "i can show you options for lunch or dinner. what meal would you like to eat?"
    #    return question(reprompt_meal)
    #loc = clarify(location)

    data = pd.read_csv("/Users/nicolelin/Documents/GitHub/KnowFood/out.csv", encoding='latin-1')
    filt = pd.read_csv("/Users/nicolelin/Documents/GitHub/KnowFood/" + clarify(location) + meal + ".csv", encoding='latin-1')
    #filt = pd.read_csv("/Users/nicolelin/Documents/GitHub/KnowFood/" + str(location) + str(meal) + ".csv", encoding='latin-1')
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

    filler1 = str(amount1) + " " + str(unit1) + " of " + str(label1)
    filler2 = str(amount2) + " " + str(unit2) + " of " + str(label2)
    filler3 = str(amount3) + " " + str(unit3) + " of " + str(label3)
    filler4 = str(amount4) + " " + str(unit4) + " of " + str(label4)

    suggestion_message = f'to meet your daily nutritional needs, you should eat {filler1}, {filler2}, {filler3}, and {filler4} for {meal} at {location}'
    return question(suggestion_message)

@ask.intent("YesIntent")
#suggested_meal(location, meal)

@ask.intent("NoIntent")
def no_intent():
  no_message = "okay bye"
  return statement(no_message)

@ask.intent("AMAZON.StopIntent")
def stop_intent():
  stop_message = "goodbye and enjoy your meals!"
  return statement(stop_message)

@ask.intent("AMAZON.HelpIntent")
def help_intent():
  help_message = "ask me for princeton dining hall meal suggestions."
  return statement(help_message)

@ask.intent("AMAZON.CancelIntent")
def cancel_intent():
  cancel_message = "cancelling my report."
  return statement(cancel_message)

@ask.intent("WigglesIntent")
def wiggles_intent():
  wiggles_message = "yummy yummy."
  return statement(wiggles_message)

@ask.intent("WhoopsIntent")
def whoops_intent():
    whoops_message = "fruit salad."
    return statement(whoops_message)

if __name__ == '__main__':
    app.run(debug=True)
