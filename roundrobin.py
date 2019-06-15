import random 
from topic_model import *
from elopy import *



num_eng_files = len(eng_only_files)

def get_two_articles():
    a, b = int(random.uniform(1,num_eng_files)), int(random.uniform(1,num_eng_files))
    text_a = open(eng_only_files[a]).read()
    text_b = open(eng_only_files[b]).read()
    return text_a, text_b


def setup_elopy():
    i = Implementation()
    for topic in range(0,30):
        i.addPlayer(topic)
    return i


def rate_two_articles(elo_tournament):
    a, b = get_two_articles()
    topic_a = predict_topic_from_text(a)[0]['topic #']
    topic_b = predict_topic_from_text(b)[0]['topic #']
    print(a)
    print("=======================")
    print("=======================")
    print(b)
    guess=input()[0]
    if guess=='a':
        elo_tournament.recordMatch(topic_a, topic_b, winner=topic_a)
    elif guess=='b':
        elo_tournament.recordMatch(topic_a, topic_b, winner=topic_b)
    else:
         elo_tournament.recordMatch(topic_a, topic_b, draw=True)
