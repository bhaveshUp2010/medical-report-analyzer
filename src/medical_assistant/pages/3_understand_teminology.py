import streamlit as st
from medical_assistant.chain.explanation import understand_terminology

st.title("Understand the medical terminology with respect to the report")

term = st.text_input("Medical term you want to know:", placeholder="WBC")
question = st.text_input("Your question:", placeholder="what is the fullform")

if st.button("understand terminology"):
    with st.spinner("getting your work done:"):
        result = understand_terminology(term=term, question=question)

    st.write(result)