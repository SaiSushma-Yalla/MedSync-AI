import sqlite3


def create_table():
    """
    Creates the reports table if it doesn't already exist.
    """

    connection = sqlite3.connect("medical.db")
    cursor = connection.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS reports(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_id TEXT,
        doctor TEXT,
        speciality TEXT,
        date TEXT,
        diagnosis TEXT,
        medications TEXT,
        creatinine TEXT,
        egfr TEXT,
        recommendations TEXT
    )
    """)

    connection.commit()
    connection.close()



def create_alert_table():
    """
    Creates the alerts table if it doesn't already exist.
    """

    connection = sqlite3.connect("medical.db")
    cursor = connection.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS alerts(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_id TEXT,
        severity TEXT,
        title TEXT,
        reason TEXT,
        recommendation TEXT
    )
    """)

    connection.commit()
    connection.close()



def insert_report(structured):
    """
    Inserts one extracted report into SQLite.
    """

    try:

        create_table()

        connection = sqlite3.connect("medical.db")
        cursor = connection.cursor()

        diagnosis = ", ".join(
            structured.get("diagnosis", [])
        )

        recommendations = ", ".join(
            structured.get("recommendations", [])
        )

        medication_list = []

        for medicine in structured.get("medications", []):

            name = medicine.get("name", "")
            dose = medicine.get("dose", "")

            medication_list.append(
                f"{name} {dose}".strip()
            )

        medications = ", ".join(medication_list)

        cursor.execute("""
        INSERT INTO reports(
            patient_id,
            doctor,
            speciality,
            date,
            diagnosis,
            medications,
            creatinine,
            egfr,
            recommendations
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (

            structured.get("patient_id", "P001"),
            structured.get("doctor", ""),
            structured.get("speciality", ""),
            structured.get("date", ""),
            diagnosis,
            medications,
            structured.get("creatinine", ""),
            structured.get("egfr", ""),
            recommendations

        ))

        connection.commit()

        print(" Report inserted successfully.")

    except Exception as e:

        print(f" Database Error: {e}")

    finally:

        connection.close()



def get_patient_reports(patient_id):
    """
    Returns every report belonging to one patient.
    """

    try:

        connection = sqlite3.connect("medical.db")
        connection.row_factory = sqlite3.Row

        cursor = connection.cursor()

        cursor.execute("""
        SELECT *
        FROM reports
        WHERE patient_id = ?
        ORDER BY date ASC
        """, (patient_id.strip(),))

        rows = cursor.fetchall()

        reports = []

        for row in rows:
            reports.append(dict(row))

        print(f"\n Found {len(reports)} previous report(s) for Patient {patient_id}")

        return reports

    except Exception as e:

        print(f"Database Error: {e}")

        return []

    finally:

        connection.close()



def insert_alert(alert):
    """
    Saves one medical alert into SQLite.
    """

    try:

        create_alert_table()

        connection = sqlite3.connect("medical.db")
        cursor = connection.cursor()

        cursor.execute("""
        INSERT INTO alerts(
            patient_id,
            severity,
            title,
            reason,
            recommendation
        )
        VALUES (?, ?, ?, ?, ?)
        """, (

            alert.get("patient_id", ""),
            alert.get("severity", ""),
            alert.get("title", ""),
            alert.get("reason", ""),
            alert.get("recommendation", "")

        ))

        connection.commit()

        print(" Alert saved successfully.")

    except Exception as e:

        print(f" Alert Database Error: {e}")

    finally:

        connection.close()



def get_patient_alerts(patient_id):
    """
    Returns all alerts for a patient.
    """

    try:

        create_alert_table()

        connection = sqlite3.connect("medical.db")
        connection.row_factory = sqlite3.Row

        cursor = connection.cursor()

        cursor.execute("""
        SELECT *
        FROM alerts
        WHERE patient_id = ?
        ORDER BY id DESC
        """, (patient_id.strip(),))

        rows = cursor.fetchall()

        alerts = []

        for row in rows:
            alerts.append(dict(row))

        print(f" Found {len(alerts)} alert(s) for Patient {patient_id}")

        return alerts

    except Exception as e:

        print(f" Database Error: {e}")

        return []

    finally:

        connection.close()



if __name__ == "__main__":

    create_table()
    create_alert_table()

    reports = get_patient_reports("P001")

    print("\n========== PATIENT REPORTS ==========\n")

    for report in reports:
        print(report)

    alerts = get_patient_alerts("P001")

    print("\n========== PATIENT ALERTS ==========\n")

    for alert in alerts:
        print(alert)