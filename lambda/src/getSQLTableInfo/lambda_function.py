from enum import Enum
import json
import pymysql
import os

conn = None

def bedrock_formatted_response(body):
    formatted_response = {
        "messageVersion": "1.0",
        "response": {
            "actionGroup": "GetTableInfo",
            "function": "describeDatabaseSchema",
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


def get_connection():
    global conn
    try:
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
    except Exception as e:
        print(f"❌ Exception occurred while connecting to DB: {type(e).__name__} - {str(e)}")
        raise

def lambda_handler(event, context):
    print("📦 Incoming event:", json.dumps(event))
    
    connection = get_connection()
    table_info = {"tables": []}
    
    try:
        with connection.cursor() as cursor:
            cursor.execute("SHOW TABLES;")
            tables = [row["Tables_in_{}".format(os.environ['DB_NAME'])] for row in cursor.fetchall()]
            print("📋 Found tables:", tables)
            for table in tables:
                cursor.execute(f"DESCRIBE `{table}`;")
                columns = cursor.fetchall()
                formatted_columns = []
                for col in columns:
                    formatted_columns.append({
                        "name": col["Field"],
                        "type": col["Type"],
                        "nullable": col["Null"] == "YES",
                        "key": col["Key"],
                        "default": col["Default"],
                        "extra": col["Extra"]
                    })

                table_info["tables"].append({
                        "name": table,
                        "columns": formatted_columns
                        })

            print("✈️ Outgoing response:", json.dumps(table_info))
            return bedrock_formatted_response(table_info)
    except Exception as e:
        print(f"❌ Error: {type(e).__name__} - {str(e)}")
        return bedrock_formatted_response({"error": f"{type(e).__name__} - {str(e)}"})
