# WordCards - English ↔ Ukrainian Flashcards

## Description
Simple Python flashcards program for practicing English ↔ Ukrainian vocabulary.

## Features
- Select language (English/Ukrainian)
- Choose topic by number
- Randomized cards
- Track correct and incorrect answers
- Retry mistakes

## Setup
1. Clone repository:
   git clone <your-repo-url>
2. Create virtual environment:
   python -m venv venv
   source venv/bin/activate   # Linux/Mac
   venv\Scripts\activate      # Windows
3. Install dependencies (if any):
   pip install -r requirements.txt

## Usage
Run the program:
   python main.py

## CSV Template
Use `data/WordCards_template.csv` as a template to create your own `WordCards.csv`.

Example CSV:
topic,eng_word,ukr_word
Animals,cat,кіт
Animals,dog,собака
Colors,red,червоний
Colors,blue,синій

## Notes
- `.gitignore` excludes __pycache__/, .env, venv/, and system files.
- Keep personal CSV data private.
