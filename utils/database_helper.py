from sqlalchemy import Engine, QueuePool, create_engine, MetaData, text
from dotenv import load_dotenv
import os

load_dotenv()

async def get_db_engine() -> Engine:
    db_user = os.environ["DB_USER"]
    db_password = os.environ["DB_PASSWORD"]
    db_host = os.environ["DB_HOST"]
    db_port = os.environ.get("DB_PORT", "3306")
    db_name = os.environ["DB_NAME"]

    db_url = f"mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
    
    engine = create_engine(
        url=db_url,
        poolclass=QueuePool,
        pool_size=10,
        max_overflow=20,
        pool_timeout=30,
        pool_recycle=1800
    )
    return engine

async def get_table_info():
    engine = await get_db_engine()
    metadata = MetaData()
    metadata.reflect(bind=engine)
    table_info = metadata.tables.items()
    return table_info

async def execute_sql_query(query : str):
    print(query)
    engine = await get_db_engine()
    with engine.connect() as connection:
        result = connection.execute(text(query))
        rows = result.fetchall()
        return [dict(row._mapping) for row in rows]