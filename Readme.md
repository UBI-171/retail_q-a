# 🧠 Talk to Your Database 💹

A natural language interface to query your database — powered by AI.

---

## ✨ Overview

This project allows users to **ask questions in plain English** and receive answers based on their **SQL database** — no SQL knowledge required! It leverages modern LLMs and serverless tech to interpret questions, generate SQL, run queries, and respond with user-friendly insights.

---

## 🏗️ Architecture Evolution

### ⚙️ Version 1 – FastAPI + LLMs + Lambda (Manual Orchestration)

🧱 **Stack:**
- `Streamlit UI` → `FastAPI Backend` → `Llama Model (via Bedrock)` → `SQL Generation & Execution`
- Separate endpoints for:
  - `/v1/generate-sql`: Use LLM to translate question to SQL
  - `/v1/execute-sql-query`: Execute SQL on RDS/MySQL

🛠️ **Flow:**
1. User enters a question in Streamlit.
2. FastAPI sends the question to LLM via Bedrock to generate SQL.
3. FastAPI then executes that SQL via a DB connection.
4. Response shown as JSON or text.

📉 **Limitations:**
- More infra management (API server)
- Manual orchestration logic
- Less flexibility for adding tools/logic


---

### 🤖 Version 2 – Bedrock Agent + Lambda Tools (Serverless AI)

🧱 **Stack:**
- `Streamlit UI` → `Bedrock Agent` (Claude-powered)
  - 🔌 **Tool 1:** GetTableInfo Lambda
  - 🔌 **Tool 2:** ExecuteSQLQuery Lambda

🛠️ **Flow:**
1. User asks a question in Streamlit.
2. Streamlit uses `boto3` to call `invoke_agent()` directly.
3. Bedrock Agent uses Claude to:
   - Parse intent
   - Call Lambda tools as needed
   - Compose and return a natural language answer
4. Result shown in the frontend.

🚀 **Advantages:**
- Fully serverless 🟢
- Less backend code to manage 🧼
- Easy tool orchestration by the Agent 🛠️
- Natural conversation-like responses 💬

---

## 💻 Streamlit UI

Simple, clean interface to ask questions:

```python
question = st.text_input("Enter your question")
```

Example questions:
- *“What is the stock count of black Adidas t-shirts?”*
- *“List all discounts available for Nike products.”*

---

## 🧠 Bedrock Agent Configuration (v2)

You’ll need:
- ✅ A Bedrock Agent with a Claude model
- ✅ Two Lambda tools integrated:
  - `GetTableInfo` (returns table schema)
  - `ExecuteSQLQuery` (executes SQL and returns result)
- ✅ Permissions to invoke Bedrock Agent from your environment

---

## 🚀 Getting Started

1. 🛠️ Configure AWS credentials for `boto3`
2. ✅ Deploy Bedrock Agent with correct `agentId` and `aliasId`
3. 🧪 Run Streamlit UI:
```bash
streamlit run app.py
```
4. 💬 Ask your database questions!

---

## 📌 TODOs & Ideas

- [ ] Add chat memory in Streamlit 💬
- [ ] Enable table visualizations 📊
- [ ] Support for multi-step queries
- [ ] Extend tools to support INSERT/UPDATE/DELETE ❗

---

## 🙌 Credits

Built with ❤️ using:
- 🦙 Claude (via Amazon Bedrock)
- 🐍 Python & Streamlit
- 🛠️ AWS Lambda & RDS