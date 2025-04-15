import boto3
from botocore.exceptions import ClientError, NoCredentialsError
import logging
import json
from utils.prompt import construct_prompt
from fastapi import HTTPException
from dotenv import load_dotenv
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

def get_sql_query(question):
    aws_region = os.environ["AWS_REGION"]
    bedrock = boto3.client("bedrock-runtime", region_name = aws_region)
    model_id = os.environ["MODEL_ID"]
    
    prompt = construct_prompt(question)
    
    formatted_prompt = f"""
    <|begin_of_text|><|start_header_id|>user<|end_header_id|>
    {prompt}
    <|eot_id|>
    <|start_header_id|>assistant<|end_header_id|>
    """
    
    native_request = {
    "prompt": formatted_prompt,
    "max_gen_len": 512,
    "temperature": 0.1,
    }
    
    request = json.dumps(native_request)
    
    try:
        response = bedrock.invoke_model(modelId=model_id, body=request)
        model_response = json.loads(response["body"].read())
        response_text = model_response["generation"]
        return response_text
    except (ClientError, Exception, NoCredentialsError) as e:
        print(f"ERROR: Can't invoke '{model_id}'. Reason: {e}")
        if NoCredentialsError:
            raise HTTPException(
                status_code = 401,
                detail="Wrong AWS Credentials"
            )
        else:
            raise HTTPException(
                status_code = 500,
                detail = f"{e}"
            )