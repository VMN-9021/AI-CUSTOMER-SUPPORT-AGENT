import streamlit as st

from agent import run_agent


st.set_page_config(
    page_title="AI Customer Support Agent",
    page_icon="🤖"
)


st.title("🤖 AI Customer Support Agent")

st.write(
    "Ask a customer support question and let the AI agent "
    "classify, retrieve information, generate and validate a response."
)


query = st.text_input(
    "Enter your question:"
)


if st.button("Submit"):

    if query.strip():

        with st.spinner("Processing your query..."):

            result = run_agent(query)

        st.subheader("Response")

        st.write(result["response"])

        st.subheader("Query Category")

        st.write(result["category"])

    else:

        st.warning("Please enter a question.")