from fastapi import APIRouter, HTTPException, Query, Body
from utils.query_helper import get_sql_query
from pydantic import BaseModel
from utils.database_helper import execute_sql_query

class Payload(BaseModel):
    query : str

router = APIRouter()

@router.get("/generate-sql")
async def generate_sql(question : str = Query(..., description="Natural language question for the database")):
    sql_query = get_sql_query(question)
    return {
        "question" : question,
        "generated_sql" : sql_query.strip()
    }

@router.post("/execute-sql-query")
async def execute_query(payload : Payload = Body(..., description="Query for the database")):
    if not payload.query.strip().lower().startswith("select"):
        raise HTTPException(status_code=403, detail="Only SELECT queries are allowed.")
    response = await execute_sql_query(payload.query)
    return {
        "query" : payload.query,
        "result" : response
    }
