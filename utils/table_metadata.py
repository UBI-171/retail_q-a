from sqlalchemy import create_engine, MetaData
from dotenv import load_dotenv
import os

load_dotenv()

def get_table_info():
    db_user = os.environ["DB_USER"]
    db_password = os.environ["DB_PASSWORD"]
    db_host = os.environ["DB_HOST"]
    db_port = os.environ["DB_PORT"]
    db_name = os.environ["DB_NAME"]
    db_url = f"mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
    engine = create_engine(url=db_url)
    metadata = MetaData()
    metadata.reflect(bind=engine)
    table_info = metadata.tables.items()
    
    # Iterate through all tables
    # for table_name, table in metadata.tables.items():
    #     print(f"Table: {table_name}")
    #     for column in table.columns:
    #         print(f"  Column: {column.name}, Type: {column.type}, Nullable: {column.nullable}")
    
    return table_info

