import streamlit as st
from medical_assistant.chain.analysis import analyse_report


st.title("lets analyze your medical report:")

uploaded_file = st.file_uploader("Upload your medical report:" , type = ["txt"])

if uploaded_file:
    st.toast("File uploaded successfully!", icon="✅")

    content = uploaded_file.getvalue().decode("utf-8")

    if st.button("analyze report"):
        with st.spinner("analyzing your medical report:"):
            analysis = analyse_report(content)
            st.session_state["analysis"] = analysis

        st.subheader("Your report analysis:")
        with st.expander("Medical Summary"):
            st.write(analysis["summary"])

        with st.expander("extracted tests"):
            st.write(analysis["medical_data"])


        st.text("didnt understood a medical terminology? ")
        st.page_link("pages/2_compare_report.py", label="Understand terminiology")