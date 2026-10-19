from agents.extractor import extract_report

from database import (
    get_patient_reports,
    insert_alert,
    get_patient_alerts
)
from config import client
import json
from agents.comparator import compare_reports
from agents.reasoning_agent import generate_reasoning
from agents.alert_agent import generate_alerts
from agents.recommendation_agent import generate_recommendations


def process_new_report(uploaded_file):
    """
    Main workflow of the Medical Agent.

    Workflow:
    1. Extract current report
    2. Get patient ID
    3. Retrieve previous reports
    4. Compare current report with previous reports
    5. Generate AI reasoning
    6. Generate alerts
    7. Save alerts to SQLite
    8. Generate recommendations
    9. Retrieve all saved patient alerts
    10. Return everything to Streamlit
    """

    print("\n========== Medical Agent Started ==========\n")

    try:

      

        structured_report = extract_report(uploaded_file)

        if structured_report is None:
            print(" Report extraction failed.")
            return None

        print(" Report extraction completed.")


     

        patient_id = structured_report.get(
            "patient_id",
            "P001"
        )

        print(f"\nPatient ID: {patient_id}")


        

        previous_reports = get_patient_reports(patient_id)

        print("\n========== PREVIOUS REPORTS ==========\n")

        if len(previous_reports) == 0:

            print("No previous reports found.")

        else:

            print(
                f"Found {len(previous_reports)} previous report(s)."
            )

            for report in previous_reports:

                print(report)


       

        comparison_result = compare_reports(
            structured_report,
            previous_reports
        )

        print("\n========== COMPARISON RESULT ==========\n")

        print(comparison_result)


      

        reasoning = generate_reasoning(
            structured_report,
            previous_reports
        )

        print("\n========== AI REASONING ==========\n")

        print(reasoning)


      

        alerts = generate_alerts(
            patient_id,
            reasoning
        )

        print("\n========== GENERATED ALERTS ==========\n")

        print(alerts)


        

        if alerts:

            for alert in alerts:

                # Make sure patient_id exists
                if not alert.get("patient_id"):

                    alert["patient_id"] = patient_id

                insert_alert(alert)

            print(" New alerts stored successfully.")

        else:

            print(" No new alerts generated.")


       

        recommendations = generate_recommendations(
            alerts
        )

        print("\n========== RECOMMENDATIONS ==========\n")

        print(recommendations)


        
        patient_alerts = get_patient_alerts(
            patient_id
        )

        print("\n========== SAVED PATIENT ALERTS ==========\n")

        if len(patient_alerts) == 0:

            print("No saved alerts found.")

        else:

            for alert in patient_alerts:

                print(alert)


      
        print(
            "\n========== Workflow Completed ==========\n"
        )


   
        return {

            "current_report": structured_report,

            "previous_reports": previous_reports,

            "comparison": comparison_result,

            "reasoning": reasoning,

            "alerts": alerts,

            "recommendations": recommendations,

            "patient_alerts": patient_alerts

        }


    except Exception as e:

        print(f" Workflow Error: {e}")

        return None