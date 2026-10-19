from typing import TypedDict, Any


class MedicalAgentState(TypedDict, total=False):

    
    pdf: Any


    report_json: dict

   
    previous_reports: list

    
    comparison: dict

   
    reasoning: dict

    alerts: list

    recommendations: dict

  
    patient_alerts: list