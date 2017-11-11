from html.parser import HTMLParser
import pandas as pd
import requests
import math


def retrieve_nutrition_html():
    url = 'https://diningmenu.princeton.edu/getnutrition.php?nutrition=' + str(100001).zfill(6)
    text = requests.get(url).text
    text = strip_tags(text)
    text = ''.join(text.split())
    df = parse_data(text)
    i = 100001
    while i in range(100001, 1000000):
        print(i)
        url = 'https://diningmenu.princeton.edu/getnutrition.php?nutrition=' + str(i).zfill(6)
        text = requests.get(url).text
        text = strip_tags(text)
        text = ''.join(text.split())
        if not text.startswith('NutritionLabelNutritional'):
            df2 = parse_data(text)
            if not df2.at[len(df2)-1, 'Serving Size'] == '---':
                df = pd.merge(df, df2, how='outer')
                i += 1
            else:
                if i % 1000 == 0:
                    i += 1
                else:
                    i = int(math.ceil(i / 1000.0)) * 1000
        elif i % 1000 == 0:
            i += 1
        else:
            i = int(math.ceil(i / 1000.0)) * 1000
    df.to_csv('out.csv', sep=',')
    print(df)


def parse_data(text):
    start_list = ['Label', 'Size', 'Calories', 'TotalFat', 'Cholesterol', 'Sodium', 'Carb.', 'Protein']
    end_list = ['NutritionFactsServing', 'Amount', 'Calories', 'g', 'mg', 'mg', 'g', 'g']
    row = []
    df = pd.DataFrame(columns=['Label', 'Serving Size', 'Calories', 'Fat', 'Cholesterol', 'Sodium', 'Carbs', 'Protein'])
    for i in range(0,8):
        try:
            row.append((text.split(start_list[i]))[1].split(end_list[i])[0])
        except IndexError:
            row.append('')
    df.loc[0] = row
    return df


class NutritionParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.reset()
        self.fed = []

    def handle_data(self, d):
            self.fed.append(d)

    def get_data(self):
            return ''.join(self.fed)


def strip_tags(html):
    s = NutritionParser()
    s.feed(html)
    return s.get_data()


retrieve_nutrition_html()

