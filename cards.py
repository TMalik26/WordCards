# Description: This module contains functions for practicing flashcards
# in both directions: English -> Ukrainian and Ukrainian -> English.
# The functions track correct answers, incorrect answers, and allow
# the user to redo mistakes


from data_handler import get_topics_English_to_Ukranian, get_topics_Ukranian_to_English
import random


def practice_cards_English_to_Ukranian(topic):
    """
    Practice English -> Ukrainian flashcards.
    
    Parameters:
        topic (dict): Dictionary of English words as keys and Ukrainian translations as values.
        
    Behavior:
        - Randomizes the order of flashcards.
        - Tracks correct and incorrect answers.
        - Allows the user to retry incorrect answers.
    """
    correct = 0 # Counter for correct answers
    wrong_answers = {} # Store incorrect answers for review

    # Convert dictionary to list and shuffle to randomize flashcard order
    items = list(topic.items())
    random.shuffle(items)

    # Iterate over all flashcards
    for eng_word, ukr_word in items: 
        user_input = input(f"{eng_word}: ").strip() # Ask user for translation
        if user_input.lower() == ukr_word.lower():
            correct += 1
        else:
            wrong_answers[eng_word] = ukr_word # Save wrong answer

    # Check if all answers were correct        
    if correct == len(topic):
        print("\nВітаю! У вас 100% правильних відповідей!")
        return
    else:
        # Calculate percentage of correct answers
        x = (correct * 100) / len(topic)
        print(f"\nУ вас {x}% правильних відповідей!")

        # Ask user if they want to review mistakes
        answer = input(
            "\nБажаєте зробити роботу над помилками?\n"
            "(Введіть 'так' щоб продовжити, або 'ні' щоб повернутися до вибору розділу у головне меню): "
        )
        if answer.strip().lower() == "так":
            return practice_cards_English_to_Ukranian(wrong_answers)
        else:
            print("Повернення до головного меню...")


def practice_cards_Ukranian_to_English(topic):
    """
    Practice Ukrainian -> English flashcards.
    
    Parameters:
        topic (dict): Dictionary of Ukrainian words as keys and English translations as values.
        
    Behavior:
        - Randomizes the order of flashcards.
        - Tracks correct and incorrect answers.
        - Allows the user to retry incorrect answers.
    """
    correct = 0 # Counter for correct answers
    wrong_answers = {} # Store incorrect answers for review

    # Convert dictionary to list and shuffle to randomize flashcard order
    items = list(topic.items())
    random.shuffle(items)

    # Iterate over all flashcards
    for ukr_word, eng_word in items: 
        user_input = input(f"{ukr_word}: ").strip() # Ask user for translation
        if user_input.lower() == eng_word.lower():
            correct += 1
        else:
            wrong_answers[ukr_word] = eng_word # Save wrong answer

    # Check if all answers were correct
    if correct == len(topic):
        print("\nВітаю! У вас 100% правильних відповідей!")
        return
    else:
        # Calculate percentage of correct answers
        x = (correct * 100) / len(topic)
        print(f"\nУ вас {x}% правильних відповідей!")

        # Ask user if they want to review mistakes
        answer = input(
            "\nБажаєте зробити роботу над помилками?\n"
            "(Введіть 'так' щоб продовжити, або 'ні' щоб повернутися до вибору розділу у головне меню): "
        )
        if answer.strip().lower() == "так":
            return practice_cards_Ukranian_to_English(wrong_answers)
        else:
            print("Повернення до головного меню...")