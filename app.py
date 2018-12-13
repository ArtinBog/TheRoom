from flask import Flask, render_template, url_for, request, jsonify, g, flash
import random
from . import GSintegration as gs

app = Flask(__name__)
# app.static_folder = 'static'

results = []
all_quetions = gs.q_n_bg(gs.values)

def choose_color_question():

    lst = []
    for i in all_quetions:
        lst.append(i)
    random_color = random.choice(lst)

    random_question = [random_color]
    while len(random_question) < 2:
        choosen_question = random.choice(all_quetions[random_color])
        if len(choosen_question) > 1:
            random_question.append(choosen_question)

    return random_question


@app.route("/")
def index():

    result = choose_color_question()

    ## NEED TO THINK HOW TO USE gs.values TO AVOID REPETITION

    while result[1] in results:
        result = choose_color_question()
    #     if len(results) == len((result-1)/2):
    #         for i in (len(results) * 0.5):
    #             results.remove(0)

    results.append(result[1])
    color = result[0]
    question = result[1]
    font_color = 'white'

    print("Length of all questions: ", gs.values)
    print("Current question: ", result)
    print("All previous question: ", results)

    if color == 'black':
        return render_template('index.html', question=question, color=color, font_color=font_color)
    else:
        return render_template('index.html', question=question, color=color)


@app.route("/About")
def about():
    return render_template('About.html')

print('Done')


if __name__ == "__main__":
    app.run(debug=true)