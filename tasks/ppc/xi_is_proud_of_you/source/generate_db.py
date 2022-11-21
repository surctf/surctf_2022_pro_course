from random import randint
from peewee import *

db = SqliteDatabase('questions.db')

class Question(Model):
    text = CharField(unique=True)
    valid_answ = CharField()
    bad_answ1 = CharField()
    bad_answ2 = CharField()
    bad_answ3 = CharField()
    valid_ind = IntegerField()

    class Meta:
        db_table = 'questions'
        database = db


db.connect()
db.create_tables([Question, ])

with open("pasta.txt", "r") as f:
    pasta = f.read().replace("\n", " ").lower()

words = pasta.split(" ")

for i in range(1000):
    # Generating question
    q = ""
    for j in range(6):
        part_len = randint(3, 8)
        start = randint(0, len(words) - part_len - 1)
        q = q + " ".join(words[start:start+part_len]) + " "
    q = q.capitalize()[:-1] + "?"

    # Generating valid answer
    part_len = randint(1, 4)
    start = randint(0, len(words) - part_len - 1)
    valid_answ = " ".join(words[start:start+part_len]).capitalize() + "!"

    # Generating invalid answers(3)
    bad_answers = []
    for i in range(3):
        part_len = randint(1, 4)
        start = randint(0, len(words) - part_len - 1)
        bad_answ = " ".join(words[start:start+part_len]).capitalize() + "!"
        bad_answers.append(bad_answ)




    Question.get_or_create(
        text=q, 
        valid_answ=valid_answ, 
        bad_answ1=bad_answers[0],
        bad_answ2=bad_answers[1],
        bad_answ3=bad_answers[2],
        valid_ind=randint(1, 4)
    )

db.close()