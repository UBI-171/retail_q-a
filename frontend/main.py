import streamlit as st
import requests

st.set_page_config(page_title="Talk to your database 💹", layout="centered")

st.title("Talk to your database 💹")

GENERATE_SQL_ENDPOINT = "http://127.0.0.1:8000/v1/generate-sql"
EXECUTE_SQL_ENDPOINT = "http://127.0.0.1:8000/v1/execute-sql-query"

question = st.text_input("Enter your question:", 
                         placeholder="e.g., What is the total stock of black Adidas t-shirts?")

if st.button("Run Query"):
    if not question.strip():
        st.warning("Please enter a valid question.")
    else:
        with st.spinner("Generating SQL from question..."):
            try:
                response = requests.get(GENERATE_SQL_ENDPOINT, params={"question": question})
                response.raise_for_status()
                sql_query = response.json().get("generated_sql", "")

                if not sql_query:
                    st.error("Failed to generate SQL.")
                else:
                    st.success("SQL Generated!")
                    st.code(sql_query, language="sql")

                    with st.spinner("Executing SQL query..."):
                        exec_response = requests.post(EXECUTE_SQL_ENDPOINT, json={"query": sql_query})
                        exec_response.raise_for_status()
                        result = exec_response.json()

                        # st.text_area("Result:", value=str(result), height=200, disabled=True)
                        st.code(result["result"], language="json")
            except requests.exceptions.HTTPError as http_err:
                try:
                    error_detail = http_err.response.json().get("detail",str(http_err))
                    st.error(f"API Error: {error_detail}")
                except Exception:
                    st.error(f"HTTP Error: {http_err}")
            except requests.exceptions.RequestException as req_err:
                st.error(f"Request Error: {req_err}")
            except Exception as e:
                st.error(f"Unexpected error: {e}")
                   