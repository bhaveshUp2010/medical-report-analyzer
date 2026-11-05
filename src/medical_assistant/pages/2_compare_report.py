import streamlit as st
from medical_assistant.chain.comparison import compare_medical_reports

st.title("Compare your medical Reports")

file_1 = st.file_uploader("Upload your medical report:" , type = ["txt"], key="file_1")
file_2 = st.file_uploader("Upload your medical report:" , type = ["txt"], key="file_2")

if file_1 and file_2 :
    st.toast("Files uploaded successfully!", icon="✅")

    reports = {
        "report_1": file_1.read().decode("utf-8"),
        "report_2": file_2.read().decode("utf-8")
    }

    if st.button("compare reports"):
        with st.spinner("comparing the reports:"):
            comparison = compare_medical_reports(reports= reports)
            st.session_state["comparison"] = comparison
 
        st.write("Your reports comparison:")
        with st.expander("Comparison"):
            st.write(comparison["comparison"]) 

        with st.expander("comparison summary"):
            st.write(comparison["summary"])
