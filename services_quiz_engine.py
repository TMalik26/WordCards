# Description: this module contains functions to create the deck of Cards for practice,
# function to create the result of user practice, describing two that classes
# The idea was to show the Card class whith two properties:
# English translation of a word and Ukrainian translation, and the Result class, which
# has three properties: the total amaunt of words in a topic the user chose
# and practiced, amount of correct answers and wrong answers.
# To not to lose the atentivness of what exactly is happening inside each function
# was used the typing standard module.
# The idea of using the dataclasses standard module was to pay attention
# which type of instance of each class has


from dataclasses import dataclass
import random
from typing import Dict, List, Tuple


@dataclass
class Card:
    prompt: str
    answer: str

def make_deck(topic_dict: Dict[str, str]) -> List[Card]:
    """
    The function creates a deck of cards which depends on the user's choice
    whether it was the direction "English to Ukranian" or "Ukrainian to English".
    The direction is set on the first screen "home".
    
    Its behavior includes transforming the dictionary into the list
    of tuples ("word", "translation"), creating list of Card objects and 
    shuffling the deck to provide the user with unexpected words topic sequence.
    """
    # direction: "English to Ukrainian" or "Ukrainian to English"
    items = list(topic_dict.items())
    deck = [Card(k, v) for k, v in items]
    random.shuffle(deck)
    return deck

def normalize(s: str) -> str:
    """
    The function accepts the string and returns the string.

    It transforms user's answer by splitting it by any whitespace (in case
    the answer involves several words), converting letters to lowercase,
    stripping the extra whitespaces, and joining the transformed answer back into the one string to prevent
    user answer from considering it by the program as wrong one.
    """
    return " ".join(s.strip().lower().split())

def check_answer(user: str, card: Card) -> bool:
    """
    The function checks the user's answer and return "True", 
    if it is correct and "False", if it isn't.
    """
    return normalize(user) == normalize(card.answer)

@dataclass
class Result:
    total: int
    correct: int
    wrong_cards: List[Card]

def run_quiz_round(deck: List[Card], answers: List[str]) -> Result:
    """
    The function checks each answer of user during the quiz round.
    It creates a list of tuples from two lists - the deck of Cards and user's answers,
    compares each user's answer with the answer in a Card, counts the number of
    correct answers, and creates a list of Cards with wrong answers to give the user
    the possibility to only work on those ones further after the round finishes.

    The function accepts a deck - a list of Cards, and the answers - list of user's answers.
    It creates and returns the oblect of a class Result.
    """
    correct = 0
    wrong = []
    for card, user in zip(deck, answers):
        if check_answer(user, card):
            correct += 1
        else:
            wrong.append(card)
        
    return Result(total=len(deck), correct=correct, wrong_cards=wrong)


    