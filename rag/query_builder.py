def build_search_query(current_report, reasoning):
    """
    Build a search query for the medical knowledge base.

    The query is based on:
    - current patient report
    - AI-detected reasoning/conflict
    """

   

    medications = current_report.get("medications", [])
    creatinine = current_report.get("creatinine", "")
    egfr = current_report.get("egfr", "")
    diagnosis = current_report.get("diagnosis", [])

 
    medication_names = []

    for medicine in medications:

        if isinstance(medicine, dict):

            name = medicine.get("name", "")

            if name:
                medication_names.append(name)

        else:

            medication_names.append(str(medicine))

    medications_text = " ".join(medication_names)

    if isinstance(diagnosis, list):

        diagnosis_text = " ".join(
            str(item) for item in diagnosis
        )

    else:

        diagnosis_text = str(diagnosis)

   
    reasoning_text = ""

    if isinstance(reasoning, dict):

        reasoning_text = (
            reasoning.get("reason", "")
            or reasoning.get("conflict", "")
            or reasoning.get("explanation", "")
        )

    else:

        reasoning_text = str(reasoning)

 
    query_parts = []

    if medications_text:
        query_parts.append(medications_text)

    if diagnosis_text:
        query_parts.append(diagnosis_text)

    if creatinine:
        query_parts.append(
            "creatinine kidney function"
        )

    if egfr:
        query_parts.append(
            "eGFR kidney function"
        )

    if reasoning_text:
        query_parts.append(reasoning_text)

    query = " ".join(query_parts)

    if not query.strip():

        query = (
            "medication kidney function "
            "dosage recommendations"
        )

    print("\n========== SEARCH QUERY ==========")
    print(query)
    print("==================================")

    return query



if __name__ == "__main__":

    current_report = {
        "medications": [
            {
                "name": "Metformin",
                "dose": "1000 mg"
            }
        ],
        "creatinine": "2.5",
        "egfr": "35",
        "diagnosis": [
            "Type 2 Diabetes Mellitus"
        ]
    }

    reasoning = {
        "conflict": True,
        "reason": (
            "Metformin increased while "
            "kidney function worsened."
        )
    }

    query = build_search_query(
        current_report,
        reasoning
    )

    print("\nFinal Query:")
    print(query)