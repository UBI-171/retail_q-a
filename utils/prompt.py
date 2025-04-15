from utils.few_shot_examples import few_shots
from utils.table_metadata import get_table_info

def construct_prompt(question):
    table_info : dict = get_table_info()
    mysql_prompt = f"""
    You are a MySQL expert. Given an input question, create a syntactically correct MySQL query to run.
    You can order the results to return the most informative data in the database.
    Never query for all columns from a table. You must query only the columns that are needed to answer the question.
    Pay attention to use only the column names you can see in the tables below. Be careful to not query for columns that do not exist. 
    Also, pay attention to which column is in which table.
    Pay attention to use CURDATE() function to get the current date, if the question involves "today".

    Return just the query as a response.

    No pre-amble.

    Here is my table structure in the database :
    
    {table_info}
    
    Here are a few examples for you:
    
    {few_shots}
    
    Here is my question:
    
    Question : {question}
    
    """
    
    return mysql_prompt