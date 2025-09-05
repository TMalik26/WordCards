# Description: This module contains functions for convering CSV file
# into dictionaries in both directions: English -> Ukrainian and Ukrainian -> English.


import csv 


#English to Ukranian
def get_topics_English_to_Ukranian(file):
    """
    Load flashcard topics from a CSV file for English -> Ukrainian practice.

    Parameters:
        file (str): Path to the CSV file containing flashcards with columns
                    'topic', 'eng_word', 'ukr_word'.

    Returns:
        dict: Dictionary where keys are topic names and values are dictionaries
              mapping English words to their Ukrainian translations.

    Behavior:
        - Reads the CSV file.
        - Strips whitespace from topic names and words.
        - Ignores rows with missing English or Ukrainian words.
    """
    topics = {}     # Create empty dictionary to store topics

    # Open the CSV file with UTF-8 encoding
    with open(file, encoding="utf-8") as f:   
        reader = csv.DictReader(f) # Read rows as dictionaries using headers
        
        for row in reader:
            topic = row["topic"].strip()
            eng_word = row["eng_word"].strip()
            ukr_word = row["ukr_word"].strip()

            # If topic not already in topics dictionary, add it
            if topic not in topics:
                topics[topic] = {} # Initialize nested dictionary for word -> translation

            # Add the English -> Ukrainian pair if both words exist
            if eng_word and ukr_word:
                topics[topic][eng_word] = ukr_word

    return topics


def get_topics_Ukranian_to_English(file):
    """
    Load flashcard topics from a CSV file for Ukrainian -> English practice.

    Parameters:
        file (str): Path to the CSV file containing flashcards with columns
                    'topic', 'eng_word', 'ukr_word'.

    Returns:
        dict: Dictionary where keys are topic names and values are dictionaries
              mapping Ukrainian words to their English translations.

    Behavior:
        - Reads the CSV file.
        - Strips whitespace from topic names and words.
        - Ignores rows with missing English or Ukrainian words.
    """
    topics = {} # Create empty dictionary to store topics

    # Open the CSV file with UTF-8 encoding
    with open(file, encoding="utf-8") as f:   
        reader = csv.DictReader(f) # Read rows as dictionaries using headers

        for row in reader:
            topic = row["topic"].strip()
            eng_word = row["eng_word"].strip()
            ukr_word = row["ukr_word"].strip()

            # If topic not already in topics dictionary, add it
            if topic not in topics:
                topics[topic] = {}              

            # Initialize nested dictionary for word -> translation
            if eng_word and ukr_word:
                topics[topic][ukr_word] = eng_word

    return topics