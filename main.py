from cards import practice_cards_English_to_Ukranian, practice_cards_Ukranian_to_English
from data_handler import get_topics_English_to_Ukranian, get_topics_Ukranian_to_English


def main():
    """
    Main function of the flashcards program.

    Behavior:
        - Greets the user.
        - Allows the user to choose the language (English/Ukrainian).
        - Displays topics and allows selection by number.
        - Starts flashcard practice in the chosen direction.
        - Handles returning to language selection or main menu.
    """
    # Greet the user
    print("Вітаю!")
    
    # Main program loop (language selection)
    while True:
        chosen_language = input(
            "\nОберіть мову на якою будуть паказані картки або натисніть Enter для виходу.\n"
            "Введіть 'E' для англійської, або 'U' для української: " 
        )
        
        # Exit program if user presses Enter
        if chosen_language == "":
            break

        # Load topics depending on selected language
        if chosen_language == "E":
            topics = get_topics_English_to_Ukranian("data/WordCards.csv")
        elif chosen_language == "U":
            topics = get_topics_Ukranian_to_English("data/WordCards.csv")
        else:
            # Invalid input
            print("\nНекоректний вибір мови. Спробуйте ще раз.")
            continue
       
        # Loop for topic selection
        while True:
            print("\nOберіть розділ карток: \n")

            # Convert dictionary to list for numbering
            items = list(topics.items())

            # Display list of topics with numbers and word counts
            for i, (topic_name, words_dict) in enumerate(items, start=1):
                n = len(words_dict)
                print(f"{i}. {topic_name} ({n} слів)")

            # User selects a topic
            chosen_topic = input(
                "\nВведіть порядковий номер розділу або натисніть Enter для вибору мови: "
            )

            # Return to language selection
            if chosen_topic == "":
                break

            # Validate numeric input
            try:
                index = int(chosen_topic)
            except ValueError:
                print("\nВи ввели неправильний номер теми. Спробуйте ще раз.")
                continue  

            # Check if number is within valid range
            if 1 <= index <= len(items):
                topic_name, words_dict = items[index - 1]

                # Check that topic is not empty
                if not words_dict:
                    print("\nОй-вей! У обраному вими розділі поки що 0 слів для практики.\nСпробуйте обрати інший.")
                    continue

                # Run the flashcard practice in the correct direction    
                else:
                    if chosen_language == "E":
                        practice_cards_English_to_Ukranian(words_dict)
                    elif chosen_language == "U":
                        practice_cards_Ukranian_to_English(words_dict)

            else:
                print("\nТакого розділу поки що не існує, але Ви можете його створити самостійно.\nДля цього відкоригуйте файл 'WordCards.csv' у кореневому директорії, додавши небхідні слова.")
                continue 


if __name__ == "__main__":
    main()