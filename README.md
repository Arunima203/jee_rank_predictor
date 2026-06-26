# JEE Smart College Advisor

## Preview

![Project Screenshot](screenshot.png)

An intelligent JEE college prediction portal built using FastAPI.

## Features

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

## Tech Stack

- FastAPI
- Pandas
- Jinja2
- OpenPyXL
- HTML
- CSS
- JavaScript

## Live Demo

https://jee-rank-predictor-6jwn.onrender.com

## Dataset

JEE 2025 Official Cutoff Dataset

Source:
https://github.com/atmabodha/OpenNLP/blob/main/IIT-JEE/JEE_2025_Cutoffs.xlsx

## Run Locally

```bash
pip install -r requirements.txt
uvicorn main:app --reload
