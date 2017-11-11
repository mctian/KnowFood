from flask import Flask, render_template
from flask_ask import Ask, statement, question, session

app = Flask(__name__)
ask = Ask(app, "/")

# Optional
@app.route('/')
def homepage():
    return "this is working"

@ask.launch
def start_skill():
    start_message = "welcome to know food. would you like to know what to eat today?"
    return question("would you like to know what to eat today?")

@ask.intent("RequestMealPlan")
def

@ask.intent("YesIntent")


@ask.intent("NoIntent")
def no_intent():
  no_message = "okay bye"
  return statement(no_message)



if __name__ == '__main__':
    app.run(debug=True)
