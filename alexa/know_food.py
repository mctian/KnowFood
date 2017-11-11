from flask import Flask, render_template
from flask_ask import Ask, statement, question, session
import nutritionCalculator

app = Flask(__name__)
ask = Ask(app, "/")

# Optional
@app.route('/')
def homepage():
    return "this is working"

@ask.launch
def start_skill():
    start_message = render_template('welcome')
    return question(start_message)

@ask.intent("RequestMealPlan", convert = {'location':string, 'meal':string})
def suggested_meal():
    filler1 = nutritionCalculator.amount1 + " " + nutritionCalculator.unit1 + " of " + nutritionCalculator.food1
    filler2 = nutritionCalculator.amount2 + " " + nutritionCalculator.unit2 + " of " + nutritionCalculator.food2
    filler3 = nutritionCalculator.amount3 + " " + nutritionCalculator.unit3 + " of " + nutritionCalculator.food3
    filler4 = nutritionCalculator.amount4 + " " + nutritionCalculator.unit4 + " of " + nutritionCalculator.food4

    suggestion_message = f'to meet your daily nutritional needs, you should eat {filler1}, {filler2}, {filler3}, and {filler4} at ' + location + ' for ' + meal
    return question(suggestion_message)

@ask.intent("YesIntent")


@ask.intent("NoIntent")
def no_intent():
  no_message = "okay bye"
  return statement(no_message)



if __name__ == '__main__':
    app.run(debug=True)
