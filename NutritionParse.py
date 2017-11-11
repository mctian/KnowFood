from html.parser import HTMLParser
import pandas as pd
import requests


def retrieve_nutrition_html():
    url = 'https://diningmenu.princeton.edu/getnutrition.php?nutrition=' + str(100001).zfill(6)
    text = requests.get(url).text
    text = strip_tags(text)
    text = ''.join(text.split())
    df = pd.DataFrame(columns=['Label', 'Serving Size', 'Calories', 'Fat', 'Cholesterol', 'Sodium', 'Carbs', 'Protein'])
    df = parse_data(text)
    for i in range(100001, 100050):
        url = 'https://diningmenu.princeton.edu/getnutrition.php?nutrition=' + str(i).zfill(6)
        text = requests.get(url).text
        text = strip_tags(text)
        text = ''.join(text.split())
        if not text.startswith('NutritionLabelNutritional'):
            df = pd.merge(df, parse_data(text), how='outer')
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
            row.append('NaN')
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


