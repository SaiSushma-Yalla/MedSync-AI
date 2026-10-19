from config import client
import fitz
import json
import os
from database import insert_report


def extract_report(uploaded_file):
    """
    Extract structured information from an uploaded medical PDF.
    Returns a Python dictionary.
    """

    try:
        pdf_bytes = uploaded_file.getvalue()

        document = fitz.open(
            stream=pdf_bytes,
            filetype="pdf"
        )

    except Exception as e:
        print(f" Error opening PDF: {e}")
        return None

    text = ""

    for page in document:
        text += page.get_text()

    document.close()


    prompt = f"""
You are a medical information extraction assistant.

Extract ONLY the following fields from the medical report.

Extract the patient ID if it is present in the report.

If the report does not contain a patient ID, return "P001" as the patient_id.

Return ONLY a valid JSON object.

Do not include explanations.
Do not use markdown.
Do not use ```json.
Do not write anything before or after the JSON.

The JSON format must be exactly:

{{
  "patient_id":"",
    "doctor":"",
    "speciality":"",
    "date":"",
    "diagnosis":[],
    "medications":[
        {{
            "name":"",
            "dose":""
        }}
    ],
    "creatinine":"",
    "egfr":"",
    "recommendations":[]
}}

Medical Report:

{text}
"""


    try:

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

    except Exception as e:
        print(f"Groq API Error: {e}")
        return None

    
    response_text = response.choices[0].message.content.strip()

    print("\n========== RAW RESPONSE ==========")
    print(response_text)
    print("==================================")

  
    if response_text.startswith("```"):

        response_text = (
            response_text
            .replace("```json", "")
            .replace("```", "")
            .strip()
        )

    
    try:

        structured = json.loads(response_text)

    except json.JSONDecodeError as e:

        print("\n Invalid JSON returned by Groq")
        print(e)
        return None

 
    os.makedirs("structured_reports", exist_ok=True)

  
    filename = os.path.splitext(uploaded_file.name)[0]

    json_file = f"structured_reports/{filename}.json"

    with open(json_file, "w", encoding="utf-8") as file:
        json.dump(
            structured,
            file,
            indent=4,
            ensure_ascii=False
        )

    print(f"\n JSON saved successfully to: {json_file}")

    
    print("\n========== EXTRACTED DATA ==========")
    print("Patient ID:", structured.get("patient_id"))
   
    print("Doctor:", structured.get("doctor"))

    print("Speciality:", structured.get("speciality"))

    print("Date:", structured.get("date"))

    print("Diagnosis:", structured.get("diagnosis"))

    print("Creatinine:", structured.get("creatinine"))

    print("eGFR:", structured.get("egfr"))

    print("Recommendations:", structured.get("recommendations"))

    print("\nMedicine List:")

    medications = structured.get("medications", [])

    if not medications:

        print("No medications found.")

    else:

        for medicine in medications:

            name = medicine.get("name", "").strip()

            dose = medicine.get("dose", "").strip()

            print(f"- {name} : {dose}")


    try:

        insert_report(structured)

        print("Report saved to database.")

    except Exception as e:

        print(f" Database Error: {e}")

    print("\n========== EXTRACTION COMPLETED ==========\n")

    return structured