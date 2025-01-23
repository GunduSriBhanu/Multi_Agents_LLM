from pydantic import BaseModel
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security.api_key import APIKeyHeader
from typing import Optional
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = FastAPI()

# Define the API key authorization
# AUTHORIZED_API_KEYS = ["key1", "key2", "key3"]  # Replace with a list of secure API keys for employees
# API_KEY_NAME = "Authorization"
# api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=True)

# def verify_api_key(api_key: str = Depends(api_key_header)):
#     if api_key not in AUTHORIZED_API_KEYS:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Invalid API Key",
#         )

def validate_environment_keys():
    openai_api_key = os.getenv("OPENAI_API_KEY")
    tavily_api_key = os.getenv("TAVILY_API_KEY")

    if not openai_api_key or not tavily_api_key:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Environment keys for OpenAI and Tavily are missing. Please set OPENAI_API_KEY and TAVILY_API_KEY.",
        )
    
    # You can add actual validation logic for the keys here if needed (e.g., testing their validity)
    return True

# Validate keys before starting the application
validate_environment_keys()

class SubmittalInputs(BaseModel):
    Manufacturer_Name: str
    Specifications: str
    Material_Type: str
    Manufacturer_Part_Number: str

class SubmittalOutputs(BaseModel):
    Specification: str
    Material_Type: str
    Manufacturer_Name: str
    Existing_Manufacturer_Part_Number: str
    Verification_Completed: bool
    Verified_Manufacturer_Part_Number: str
    Link: str
    Confidence_Score: str
    Human_Verification: bool
    Feedback: str

# Global variables to store the latest inputs and outputs
latest_inputs: Optional[dict] = None
latest_result: Optional[dict] = None

@app.post("/kickoff/")
async def kickoff_crew_endpoint(inputs: SubmittalInputs):
    # Map Python-style keys to exact keys expected by kickoff_crew
    inputs_dict = {
        "Manufacturer Name": inputs.Manufacturer_Name,
        "Specifications": inputs.Specifications,
        "Material Type": inputs.Material_Type,
        "Manufacturer Part Number": inputs.Manufacturer_Part_Number,
    }
    
    # Simulate the result returned from kickoff_crew (replace with actual function call)
    result = kickoff_crew(inputs_dict)
    
    # Store the inputs and outputs globally
    global latest_inputs, latest_result
    latest_inputs = inputs_dict
    latest_result = {
        "Specification": result['specifications'],
        "Material_Type": result['material_name'],
        "Manufacturer_Name": result['manufacturer_name'],
        "Existing_Manufacturer_Part_Number": result['manufacturer_part_number'],
        "Verification_Completed": result['is_verification_done'],
        "Verified_Manufacturer_Part_Number": result['verified_manufacturer_part_number'],
        "Link": result['link'],
        "Confidence_Score": str(result['confidence_score']),
        "Human_Verification": result['human_verification_needed'],
        "Feedback": result['feedback'],
    }
    return {"Inputs": latest_inputs}

@app.get("/kickoff/", dependencies=[Depends(verify_api_key)])
async def get_last_result():
    if latest_result is None or latest_inputs is None:
        return {"message": "No results available. Please make a POST request to /kickoff/ first."}
    return {"Inputs": latest_inputs, "Outputs": latest_result}

@app.get("/favicon.ico")
async def favicon():
    return None