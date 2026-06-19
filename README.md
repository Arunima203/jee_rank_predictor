JEE Smart College Advisor

An intelligent JEE college prediction portal built using FastAPI.

Features

- JEE Advanced and JEE Main prediction
- Gender-based filtering
- Home State / Other State quota filtering
- Interest-based recommendations
  - Coding
  - Research
  - MBA
- Smart Guidance System
- College Comparison Feature
- Admission Chance Analysis

Tech Stack

- FastAPI
- Pandas
- Jinja2
- OpenPyXL
- HTML
- CSS
- JavaScript

Dataset

JEE 2025 Official Cutoff Dataset

Source:
https://github.com/atmabodha/OpenNLP/blob/main/IIT-JEE/JEE_2025_Cutoffs.xlsx

Run Locally

pip install -r requirements.txt
uvicorn main:app --reload

Open:

http://127.0.0.1:8000

Future Improvements

- Match Score Recommendation
- Branch Ranking System
- AI-based Career Suggestions
- Better Analytics Dashboard