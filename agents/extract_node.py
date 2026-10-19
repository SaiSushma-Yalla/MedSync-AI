from agents.extractor import extract_report


def extract_report_node(state):
    """
    LangGraph Node 1.

    Takes the uploaded PDF from the state,
    extracts structured information,
    and stores it back into the state.
    """

    print("\n========== NODE 1: EXTRACT REPORT ==========\n")

    

    pdf = state.get("pdf")

    if pdf is None:

        print(" No PDF found in state.")

        return state

    print(" PDF found in state.")

    

    try:

        report = extract_report(pdf)

    except Exception as e:

        print(
            f"❌ Report extraction failed: {e}"
        )

        state["report_json"] = {}

        return state



    if report is None:

        print("❌ Extractor returned no report.")

        state["report_json"] = {}

        return state



    state["report_json"] = report

    print(" Report extracted successfully.")

    print("\n========== EXTRACTED REPORT ==========\n")

    print(report)

    print(
        "\n========== NODE 1 COMPLETED ==========\n"
    )



    return state