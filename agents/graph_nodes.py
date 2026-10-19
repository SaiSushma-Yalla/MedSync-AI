from database import insert_report


def store_report_node(state):
    """
    LangGraph Node 2

    Takes the structured report from Node 1
    and stores it in the SQLite database.
    """

    print("\n========== NODE 2: STORE REPORT ==========\n")

   

    report = state.get("report_json")


    if not report:

        print(" No report found in state.")

        return state


    try:

        insert_report(report)

        print(" Report stored successfully.")

    except Exception as e:

        print(
            f" Error storing report: {e}"
        )


    return state