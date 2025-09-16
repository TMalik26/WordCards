# Description: This module implements a flashcard quiz application using Tkinter.
# It provides a GUI for practicing English ↔ Ukrainian vocabulary.
# 
# Screens:
#   - Home: select translation direction (EN→UA / UA→EN) and topic from CSV.
#   - Quiz: shows flashcards with a prompt, input field, and buttons to check or skip.
#   - Result: displays percentage of correct answers and allows review of wrong cards.
# 
# Features:
#   - Custom styling for Tkinter widgets (buttons, labels, entry fields, comboboxes).
#   - Supports multiple topics loaded from a CSV file.
#   - Tracks correct and incorrect answers and enables repeated practice for mistakes.


import tkinter as tk
from tkinter import ttk
import json
from datetime import datetime
import os
from data_handler import get_topics_English_to_Ukranian, get_topics_Ukranian_to_English
from services_quiz_engine import Card, make_deck, check_answer, Result, run_quiz_round


class QuizApp(tk.Tk):
    """
    Main application class for the Word Cards Quiz.

    Manages the following screens:
        - Home: select translation direction and topic
        - Quiz: display questions, input answers, skip cards
        - Result: display score and review wrong answers
    """


    def __init__(self):
        """
        Initialize the main Tkinter window, configure styles, load topics, 
        and build the Home screen.
        """
        super().__init__()
        self.title("Word Cards")
        self.geometry("750x460")
        self.resizable(False, False)
        # Configure styles for ttk widgets
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure("Quiz.TFrame", background="#9370DB")
        self.style.configure("Quiz.TButton", font=("Arial", 16, "bold"), foreground="#696969", background="#FFFF00", padding=10)
        self.style.configure("Quiz.TLabel", font=("Arial", 18, "bold"), foreground="#696969", background="#FFFF00")
        self.style.configure("Quiz.TEntry", font=("Arial", 18), fieldbackground="#F8F8FF", foreground="#696969", padding=10)
        self.style.configure("Quiz.TCombobox", font=("Arial", 18), fieldbackground="#F8F8FF", background="#F8F8FF", foreground="#696969", padding=10)
        # Load topics from CSV files
        self.topics_E2U = get_topics_English_to_Ukranian("data/WordCards.csv")
        self.topics_U2E = get_topics_Ukranian_to_English("data/WordCards.csv")
        self.direction = tk.StringVar(value="English to Ukranian")
        self.topic = tk.StringVar(value=sorted(self.topics_E2U.keys())[0])
        # Build the Home screen
        self.build_home()


    def build_home(self):
        """
        Build the Home screen where the user selects the translation direction
        and the topic. Includes 'Start' button to begin the quiz.
        """
        self.home = ttk.Frame(self, style="Quiz.TFrame", padding=32)
        self.home.pack(fill="both", expand=True)
        ttk.Label(self.home, text="Направлення перекладу", style="Quiz.TLabel").grid(row=0, column=0, sticky="e", padx=10, pady=10)
        ttk.Label(self.home, text="Оберіть тему", style="Quiz.TLabel").grid(row=1, column=0, sticky="e", padx=10, pady=10)
        # Direction combobox
        ttk.Combobox(
            self.home,
            textvariable=self.direction,
            values=["English to Ukranian", "Ukranian to English"],
            state="readonly",
            width=30,
            height=6,
            style="Quiz.TCombobox",
            font=("Arial", 18)
        ).grid(row=0, column=1, sticky="e")
        # Topic combobox
        self.topic_cb = ttk.Combobox(
            self.home,
            textvariable=self.topic,
            values=sorted(self.topics_E2U.keys()),
            state="readonly",
            width=35,
            height=10,
            style="Quiz.TCombobox",
            font=("Arial", 18)
        )
        self.topic_cb.grid(row=1, column=1, sticky="w", padx=10, pady=10)
        self.topic_cb['height'] = 10
        self.topic_cb.bind("<<ComboboxSelected>>", self.show_results_chosen_topic)
        # Label in case chosen topic is worked erlier
        self.previous_result_lb = ttk.Label(self.home, font=("Arial", 18), foreground="#FFFFF0", background="#9370DB")
        self.previous_result_lb.grid(row=2, column=0, columnspan=2, pady=12, ipady=6)
        self.home.columnconfigure(1, weight=1)
        # Start button
        ttk.Button(self.home, text="Почати!", command=self.start_quiz, style="Quiz.TButton").grid(row=3, column=0, columnspan=2, pady=12, ipady=6)      
        #Show the previous results if they were
        self.show_results_chosen_topic()


    def show_results_chosen_topic(self, event=None):
        """
        Show the laben on the home string with the describing of the results 
        of a chosen topic if that topic was worked erlier.
        """
        topic = self.topic.get()
        base_dir = os.path.dirname(os.path.abspath(__file__))
        results_dir = os.path.join(base_dir, "results")
        filename = "saved_result.json"
        os.makedirs(results_dir, exist_ok=True)
        filepath = os.path.join(results_dir, filename)
        if os.path.exists(filepath):
            with open(filepath, "r", encoding="utf-8") as f:
                saved_result_json = json.load(f)
        else:
            saved_result_json = {}
        if topic in saved_result_json:
            k1 = "Дата"
            k2 = "Результат"
            text_res = f"Дата проходження теми: {saved_result_json[topic][k1]}.\nРезультат: {saved_result_json[topic][k2]}"
            self.previous_result_lb.config(text=text_res)


    def start_quiz(self):
        """
        Start the quiz by creating a deck of cards for the selected topic
        and translation direction. Destroys the Home screen and builds the Quiz screen.
        """
        topic = self.topic.get()
        direction = self.direction.get()
        if direction == "English to Ukranian":
            data = self.topics_E2U[topic]
        else:
            data = self.topics_U2E[topic]
        self.deck = make_deck(data)
        self.answers = []
        self.home.destroy()
        self.build_quiz()


    def build_quiz(self):
        """
        Build the Quiz screen with question display, input field,
        buttons for submitting and skipping, and feedback label.
        """
        if hasattr(self, 'quiz') and self.quiz.winfo_exists():
            self.quiz.destroy()
        self.idx = 0
        self.quiz = ttk.Frame(self, style="Quiz.TFrame", padding=16)
        self.quiz.pack(fill="both", expand=True)
        self.question = ttk.Label(self.quiz, style="Quiz.TLabel")
        self.question.pack(anchor="w")
        self.user_answer = ttk.Entry(self.quiz, style="Quiz.TEntry")
        self.user_answer.pack(fill="x")
        btns = ttk.Frame(self.quiz)
        btns.pack(pady=8)
        ttk.Button(btns, text="Відповісти", command=self.submit_answer, style="Quiz.TButton").pack(side="left", padx=4, ipady=6)
        ttk.Button(btns, text="Пропустити картку", command=self.skip_card, style="Quiz.TButton").pack(side="left", padx=4, ipady=6)
        self.feedback = ttk.Label(self.quiz, style="Quiz.TLabel")
        self.feedback.pack(anchor="w", pady=6)
        # Show the first card
        self.show_card()


    def show_card(self):
        """
        Display the current card from the deck, clear the input field,
        and update feedback with the current progress.
        """
        if self.idx >= len(self.deck):
            self.finish_round()
            return
        card = self.deck[self.idx]
        self.question.config(text=card.prompt)
        self.user_answer.delete(0, tk.END)
        self.feedback.config(text=f"{self.idx+1}/{len(self.deck)}")


    def skip_card(self):
        """
        Skip the current card without answering.
        Show correct answer and move to the next card after a short delay.
        """
        user_input = ""
        if self.idx < len(self.deck):
            card = self.deck[self.idx]
            self.feedback.config(text=f"Правильна відповідь: {card.answer}")
            self.answers.append(user_input)
            self.idx += 1
            if self.idx >= len(self.deck):
                self.after(1000, self.finish_round)
            else:
                self.after(1000, self.show_card)


    def submit_answer(self):
        """
        Submit the user's answer for the current card,
        check correctness, display feedback, and move to next card.
        """
        card = self.deck[self.idx]
        user_input = self.user_answer.get()
        self.answers.append(user_input)
        ok = check_answer(user_input, card)
        if ok:
            self.feedback.config(text="Вірно!")
        else:
            self.feedback.config(text=f"Невірно. Правильна відповідь: {card.answer}")
        self.idx += 1
        self.after(1000, self.show_card)


    def finish_round(self):
        """
        Finish the quiz round, calculate the score,
        destroy the Quiz screen, and build the Result screen.
        """
        res = run_quiz_round(self.deck, self.answers)
        pct = (100 * res.correct) / len(self.deck)
        self.quiz.destroy()
        self.build_result(res, pct)
        self.save_results(res)


    def build_result(self, res, pct):
        """
        Build the Result screen showing percentage correct,
        total correct answers, and buttons for reviewing errors or returning home.

        Parameters:
            res (Result): Result object containing quiz outcome
            pct (float): Percentage of correct answers
        """
        if hasattr(self, 'result') and self.result.winfo_exists():
            self.result.destroy()
        self.result = ttk.Frame(self, style="Quiz.TFrame", padding=16)
        self.result.pack(fill="both", expand=True)
        lbl_result = ttk.Label(self.result, text=f"Результат: {pct}%. Правильних відповідей: {res.correct}/{res.total}", style="Quiz.TLabel")
        lbl_result.pack()
        ttk.Button(self.result, text="Робота над помилками", command=lambda: self.retry_errors(res), style="Quiz.TButton").pack(pady=4, ipady=6)
        ttk.Button(self.result, text="На головний екран", command=self.reset_to_home, style="Quiz.TButton").pack(pady=4, ipady=6)


    def retry_errors(self, res):
        """
        Retry only the cards that were answered incorrectly.
        Rebuild the Quiz screen for these wrong cards.

        Parameters:
            res (Result): Result object containing wrong_cards list
        """
        self.deck = res.wrong_cards
        self.answers = []
        self.result.destroy()
        self.build_quiz()


    def reset_to_home(self):
        """
        Destroy the Result screen and return to the Home screen.
        """
        self.result.destroy()
        self.build_home()


    def save_results(self, res):
        """
        Create a json file with result of each worked topic.
        If such file already exists - add new information to json file. 
        """
        # Define the repo "results" near the file with code
        base_dir = os.path.dirname(os.path.abspath(__file__))
        results_dir = os.path.join(base_dir, "results")
        filename = "saved_result.json"
        # Create the repo if it does not exist yet 
        os.makedirs(results_dir, exist_ok=True)
        # The full path to file
        filepath = os.path.join(results_dir, filename)
        # If such file already exist - open it and read as pethon's dict
        if os.path.exists(filepath):
            with open(filepath, "r", encoding="utf-8") as f:
                saved_result_json = json.load(f)
        # If not - creat an ampty dict
        else:
            saved_result_json = {}
        # Create the data we need to be putting into the label on the home screen near the topic
        topic = self.topic.get()
        day = datetime.now().strftime("%d.%m.%Y")
        # Update the existing or newly created saved_result_json python object by adding the results data
        saved_result_json[topic] = {
            "Дата" : day,
            "Результат" : f"Правильних відповідей {res.correct}/{res.total}."
        }           
        # Wrute a new updated json file with old dat (if it was) and new data
        with open(filepath, "w", encoding="utf-8") as json_file:
            json.dump(saved_result_json, json_file, ensure_ascii=False, indent=4)
        

if __name__ == "__main__":
    QuizApp().mainloop()
