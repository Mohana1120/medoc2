from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates


from pydantic import BaseModel
import json
from models.drug_extract import extract_drugs

app = FastAPI()
templates = Jinja2Templates(directory="templates")



with open("data/drug_db.json") as f:
    DRUG_DB = json.load(f)

class Prescription(BaseModel):
    text: str
    age: int

def match_age_to_range(age: int, age_dosage: dict) -> str:
    for range_str, dosage in age_dosage.items():
        if '+' in range_str:
            min_age = int(range_str.replace('+', ''))
            if age >= min_age:
                return dosage
        elif '-' in range_str:
            low, high = map(int, range_str.split('-'))
            if low <= age <= high:
                return dosage
        elif range_str.isdigit():
            if int(range_str) == age:
                return dosage
    return None
@app.get("/form", response_class=HTMLResponse)
async def form_page(request: Request):
    return templates.TemplateResponse("form.html", {"request": request})

@app.post("/analyze-ui", response_class=HTMLResponse)
async def analyze_ui(request: Request, text: str = Form(...), age: int = Form(...)):
    result = analyze_prescription(Prescription(text=text, age=age))
    return templates.TemplateResponse("result.html", {"request": request, "result": result})


@app.post("/analyze/")
def analyze_prescription(prescription: Prescription):
    drugs = extract_drugs(prescription.text)
    drug_names = [d["drug"].lower() for d in drugs]

    issues = []
    recommendations = []
    alternatives = set()

    for drug_info in drugs:
        name = drug_info["drug"].lower()


        matched = next((entry for entry in DRUG_DB if entry["medicine"].lower() == name), None)
        if matched:
            details = matched.get("details", {})

    
            for interaction in details.get("interacts_with", []):
                if interaction.lower() in drug_names and interaction.lower() != name:
                    issues.append(f"{name.title()} interacts with {interaction.title()}")

            
            age_dosage = details.get("age_dosage", {})
            dosage = match_age_to_range(prescription.age, age_dosage)
            if dosage:
                recommendations.append(f"{name.title()} recommended dose for age {prescription.age}: {dosage}")

        
            for alt in details.get("alternatives", []):
                alternatives.add(f"{alt} (alternative to {name.title()})")

    return {
        "drugs": drugs,  
        "issues": issues,
        "recommendations": recommendations,
        "alternatives": sorted(alternatives)
    }
