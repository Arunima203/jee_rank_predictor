import pandas as pd
import requests
import io

github_raw_url = "https://github.com/atmabodha/OpenNLP/raw/refs/heads/main/IIT-JEE/JEE_2025_Cutoffs.xlsx"

try:
    print("GitHub link tried to load...")
    
   
    response = requests.get(github_raw_url)
    
   
    df = pd.read_excel(io.BytesIO(response.content))
    
    print("🎉congratulation,file successfully loaded!")
    print(df.head()) 
except Exception as e:
    print("sorry! till now no file loaded")
    print(e)