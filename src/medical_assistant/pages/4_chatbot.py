import streamlit as st

st.title("Chatbot")
st.subheader("ask your questions to our chatbot")

analysis = st.session_state.get("analysis")
comparison = st.session_state.get("comparison")