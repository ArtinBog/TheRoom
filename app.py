from flask import Flask, render_template, url_for, redirect, request
import random
from .pkgs import GSintegration as gs
from flask_sqlalchemy import SQLAlchemy
import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres@localhost/the_room"
app.debug = True
db = SQLAlchemy(app)

# all_questions contains all colors (Keys) and questions (Values)
all_questions = gs.q_n_bg(gs.values)

# create an empty dictionary which will fill out by func (clean_dict_creation)
# with colors (as keys) and question (as values)
# without '' empty questions that come from all_questions
clean_full_dict = dict()

print("TEST_________", all_questions)

historical_questions = []
historical_colors = []
historical_font_colors = []
font_family_list = []


# Create a Questions table in the database
class Questions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String, unique=True)
    color = db.Column(db.String(255))
    creator = db.Column(db.String(255))
    data_time = db.Column(db.String(255))

    def __init__(self, question, color, creator, data_time):
        self.question = question
        self.color = color
        self.creator = creator
        self.data_time = data_time

    def __repr__(self):
        return "{self.question}{self.color}{self.creator}{self.data_time}".format(self=self)

# create clean dictionary (clean_full_dict)
# with colors (as keys) and questions (as values)
# without '' empty questions that come from all_questions
def clean_dict_creation():
    for col in all_questions:
        if col not in clean_full_dict:
            clean_full_dict[col] = []
            for ques in all_questions[col]:
                if len(ques) > 1 and ques not in clean_full_dict[col]:
                    clean_full_dict[col].append(ques)

    return clean_full_dict

# NEED TO WORK ON IT
def migrate_data():
    data = clean_dict_creation()
    # all_rows = []
    for color in data:
        # row = []
        for question in data[color]:
            time = datetime.datetime.today()
            # row.append(time)
            # all_rows.append([question, color, "admin", time])
            # Questions(all_rows[0], all_rows[1], all_rows[2], all_rows[3])
            question_row = Questions(question, color, "admin", time)
            db.session.add(question_row)
            db.session.commit()

            # all_rows.append(row)




def available_questions(lst_of_questions, historical_questions):
    available_questions_lst = []
    numbr = int(len(historical_questions) * 0.3)

    for i in lst_of_questions:
        available_questions_lst.append(i)

    if len(historical_questions) > int(0.8 * len(lst_of_questions)):
        historical_questions = historical_questions[:numbr]

    for i in historical_questions:
        if i in available_questions_lst:
            available_questions_lst.remove(i)

    return(available_questions_lst)

def choose_color_question():

    # I need to create 2 separate lists
    # where I put all colors and all questions
    # detached from each other
    # First I defined empty 'color' list: lst_of_colors
    lst_of_colors = []

    # push all colors (keys) to the new list (lst_of_colors) above
    for i in all_questions:
        lst_of_colors.append(i)

    # I need to create 2 separate lists
    # where I put all colors and all questions
    # detached from each other
    # Second I defined empty 'questions' list: lst_of_questions
    lst_of_questions = []

    # push all questions (values of all colors in dict all_questions)
    # to the new list (lst_of_questions) above
    # run i '8' times (amount of colors)
    for i in range(len(lst_of_colors)):

        # run q as many times as certain color has values in it
        for q in all_questions[lst_of_colors[i]]:

            # build up clean list of question (without colors, keys, dict)
            lst_of_questions.append(q)

    # eliminate all duplicates (empty spaces '') from the lst_of_questions
    # by converting it into a set, then print length of it
    lst_of_questions = set(lst_of_questions)

    # convert back to the list but without duplicates
    lst_of_questions = list(lst_of_questions)

    # print length of my new list
    print("Total amount of questions is ", len(lst_of_questions))



    # create new var 'lst_of_available_questions' by calling function available_questions
    # with 2 parameters 'lst_of_questions' and 'historical_questions'
    # the fuct deducts 'historical_questions' from all question (lst_of_questions)
    lst_of_available_questions = available_questions(lst_of_questions, historical_questions)

    print("Total amount of ALL questions (lst_of_questions) is", len(lst_of_questions))
    print("Total amount of AVAILABLE questions (lst_of_available_questions) is ", len(lst_of_available_questions))

    # choose random color (item) from lst (list)
    random_color = random.choice(lst_of_colors)

    # it's a list with a 2 potential items
    # color (random_color) and question (chosen_question)
    # now it has only 1, but after while loop it gets appended chosen_question
    random_color_question = [random_color]


# random_question is always less then 2 before entering while loop
# while this loop is selecting empty strings it will continue run,
# but when the an actual question got chosen the loop stops
    while len(random_color_question) < 2:

        # choose random question from the dictionary by random color key
        # that was passed via 'random_color' variable
        chosen_question = random.choice(lst_of_available_questions)

        # chosen_question is a string. > 1 means not empty
        # so we taking any not empty string and attach it as 2nd
        # item into random_color_question list

        if len(chosen_question) > 1:
            random_color_question.append(chosen_question)

    return random_color_question

def parameters():

    result = choose_color_question()
    font_family = ["Avenir Next, Verdana, sans-serif",
                   "Roboto, Verdana, sans-serif",
                   "Mina, Verdana, sans-serif",
                   "Open Sans, Verdana, sans-serif",
                   "Lato, Verdana, sans-serif",
                   "Noto Sans, Verdana, sans-serif",
                   "Montserrat, Verdana, sans-serif",
                   "Oswald, Verdana, sans-serif",
                   "Roboto Condensed, Verdana, sans-serif",
                   "Times New Roman, Georgia, serif",
                   "Georgia, Times New Roman, serif"
                   ]

    color = result[0]
    question = result[1]

    historical_questions.append(question)
    historical_colors.append(color)
    font_family_list.append(random.choice(font_family))


    font_family_choice = font_family_list[-1]


    print("Current color and question: ", result)
    print("All previous question: ", historical_questions)
    print("Amount of historical questions", len(historical_questions))
    print("Chosen font is: ", font_family_list[-1])



    # if question not in historical_questions:
    if color in ['black', 'darkred', 'purple', 'blue', 'red', 'green', 'red']:
        font_color = "white"
        historical_font_colors.append(font_color)
        return {'question': question, 'color': color, 'font_color': font_color, \
                'font_family_choice': font_family_choice}
    else:
        font_color = "black"
        historical_font_colors.append(font_color)
        return {'question': question, 'color': color, 'font_color': font_color, \
                'font_family_choice': font_family_choice}



# render template with passed variables
# question, bg color (color), font_color, font_family_choice
@app.route('/TheRoom')
def index():
    question = historical_questions[-1]
    print(question[0])
    first_leter = question[:1].capitalize()
    question = question[1:]
    question = first_leter + question
    color = historical_colors[-1]
    font_color = historical_font_colors[-1]
    font_family_choice = font_family_list[-1]
    print(font_family_choice)

    return render_template('index.html',
                           question=question,
                           color=color,
                           font_color=font_color,
                           font_family_choice=font_family_choice)


# Create URL with question on it
@app.route('/')
def urls():

    # call a func parameters() to get a random question, color, etc...
    data = parameters()

    # from all returns just take question
    question = data['question']

    # The second parameter of url_for() constructs the URL with passed variable
    # In our case this is "question"
    return redirect(url_for('index', question=question))

@app.route("/about")
def about():
    return render_template('about.html')

# db.create_all()
parameters()
clean_dict_creation()
# migrate_data()

# print(historical_questions[-1])
# print(clean_dict_creation())
print('Done')

# remove debug mode before putting it on the internet
if __name__ == "__main__":
    app.run(debug=True, port=5000)
