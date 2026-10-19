from langgraph.graph import StateGraph, START, END

from agents.extractor import extract_report

from database import (
    insert_report,
    get_patient_reports
)

from agents.comparator import compare_reports

from agents.reasoning_agent import generate_reasoning

from agents.recommendation_agent import generate_recommendations




def extract_report_node(state):

    print("\n========== NODE 1: EXTRACT REPORT ==========\n")

    pdf = state["pdf"]

    try:

        report = extract_report(pdf)

    except Exception as e:

        print(
            f" Report extraction error: {e}"
        )

        state["report_json"] = None

        return state

    if report is None:

        print(
            " Report extraction failed."
        )

        state["report_json"] = None

        return state

    state["report_json"] = report

    print(
        " Report extracted successfully."
    )

    return state



def store_report_node(state):

    print(
        "\n========== NODE 2: STORE REPORT ==========\n"
    )

    report = state.get(
        "report_json"
    )

    if not report:

        print(
            " No report found."
        )

        return state

    try:

        insert_report(report)

        print(
            " Report stored successfully."
        )

    except Exception as e:

        print(
            f" Database error: {e}"
        )

    return state




def retrieve_history_node(state):

    print(
        "\n========== NODE 3: RETRIEVE HISTORY ==========\n"
    )

    report = state.get(
        "report_json",
        {}
    )

    patient_id = report.get(
        "patient_id",
        "P001"
    )

    print(
        f"Patient ID: {patient_id}"
    )

    try:

        history = get_patient_reports(
            patient_id
        )

        state["history"] = history

        print(
            f" Retrieved {len(history)} "
            "previous report(s)."
        )

    except Exception as e:

        print(
            f" History retrieval error: {e}"
        )

        state["history"] = []

    return state




def compare_reports_node(state):

    print(
        "\n========== NODE 4: COMPARE REPORTS ==========\n"
    )

    history = state.get(
        "history",
        []
    )

    current = state.get(
        "report_json",
        {}
    )

    if not current:

        print(" Current report not found.")

        state["conflict"] = {
            "conflict": False,
            "comparison_results": [],
            "alerts": []
        }

        return state

    try:

        result = compare_reports(
            current,
            history
        )

   

        if not isinstance(result, dict):

            result = {
                "comparison_results": [],
                "alerts": []
            }

        

        comparison_results = result.get(
            "comparison_results",
            []
        )

        alerts = result.get(
            "alerts",
            []
        )

        

        has_conflict = (
            len(comparison_results) > 0
            or
            len(alerts) > 0
            or
            result.get("conflict") is True
        )

        

        result["conflict"] = has_conflict

        state["conflict"] = result

        print(
            "\n========== COMPARISON RESULT ==========\n"
        )

        print(result)

        print(
            f"\n Conflict status: {has_conflict}"
        )

    except Exception as e:

        print(
            f" Comparison error: {e}"
        )

        state["conflict"] = {
            "conflict": False,
            "comparison_results": [],
            "alerts": [],
            "error": str(e)
        }

    return state


def decide_next_step(state):

    print("\n========== DECISION NODE ==========\n")

    comparison = state.get(
        "conflict",
        {}
    )



    if comparison.get("conflict") is True:

        print(" Conflict detected.")
        print(" Routing to RAG.")

        return "rag"

 

    comparison_results = comparison.get(
        "comparison_results",
        []
    )

 
    alerts = comparison.get(
        "alerts",
        []
    )

   

    if comparison_results or alerts:

        print(" Comparison issue detected.")
        print(" Routing to RAG.")

        return "rag"


    print(" No coordination conflict detected.")
    print(" Ending workflow.")

    return "end"


    if conflict.get("conflict") is True:

        print(
            " Conflict detected."
        )

        print(
            " Routing to RAG."
        )

        return "rag"



    print(
        " No conflict detected."
    )

    print(
        "➡ Ending workflow."
    )

    return "end"




def rag_reasoning_node(state):

    print(
        "\n========== NODE 5: RAG REASONING ==========\n"
    )

    current = state.get(
        "report_json",
        {}
    )

    history = state.get(
        "history",
        []
    )

    try:

        reasoning = generate_reasoning(
            current,
            history
        )

        state["reasoning"] = reasoning

        print(
            "\n========== RAG RESULT ==========\n"
        )

        print(reasoning)

        print(
            "\n RAG reasoning completed."
        )

    except Exception as e:

        print(
            f" RAG reasoning error: {e}"
        )

        state["reasoning"] = {
            "conflicts": [],
            "error": str(e)
        }

    return state



def recommendation_node(state):

    print(
        "\n========== NODE 6: RECOMMENDATION ==========\n"
    )

    report = state.get(
        "report_json",
        {}
    )

    conflict = state.get(
        "conflict",
        {}
    )

    reasoning = state.get(
        "reasoning",
        {}
    )

    try:

        recommendation = generate_recommendations(
            report,
            conflict,
            reasoning
        )

        state["recommendation"] = recommendation

        print(
            "\n========== RECOMMENDATION RESULT ==========\n"
        )

        print(recommendation)

        print(
            "\n Recommendation generated."
        )

    except Exception as e:

        print(
            f" Recommendation error: {e}"
        )

        state["recommendation"] = {
            "recommendations": [],
            "error": str(e)
        }

    return state


def doctor_message_node(state):

    print(
        "\n========== NODE 7: DOCTOR MESSAGE ==========\n"
    )

    conflict = state.get(
        "conflict",
        {}
    )

    reasoning = state.get(
        "reasoning",
        {}
    )

    recommendation = state.get(
        "recommendation",
        {}
    )

    message = {
        "title": "Medical Coordination Review",
        "message": (
            "The patient's longitudinal reports contain "
            "findings that may require review by the "
            "treating healthcare professionals."
        ),
        "conflict": conflict,
        "reasoning": reasoning,
        "recommendation": recommendation
    }

    state["doctor_message"] = message

    print(
        "\n✅ Doctor coordination message generated."
    )

    return state


def notify_node(state):

    print(
        "\n========== NODE 8: NOTIFICATION ==========\n"
    )

    recommendation = state.get(
        "recommendation",
        {}
    )

    doctor_message = state.get(
        "doctor_message",
        {}
    )

    notification = {
        "status": "completed",
        "message": (
            "A medical coordination review has been "
            "generated from the available reports."
        ),
        "recommendation_available": bool(
            recommendation
        ),
        "doctor_message_available": bool(
            doctor_message
        )
    }

    state["notification"] = notification

    print(
        "🔔 Notification workflow completed."
    )

    return state





builder = StateGraph(dict)




builder.add_node(
    "extract_report",
    extract_report_node
)

builder.add_node(
    "store_report",
    store_report_node
)

builder.add_node(
    "retrieve_history",
    retrieve_history_node
)

builder.add_node(
    "compare_reports",
    compare_reports_node
)

builder.add_node(
    "rag_reasoning",
    rag_reasoning_node
)

builder.add_node(
    "recommendation",
    recommendation_node
)

builder.add_node(
    "doctor_message",
    doctor_message_node
)

builder.add_node(
    "notify",
    notify_node
)



builder.add_edge(
    START,
    "extract_report"
)

builder.add_edge(
    "extract_report",
    "store_report"
)

builder.add_edge(
    "store_report",
    "retrieve_history"
)

builder.add_edge(
    "retrieve_history",
    "compare_reports"
)




builder.add_conditional_edges(
    "compare_reports",

    decide_next_step,

    {
        "rag": "rag_reasoning",
        "end": END
    }
)



builder.add_edge(
    "rag_reasoning",
    "recommendation"
)




builder.add_edge(
    "recommendation",
    "doctor_message"
)




builder.add_edge(
    "doctor_message",
    "notify"
)




builder.add_edge(
    "notify",
    END
)



medical_graph = builder.compile()

print(
    "\n Medical LangGraph compiled successfully."
)