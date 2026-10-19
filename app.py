import streamlit as st

from graph import medical_graph


st.set_page_config(
    page_title="Medical Report Analyzer",
    page_icon="🏥",
    layout="wide"
)


st.title(" Medical Report Analyzer")

st.write(
    "Upload a medical report to analyze it using "
    "an Agentic AI medical coordination workflow."
)


uploaded_file = st.file_uploader(
    "Upload Medical Report",
    type=["pdf"]
)


if uploaded_file is None:

    st.info(
        " Please upload a PDF medical report."
    )

    st.stop()



st.success(
    " PDF uploaded successfully!"
)


if st.button(
    " Analyze Medical Report"
):

    initial_state = {
        "pdf": uploaded_file
    }

    print(
        "\n========== STARTING MEDICAL GRAPH ==========\n"
    )


    with st.spinner(
        " Running Medical Agent workflow..."
    ):

        try:

            result = medical_graph.invoke(
                initial_state
            )

        except Exception as e:

            st.error(
                f" Medical workflow failed: {e}"
            )

            st.exception(e)

            st.stop()

    print(
        "\n========== MEDICAL GRAPH COMPLETED ==========\n"
    )

    st.success(
        " Medical Agent workflow completed!"
    )


    with st.expander(
        " Developer: View Final LangGraph State"
    ):

        st.write(
            "Keys returned by LangGraph:"
        )

        st.write(
            list(result.keys())
        )

        st.json(result)


    st.subheader(
        " Current Report"
    )

    current_report = result.get(
        "report_json",
        {}
    )

    if current_report:

        st.json(
            current_report
        )

    else:

        st.warning(
            " No extracted report was returned."
        )

    st.subheader(
        " Previous Reports"
    )

    history = result.get(
        "history",
        []
    )

    if not history:

        st.info(
            "No previous reports found."
        )

    else:

        st.write(
            f"Found **{len(history)}** previous report(s)."
        )

        for i, report in enumerate(
            history,
            start=1
        ):

            with st.expander(
                f" Previous Report {i}"
            ):

                st.json(
                    report
                )


    st.subheader(
        "Report Comparison"
    )

    conflict = result.get(
        "conflict",
        {}
    )

    if not conflict:

        st.info(
            "No comparison result available."
        )

    else:

        st.json(
            conflict
        )

        if conflict.get("conflict") is True:

            st.warning(
                " Possible coordination conflict detected."
            )

        else:

            st.success(
                " No coordination conflict detected."
            )


 
    st.subheader(
        " AI Reasoning / RAG"
    )

    reasoning = result.get(
        "reasoning",
        {}
    )

  
    if reasoning:

      
        reasoning_conflicts = reasoning.get(
            "conflicts",
            []
        )

        if reasoning_conflicts:

            for i, conflict_item in enumerate(
                reasoning_conflicts,
                start=1
            ):

                st.markdown(
                    f"###  RAG Conflict {i}"
                )

               
                issue = conflict_item.get(
                    "issue",
                    ""
                )

                if issue:

                    st.warning(
                        f" {issue}"
                    )

          
                severity = conflict_item.get(
                    "severity",
                    ""
                )

                if severity:

                    st.write(
                        f"**Severity:** {severity}"
                    )

            
                reason = conflict_item.get(
                    "reason",
                    ""
                )

                if reason:

                    st.write(
                        f"**Reason:** {reason}"
                    )

                evidence = conflict_item.get(
                    "evidence",
                    ""
                )

                if evidence:

                    st.write(
                        "**Medical Evidence:**"
                    )

                    st.info(
                        evidence
                    )

                source = conflict_item.get(
                    "source",
                    ""
                )

                if source:

                    st.write(
                        f"**Source:** {source}"
                    )

        else:

            st.info(
                "No RAG conflicts were generated."
            )

    else:

        st.info(
            "No RAG reasoning was generated."
        )


    st.subheader(
        " Patient-Friendly Recommendation"
    )

    recommendation = result.get(
        "recommendation",
        {}
    )

    if recommendation:

        recommendations = recommendation.get(
            "recommendations",
            []
        )

        if recommendations:

            for i, rec in enumerate(
                recommendations,
                start=1
            ):

                st.markdown(
                    f"### Recommendation {i}"
                )

                title = rec.get(
                    "title",
                    "Possible Coordination Issue"
                )

                explanation = rec.get(
                    "explanation",
                    ""
                )

                why_it_matters = rec.get(
                    "why_it_matters",
                    ""
                )

                next_steps = rec.get(
                    "next_steps",
                    []
                )

             
                st.warning(
                    f" {title}"
                )

             
                if explanation:

                    st.write(
                        "**Explanation:**"
                    )

                    st.write(
                        explanation
                    )

              
                if why_it_matters:

                    st.write(
                        "**Why it may matter:**"
                    )

                    st.write(
                        why_it_matters
                    )

           
                if next_steps:

                    st.write(
                        "**Safe next steps:**"
                    )

                    for step in next_steps:

                        st.write(
                            f"• {step}"
                        )

        else:

        
            st.json(
                recommendation
            )

    else:

        st.info(
            "No recommendation generated."
        )


  
    st.subheader(
        " Doctor Coordination Message"
    )

    doctor_message = result.get(
        "doctor_message",
        {}
    )

    if doctor_message:

        if isinstance(
            doctor_message,
            dict
        ):

            st.json(
                doctor_message
            )

        else:

            st.write(
                doctor_message
            )

    else:

        st.info(
            "No doctor message generated."
        )


    st.subheader(
        " Notification"
    )

    notification = result.get(
        "notification",
        {}
    )

    if notification:

        st.success(
            " Notification workflow completed."
        )

        if isinstance(
            notification,
            dict
        ):

            st.json(
                notification
            )

        else:

            st.write(
                notification
            )

    else:

        st.info(
            "No notification generated."
        )


    st.subheader(
        " LangGraph Workflow"
    )

    st.success(
        """
        START → Extract Report → Store Report →
        Retrieve History → Compare Reports →
        Decision → RAG Reasoning → Recommendation →
        Doctor Message → Notification → END
        """
    )