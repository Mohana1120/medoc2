from fastapi import FastAPI
from pydantic import BaseModel
from models.drug_extract import extract_drugs
import json

app = FastAPI()

with open("data/drug_db.json") as f:
    DRUG_DB = json.load(f)

class Prescription(BaseModel):
    text: str
    age: int

@app.post("/analyze/")
def analyze_prescription(prescription: Prescription):
    drugs = extract_drugs(prescription.text)
    drug_names = [d["drug"].lower() for d in drugs]

    issues = []
    alternatives = set()
    recommendations = []

    for drug_info in drugs:
        name = drug_info["drug"].lower()
        if name in DRUG_DB:
            for other in drug_names:
                if other != name and other in DRUG_DB[name]["interacts_with"]:
                    issues.append(f"{name.title()} interacts with {other.title()}")

            group = "child" if prescription.age < 18 else "adult"
            dosage = DRUG_DB[name]["age_dosage"].get(group)
            if dosage:
                recommendations.append(f"{name.title()} recommended dose for {group}s: {dosage}")

            alternatives.update(DRUG_DB[name].get("alternatives", []))

    return {
        "drugs": drugs,
        "issues": issues,
        "recommendations": recommendations,
        "alternatives": sorted(alternatives)
    }
