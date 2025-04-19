import json
import pymysql
import os

conn = None


def bedrock_formatted_response(body):
    formatted_response = {
        "messageVersion": "1.0",
        "response": {
            "actionGroup": "ExecuteSQLQuery",
            "function": "executeSQLQuery",
            "functionResponse": {
            "responseBody": {
                "TEXT": {
                "body": json.dumps(body, default=str)
                }
            }
            }
        },
        "sessionAttributes": {},
        "promptSessionAttributes": {},
        "knowledgeBasesConfiguration": []
        }
    return formatted_response


def extract_query_from_parameters(parameters):
    for param in parameters:
        if param.get("name") == "query":
            return param.get("value")
    return None

def get_connection():
    global conn
    if conn is None or not conn.open:
        try:
            print("🏓 Pinging old DB connection...")
            conn.ping(reconnect=True)
        except:
            conn = None
        print("🔌 Opening new DB connection...")
        conn = pymysql.connect(
            host=os.environ['DB_HOST'],
            user=os.environ['DB_USER'],
            password=os.environ['DB_PASSWORD'],
            database=os.environ['DB_NAME'],
            cursorclass=pymysql.cursors.DictCursor,
            connect_timeout=5
        )
    else:
        print("✅ Reusing existing DB connection")
    return conn

def lambda_handler(event, context):
    
    print("📦 Incoming event:", json.dumps(event))
    
    connection = get_connection()
    
    parameters = event.get("parameters", [])
    query = extract_query_from_parameters(parameters)
    
    if not query.strip().lower().startswith("select"):
        return {
            "contentType": "application/json",
            "body": {"error":"Only SELECT queries are allowed."}
        }
    
    try:
        with connection.cursor() as cursor:
            cursor.execute(query)
            rows = cursor.fetchall()
            result = []
            for row in rows:
                if hasattr(row, "_mapping"):
                    result.append(dict(row._mapping))
                else:
                    result.append(dict(row))
                    
            print("✈️ Outgoing response:", json.dumps(result, default = str))

            
            return bedrock_formatted_response(result)
    except Exception as e:
        print(f"❌ Error: {e}")
        return bedrock_formatted_response({"error": str(e)})
