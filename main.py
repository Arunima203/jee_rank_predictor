from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
import pandas as pd
import requests
import io
import os

app = FastAPI()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

df_global = None

def load_jee_data():
    global df_global
    github_raw_url = "https://raw.githubusercontent.com/atmabodha/OpenNLP/main/IIT-JEE/JEE_2025_Cutoffs.xlsx"
    try:
        print("GitHub file try to loaded...")
        response = requests.get(github_raw_url)
        df = pd.read_excel(io.BytesIO(response.content), engine='openpyxl')

        df['Opening Rank'] = pd.to_numeric(df['Opening Rank'], errors='coerce')
        df['Closing Rank'] = pd.to_numeric(df['Closing Rank'], errors='coerce')
        df = df.dropna(subset=['Opening Rank', 'Closing Rank'])

        df_global = df
        print(df.columns.tolist())
        print("Real Cutoff Data Loaded Successfully into FastAPI!")
    except Exception as e:
        print("Error loading data:", e)

# ডাটা লোড করা শুরু
load_jee_data()

@app.get("/")
def home(request: Request):
    # হোম পেজ লোড করার সময় context-এ অবশ্যই request পাঠাতে হবে
    return templates.TemplateResponse(request=request,
    name="index.html")

@app.post("/predict")
def predict(
    request: Request,
    exam_type: str = Form(...),
    rank: int = Form(...),
    gender: str = Form(...),
    quota: str = Form("Any"),
    interest: str = Form(None)
):


    print("Selected Exam =", exam_type)
    print("Rank =", rank)
    print("Quota =", quota)
    global df_global

    if df_global is None:
        return templates.TemplateResponse("result.html", {"request": request, "error": "Data not loaded yet. Please restart server."})

    if gender == "Female":
        gender_filter = "Female-only (including Supernumerary)"
    else:
        gender_filter = "Gender-Neutral"

    if exam_type == "advanced":

        institute_filter = df_global[
             df_global["Institute"].str.contains(
                "Indian Institute of Technology",
               case= False,
               na= False 
             )
        ]    

    else:

        institute_filter = df_global[
             -df_global["Institute"].str.contains(
                "Indian Institute of Technology",
                case=False,
                na=False
             )
        ]

    try:

        print("Exam Type =", exam_type)
        print("Total Institutes =",
        len(institute_filter))

        condition = (institute_filter['Closing Rank'] >= rank) & (institute_filter['Gender'] == gender_filter)
        if quota != "Any":
            condition = condition & (institute_filter['Quota'] == quota)

        # Apply Interest branch filtering
        coding_keywords = ["computer", "information technology", "data science", "artificial intelligence", "software", "computing", "computational"]
        
        if interest == "Coding":
            interest_mask = institute_filter['Academic Program Name'].str.contains('|'.join(coding_keywords), case=False, na=False)
            condition = condition & interest_mask
        elif interest == "Research":
            research_keywords = ["physics", "chemistry", "mathematics", "science", "biotech", "biological", "geophysics", "aerospace", "astronomy", "research"]
            interest_mask = (institute_filter['Academic Program Name'].str.contains('|'.join(research_keywords), case=False, na=False) | \
                             institute_filter['Academic Program Name'].str.contains("Bachelor of Science", case=False, na=False) | \
                             institute_filter['Academic Program Name'].str.contains("BS", case=False, na=False))
            # Exclude coding branches
            exclude_mask = -institute_filter['Academic Program Name'].str.contains('|'.join(coding_keywords), case=False, na=False)
            condition = condition & interest_mask & exclude_mask
        elif interest == "MBA":
            mba_keywords = ["industrial", "operations research", "management", "business", "economics", "production", "mba"]
            interest_mask = institute_filter['Academic Program Name'].str.contains('|'.join(mba_keywords), case=False, na=False)
            # Exclude coding branches
            exclude_mask = -institute_filter['Academic Program Name'].str.contains('|'.join(coding_keywords), case=False, na=False)
            condition = condition & interest_mask & exclude_mask

        filtered_df = institute_filter[condition]
        filtered_df = filtered_df.sort_values(by='Closing Rank').head(20)
        guidance = ""

        if interest == "Coding":
              guidance = f"Based on your rank {rank}, Computer Science, AI, Data Science and Electronics related branches are recommended for software engineering careers."

        elif interest == "Research":
              guidance = f"Based on your rank {rank}, Physics, Mathematics and Science-oriented programs may be better suited for research and higher studies."

        elif interest == "MBA":
              guidance = f"Based on your rank {rank}, branches like Mechanical, Electrical and Industrial Engineering can provide a strong foundation before pursuing an MBA."

        colleges_list = []
        for _, row in filtered_df.iterrows():

            closing_rank = int(row['Closing Rank'])
            margin = closing_rank - rank

            if margin > 3000:
                chance = "High"
            elif margin >1000:
                chance = "Medium"
            else:
                chance = "Low"

            colleges_list.append({
                "institute": row['Institute'],
                "program": row['Academic Program Name'],
                "quota": row['Quota'],
                "opening": int(row['Opening Rank']),
                "closing": int(row['Closing Rank']),
                "margin" : margin,
                "chance" : chance 
            })

        return templates.TemplateResponse(
            request=request,
            name="result.html", 
            context={
                "rank": rank, 
                "gender": gender,
                "quota": quota,
                "interest": interest,
                "guidance": guidance,
                "colleges": colleges_list
            }
        )
    except Exception as e:
       print("ERROR:" , e)

       return templates.TemplateResponse(
           request=request,
           name="result.html" ,
           context ={
            "error": str(e)
           }
       )
       
@app.get("/compare")
def compare(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="compare.html",

        )   