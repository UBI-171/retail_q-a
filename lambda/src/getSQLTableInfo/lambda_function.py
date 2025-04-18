import json
import pymysql
import os

conn = None

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
    connection = get_connection()
    table_info = {}
    
    try:
        with connection.cursor() as cursor:
            cursor.execute("SHOW TABLES;")
            tables = [row["Tables_in_{}".format(os.environ['DB_NAME'])] for row in cursor.fetchall()]
            print("📋 Found tables:", tables)
            for table in tables:
                cursor.execute(f"DESCRIBE `{table}`;")
                columns = cursor.fetchall()
                table_info[table] = columns
            return {
            "statusCode": 200,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps(table_info, indent=2, default=str)
            }
    except Exception as e:
        print(f"❌ Error: {type(e).__name__} - {str(e)}")
        return {
            "statusCode": 500,
            "body": json.dumps({"error": f"{type(e).__name__} - {str(e)}"})
        }
