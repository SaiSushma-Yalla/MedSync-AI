from config import client
import json


def generate_recommendations(alerts):
    """
    Generate patient-friendly explanations and safe next steps
    from alerts produced by the Alert Agent.

    This agent does NOT read PDFs.
    It receives structured alerts only.

    It does NOT diagnose or provide medication changes.
    """

    print("\n========== Recommendation Agent ==========\n")


    if not alerts:

        print("ℹ️ No alerts found.")

        return {
            "recommendations": []
        }



    try:

        alerts_json = json.dumps(
            alerts,
            indent=2,
            ensure_ascii=False
        )

    except Exception as e:

        print(f"❌ Error converting alerts to JSON: {e}")

        return {
            "recommendations": []
        }



    prompt = f"""
You are an AI assistant helping patients understand
possible care coordination issues.

You are NOT a doctor.

IMPORTANT SAFETY RULES:

- Do NOT diagnose the patient.
- Do NOT recommend starting any medication.
- Do NOT recommend stopping any medication.
- Do NOT recommend increasing any medication.
- Do NOT recommend decreasing any medication.
- Do NOT provide a medical treatment plan.
- Do NOT make a definitive medical conclusion.
- Explain only what was detected by the Medical Agent.
- Explain the issue in simple, patient-friendly language.
- Encourage the patient to discuss the issue with
  their treating healthcare professionals.

Here are the alerts detected by the Medical Agent:

{alerts_json}

For EACH alert, generate:

1. A short title
2. A simple patient-friendly explanation
3. Why the issue may matter
4. Safe next steps for the patient

The next steps should encourage appropriate communication
with the patient's treating healthcare professionals.

Do not tell the patient to change medication on their own.

Return ONLY valid JSON.

Do not use markdown.
Do not use ```json.
Do not write anything before or after the JSON.

Use exactly this structure:

{{
    "recommendations": [
        {{
            "title": "",
            "explanation": "",
            "why_it_matters": "",
            "next_steps": []
        }}
    ]
}}
"""
    
    print(" Recommendation prompt created.")

 

    try:

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.2
        )

    except Exception as e:

        print(
            f" Groq Recommendation Error: {e}"
        )

        return {
            "recommendations": []
        }

    

    try:

        response_text = (
            response
            .choices[0]
            .message
            .content
            .strip()
        )

    except Exception as e:

        print(
            f" Error reading Groq response: {e}"
        )

        return {
            "recommendations": []
        }

    print(
        "\n========== RAW RECOMMENDATION RESPONSE =========="
    )

    print(response_text)

    print(
        "=================================================="
    )

 

    if response_text.startswith("```"):

        response_text = (
            response_text
            .replace("```json", "")
            .replace("```JSON", "")
            .replace("```", "")
            .strip()
        )

    

    try:

        recommendations = json.loads(
            response_text
        )

    except json.JSONDecodeError as e:

        print(
            " Invalid JSON returned by Groq."
        )

        print(e)

        print(
            "\nRaw response was:"
        )

        print(response_text)

        return {
            "recommendations": []
        }



    if not isinstance(
        recommendations,
        dict
    ):

        print(
            " Recommendation response is not a JSON object."
        )

        return {
            "recommendations": []
        }

    if "recommendations" not in recommendations:

        print(
            " 'recommendations' field missing."
        )

        return {
            "recommendations": []
        }

    if not isinstance(
        recommendations["recommendations"],
        list
    ):

        print(
            " 'recommendations' must be a list."
        )

        return {
            "recommendations": []
        }

 

    print(
        "\n Recommendation generation completed."
    )

    print(
        f"Generated "
        f"{len(recommendations['recommendations'])} "
        f"recommendation(s)."
    )



    return recommendations