import datetime
import requests
import pandas as pd
import json
import re

def retrieve_menus():
    today = datetime.datetime.now()
    today_formatted = str(today.month) + '/' + str(today.day) + '/' + str(today.year)
    url = 'https://tigermenus.herokuapp.com/api/' + today_formatted
    text = requests.get(url).json()
    data = json.dumps(text)
    data = data.replace(" ", "")
    data = data.replace('"legend"', "")
    data = data.replace('"item"', "")
    data = data.replace('"label"', "")
    print(data)
    dinIndex = []
    lunIndex = []
    matches = re.findall(r'"([A-Za-z0-9_&\'\./\\]*)"', data)
    for i in range(1, len(matches)):
        if matches[i] == 'Dinner':
            dinIndex.append(i)
        elif matches[i] == 'Lunch':
            lunIndex.append(i)

    output_csv_menu(matches, dinIndex[0], dinIndex[1], 'WilcoxDinner')
    output_csv_menu(matches, dinIndex[1], dinIndex[2], 'CJLDinner')
    output_csv_menu(matches, dinIndex[2], dinIndex[3], 'WhitmanDinner')
    output_csv_menu(matches, dinIndex[3], dinIndex[4], 'RomaDinner')
    output_csv_menu(matches, dinIndex[4], lunIndex[0], 'ForbesDinner')
    output_csv_menu(matches, lunIndex[0], lunIndex[1], 'WilcoxLunch')
    output_csv_menu(matches, lunIndex[1], lunIndex[2], 'CJLLunch')
    output_csv_menu(matches, lunIndex[2], lunIndex[3], 'WhitmanLunch')
    output_csv_menu(matches, lunIndex[3], lunIndex[4], 'RomaLunch')
    output_csv_menu(matches, lunIndex[4], len(matches), 'ForbesLunch')


def output_csv_menu(list, start, end, name):
    other = []
    vegan = []
    vegetarian = []
    pork = []
    for i in range(start,end):
        if list[i] == 'vegetarian':
            vegetarian.append(list[i-1])
        elif list[i] == 'vegan':
            vegan.append(list[i-1])
        elif list[i] == 'pork':
            pork.append(list[i-1])
        elif list[i] == '':
            other.append(list[i-1])
    df1 = pd.DataFrame({'Other': other})
    df2 = pd.DataFrame({'Vegan': vegan})
    df3 = pd.DataFrame({'Vegetarian': vegetarian})
    df4 = pd.DataFrame({'Pork': pork})
    df = pd.concat([df1, df2, df3, df4], axis=1)
    df.to_csv(name + '.csv', sep=',')
    return df

retrieve_menus()
