import streamlit as st
import boto3
import json

st.set_page_config(page_title="Talk to your database 💹", layout="centered")
st.title("Talk to your database 💹")

AGENT_ID = "26IDHLJRHY"
REGION = "ap-south-1"
AGENT_ALIAS_ID = "WHT4PAEPAE"

bedrock_agent_client = boto3.client("bedrock-agent-runtime", region_name=REGION)

question = st.text_input(
    "Enter your question:",
    placeholder="e.g., What is the total stock of black Adidas t-shirts?"
)

if st.button("Ask"):
    if not question.strip():
        st.warning("Please enter a valid question.")
    else:
        with st.spinner("Talking to your Agent..."):
            try:
                response = bedrock_agent_client.invoke_agent(
                    agentAliasId=AGENT_ALIAS_ID,
                    agentId=AGENT_ID,
                    sessionId="streamlit-session",
                    inputText = question
                )

                full_response = ""
                for event in response["completion"]:
                    chunk = event.get("chunk", {}).get("bytes", b"").decode("utf-8")
                    full_response += chunk

                st.success("Agent's Answer:")
                st.write(full_response)

            except bedrock_agent_client.exceptions.ValidationException as ve:
                st.error(f"Validation Error: {ve}")
            except Exception as e:
                st.error(f"Error calling Bedrock Agent: {str(e)}")
