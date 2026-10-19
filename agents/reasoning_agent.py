from config import client
from rag.retriever import search_knowledge_base

import json


def generate_reasoning(current_report, previous_reports):
    """
    RAG-based Medical Reasoning Agent.

    Workflow:
    1. Create a medical search query from the current report.
    2. Search the medical knowledge base.
    3. Retrieve relevant guideline chunks.
    4. Send previous reports + current report + retrieved
       medical knowledge to Groq.
    5. Ask the LLM to identify possible coordination conflicts.
    6. Return structured JSON.
    """

    print("\n========== RAG REASONING AGENT ==========\n")

   

    query_parts = []


    medications = current_report.get(
        "medications",
        []
    )

    for medicine in medications:

        if isinstance(medicine, dict):

            name = medicine.get(
                "name",
                ""
            )

            dose = medicine.get(
                "dose",
                ""
            )

            if name or dose:

                query_parts.append(
                    f"{name} {dose}"
                )

        else:

            query_parts.append(
                str(medicine)
            )



    creatinine = current_report.get(
        "creatinine",
        ""
    )

    egfr = current_report.get(
        "egfr",
        ""
    )

    if creatinine:

        query_parts.append(
            f"creatinine {creatinine}"
        )

    if egfr:

        query_parts.append(
            f"eGFR {egfr}"
        )

  

    query_parts.append(
        "kidney function medication dosage "
        "medication safety specialist recommendations"
    )



    query = " ".join(query_parts)

    print("========== SEARCH QUERY ==========")
    print(query)


    try:

        retrieved_chunks = search_knowledge_base(
            query,
            top_k=3
        )

    except Exception as e:

        print(
            f" Knowledge retrieval error: {e}"
        )

        retrieved_chunks = []

    print(
        f"\n Retrieved "
        f"{len(retrieved_chunks)} "
        f"medical knowledge chunk(s)."
    )

   
    knowledge_text = ""

    for result in retrieved_chunks:

        
        source = result.get(
            "source",
            result.get(
                "filename",
                "Unknown"
            )
        )

        content = result.get(
            "text",
            result.get(
                "content",
                ""
            )
        )

        score = result.get(
            "score",
            result.get(
                "distance",
                ""
            )
        )

        if not content:

            continue

        knowledge_text += (
            f"Source: {source}\n"
            f"Similarity Score: {score}\n"
            f"Content:\n{content}\n\n"
        )

  

    if not knowledge_text:

        knowledge_text = (
            "No relevant medical guideline "
            "was retrieved from the knowledge base."
        )

    print(
        "\n========== RETRIEVED MEDICAL KNOWLEDGE ==========\n"
    )

    print(knowledge_text)

  

    current_json = json.dumps(
        current_report,
        indent=4
    )

    previous_json = json.dumps(
        previous_reports,
        indent=4
    )

    

    prompt = f"""
You are an AI assistant analyzing possible
medical care coordination issues.

You are NOT a doctor.

Do NOT diagnose the patient.

Do NOT recommend starting medication.

Do NOT recommend stopping medication.

Do NOT recommend increasing medication.

Do NOT recommend decreasing medication.

Do NOT provide a treatment plan.

Your job is only to identify and explain
possible coordination concerns between
different medical reports.

Use the retrieved medical guidelines as
supporting evidence.

IMPORTANT:
Only use information that is present in the
patient reports or retrieved medical guidelines.

Do not invent medical facts.

If there is not enough evidence to identify
a meaningful conflict, clearly state that
there is insufficient evidence.

==================================================
PREVIOUS PATIENT REPORTS
==================================================

{previous_json}

==================================================
CURRENT PATIENT REPORT
==================================================

{current_json}

==================================================
RETRIEVED MEDICAL GUIDELINES
==================================================

{knowledge_text}

==================================================
TASK
==================================================

Analyze the previous reports together with
the current report.

Pay particular attention to:

1. Medication changes
2. Medication dose changes
3. Kidney function changes
4. Creatinine changes
5. eGFR changes
6. Recommendations from different specialists
7. Possible coordination conflicts

Explain whether the reports contain a
possible coordination concern.

Use the retrieved guidelines as evidence.

For every identified conflict, explain:

- What changed
- Why it may represent a coordination concern
- What evidence from the reports supports it
- Which retrieved guideline supports the concern

Do NOT give treatment instructions.

Do NOT tell the patient to change medication.

Do NOT diagnose the patient.

Return ONLY valid JSON.

Use exactly this format:

{{
    "conflicts": [
        {{
            "conflict": true,
            "severity": "Low | Medium | High",
            "issue": "",
            "reason": "",
            "evidence": "",
            "source": ""
        }}
    ]
}}

If there is no meaningful conflict, return:

{{
    "conflicts": []
}}

Do not use markdown.

Do not use ```json.

Do not write anything before or after the JSON.
"""

    print(
        "\n Final RAG prompt created."
    )

  

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

        print(
            f" Groq reasoning error: {e}"
        )

        return {
            "conflicts": []
        }

   

    response_text = (
        response
        .choices[0]
        .message
        .content
        .strip()
    )

    print(
        "\n========== RAW LLM RESPONSE ==========\n"
    )

    print(response_text)



    if response_text.startswith("```"):

        response_text = (
            response_text
            .replace("```json", "")
            .replace("```JSON", "")
            .replace("```", "")
            .strip()
        )


    try:

        reasoning = json.loads(
            response_text
        )

    except json.JSONDecodeError as e:

        print(
            f" Invalid JSON returned by Groq: {e}"
        )

        print(
            "\nRaw response was:"
        )

        print(response_text)

        return {
            "conflicts": []
        }


    if not isinstance(
        reasoning,
        dict
    ):

        print(
            " Reasoning response is not a dictionary."
        )

        return {
            "conflicts": []
        }

    if "conflicts" not in reasoning:

        print(
            " 'conflicts' key missing from LLM response."
        )

        reasoning["conflicts"] = []



    if not isinstance(
        reasoning["conflicts"],
        list
    ):

        print(
            " 'conflicts' is not a list."
        )

        reasoning["conflicts"] = []

    

    print(
        "\n========== FINAL RAG REASONING ==========\n"
    )

    print(
        json.dumps(
            reasoning,
            indent=4
        )
    )

    print(
        "\n RAG reasoning completed."
    )

    return reasoning




if __name__ == "__main__":

    current_report = {

        "patient_id": "P001",

        "doctor": "Endocrinologist",

        "speciality": "Endocrinology",

        "date": "2026-07-15",

        "diagnosis": [
            "Type 2 Diabetes Mellitus"
        ],

        "medications": [

            {
                "name": "Metformin",
                "dose": "1000mg"
            }

        ],

        "creatinine": "2.5",

        "egfr": "30",

        "recommendations": []

    }

    previous_reports = [

        {

            "patient_id": "P001",

            "doctor": "Nephrologist",

            "speciality": "Nephrology",

            "date": "2026-07-10",

            "creatinine": "2.0",

            "egfr": "40",

            "medications": [
                "Metformin 500mg"
            ],

            "recommendations": [
                "Review metformin dosing"
            ]

        }

    ]


    result = generate_reasoning(
        current_report,
        previous_reports
    )

 

    print(
        "\n========== FINAL REASONING RESULT ==========\n"
    )

    print(
        json.dumps(
            result,
            indent=4
        )
    )