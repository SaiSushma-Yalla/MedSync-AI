def compare_reports(current_report, previous_reports):
    """
    Compare every previous report with the current uploaded report.
    """

    if len(previous_reports) <= 1:
        return {
            "comparison_results": [],
            "alerts": []
        }

    comparison_results = []
    alerts = []

    
    for report in previous_reports[:-1]:

        comparison = {
            "previous_report_id": report["id"],
            "previous_date": report["date"],

            "doctor_changed":
                report["doctor"] != current_report.get("doctor", ""),

            "diagnosis_changed":
                report["diagnosis"] != ", ".join(current_report.get("diagnosis", [])),

            "medication_changed":
                report["medications"] != ", ".join(
                    [
                        f"{m.get('name','')} {m.get('dose','')}".strip()
                        for m in current_report.get("medications", [])
                    ]
                ),

            "creatinine_changed":
                report["creatinine"] != current_report.get("creatinine", ""),

            "egfr_changed":
                report["egfr"] != current_report.get("egfr", ""),

            "recommendations_changed":
                report["recommendations"] != ", ".join(
                    current_report.get("recommendations", [])
                )
        }

        comparison_results.append(comparison)

        # Generate alerts
        if comparison["medication_changed"]:
            alerts.append(
                f"Medication changed compared with report dated {report['date']}"
            )

        if comparison["creatinine_changed"]:
            alerts.append(
                f"Creatinine changed compared with report dated {report['date']}"
            )

        if comparison["egfr_changed"]:
            alerts.append(
                f"eGFR changed compared with report dated {report['date']}"
            )

    return {
        "comparison_results": comparison_results,
        "alerts": alerts
    }