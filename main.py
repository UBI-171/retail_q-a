from utils.query_helper import get_sql_query
from fastapi import FastAPI, Query

app = FastAPI()

@app.get("/generate-sql")
async def generate_sql(question : str = Query(..., description="Natura language question for the database")):
    sql_query = get_sql_query(question)
    return {
        "question" : question,
        "generated_sql" : sql_query.strip()
    }