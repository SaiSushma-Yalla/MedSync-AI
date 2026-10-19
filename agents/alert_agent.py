def generate_alerts(patient_id, reasoning):
    """
    Generates patient alerts from the AI reasoning output.

    Parameters
    ----------
    patient_id : str
        Patient ID

    reasoning : dict
        Output returned by reasoning_agent.py

    Returns
    -------
    list
        List of generated alerts
    """

    print("\n========== ALERT AGENT STARTED ==========\n")

    alerts = []

    conflicts = reasoning.get("conflicts", [])

    if len(conflicts) == 0:

        print(" No conflicts found.")

        return alerts


    for conflict in conflicts:

        severity = conflict.get("severity", "Low")

        issue = conflict.get("issue", "Unknown Issue")

        reason = conflict.get("reason", "No reason provided.")


        if severity.lower() == "high":

            recommendation = (
                "Discuss this finding with your nephrologist "
                "and endocrinologist before changing medication."
            )

        elif severity.lower() == "medium":

            recommendation = (
                "Review the treatment plan during the next consultation."
            )

        else:

            recommendation = (
                "Continue monitoring and follow your doctor's advice."
            )

    
        alert = {
            "patient_id": patient_id,
            "title": "Medication Coordination Alert",
            "severity": severity,
            "issue": issue,
            "reason": reason,
            "recommendation": recommendation
        }

        alerts.append(alert)

    print("\n========== GENERATED ALERTS ==========")

    for alert in alerts:
        print(alert)

    print("\n========== ALERT AGENT COMPLETED ==========\n")

    return alerts


if __name__ == "__main__":

    patient_id = "P001"

    reasoning = {
        "conflicts": [
            {
                "severity": "High",
                "issue": "Medication Coordination Conflict",
                "reason": (
                    "Metformin dosage increased while kidney "
                    "function declined."
                )
            },
            {
                "severity": "Medium",
                "issue": "Recommendation Conflict",
                "reason": (
                    "Two specialists provided different follow-up advice."
                )
            }
        ]
    }

    alerts = generate_alerts(patient_id, reasoning)

    print("\nReturned Alerts:\n")

    for alert in alerts:
        print(alert)