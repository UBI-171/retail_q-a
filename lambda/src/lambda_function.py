import json
import pymysql
import os

conn = None

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
    connection = get_connection()
    
    query = event.get('query', 'SELECT NOW()')
    
    if not query.strip().lower().startswith("select"):
        return {
            "statusCode": 403,
            "body": "Only SELECT queries are allowed."
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
    except Exception as e:
        print(f"❌ Error: {e}")
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }
    
    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(result, indent=2, default=str)
    }
