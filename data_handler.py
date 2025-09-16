# Description: This module contains functions for convering CSV file
# into dictionaries in both directions: English -> Ukrainian and Ukrainian -> English.


import csv 


#English to Ukranian
def get_topics_English_to_Ukranian(file):
    """
    The function gives a data for te cards of word to practice vocabulay
    with transtaling words from English language to Ukanian.

    The function tskes a CSV file which has three columns ("eng_word", 
    "ukr_word" and "topic") and transforms it to a dictionary which
    contains the topics as the keys and the dictionaries with the pairs
    eng_word - ukr_word as the values.

    Function behavior includes the reading CSV file, striping extra
    whitespaces from topics names, English and Ukranian words and ignoring
    the topics where is no words to practice yet.
    """
    topics = {}     # Create empty dictionary to store topics

    # Open the CSV file with UTF-8 encoding
    with open(file, encoding="utf-8") as f:   
        reader = csv.DictReader(f) # Read rows as dictionaries using headers
        
        for row in reader:
            topic = row["topic"].strip()
            eng_word = row["eng_word"].strip()
            ukr_word = row["ukr_word"].strip()

            # Only add if topic and both words are not empty
            if topic and eng_word and ukr_word:
                if topic not in topics: # If topic not already in topics dictionary, add it
                    topics[topic] = {} # Initialize nested dictionary for word -> translation
                topics[topic][eng_word] = ukr_word # Add the English -> Ukrainian pair 

    return topics


def get_topics_Ukranian_to_English(file):
    """
    The function gives a data for te cards of word to practice vocabulay
    with transtaling words from Ukanian language to English.

    The function is very similar to the get_topics_English_to_Ukranian() function.
    It tskes and returns the same types of value, it has the same behavior.
    
    Only one difference is that this function create  ato to translate words
    from Ukranian language to English. The the keys in the nested dictionaries
    are the Ukranian words and the values are their translation on English.
    
    """
    topics = {} # Create empty dictionary to store topics

    # Open the CSV file with UTF-8 encoding
    with open(file, encoding="utf-8") as f:   
        reader = csv.DictReader(f) # Read rows as dictionaries using headers

        for row in reader:
            topic = row["topic"].strip()
            eng_word = row["eng_word"].strip()
            ukr_word = row["ukr_word"].strip()

            # Only add if topic and both words are not empty
            if topic and eng_word and ukr_word:
                if topic not in topics: # If topic not already in topics dictionary, add it
                    topics[topic] = {} # Initialize nested dictionary for word -> translation
                topics[topic][ukr_word] = eng_word # Add the Ukrainian -> English pair 

    return topics