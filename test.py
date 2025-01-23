import requests

#url = 'http://127.0.0.1:8000/kickoff/'

url = 'http://18.237.64.190:8000/kickoff/'
request = requests.get(url)
payload = {
    "Specifications": "6\" Bend Sixteenth NH CI ASTM A888 - NH-14",
    "Manufacturer_Name": "Charlotte",
    "Material_Type": "Fittings",
    "Manufacturer_Part_Number": "A-14"
}
headers = {"Content-Type": "application/json"}


# Make the GET request to the FastAPI endpoint
response = requests.get(url, headers=headers)

# Check if the response is successful
if response.status_code == 200:
    # Extract and print the Outputs from the JSON response
    outputs = response.json().get('Outputs', {})
    print("Outputs:", outputs)
else:
    print(f"Error: {response.status_code}, {response.text}")

# 18.237.64.190
# import shutil
# import os
# from dotenv import load_dotenv

# # Load environment variables from .env file
# load_dotenv()

# # Paths
# source_path = r"/mnt/c/Users/SGundu/Multi_Agents/Multi_Agents_LLM/multi-agents-cdk/.venv/lib/site-packages"
# layer_root = r"/mnt/c/Users/SGundu/Multi_Agents/Multi_Agents_LLM/multi-agents-cdk/lambda_layer"
# layer_python_path = os.path.join(layer_root, "python", "lib", "python3.11", "site-packages")
# layer_zip_path = r"/mnt/c/Users/SGundu/Multi_Agents/Multi_Agents_LLM/multi-agents-cdk/layer.zip"

# # Step 1: Create the directory structure
# if os.path.exists(layer_root):
#     print(f"Cleaning up existing directory: {layer_root}")
#     shutil.rmtree(layer_root)  # Clean up any existing layer folder

# print(f"Creating directory structure at {layer_python_path}")
# os.makedirs(layer_python_path, exist_ok=True)

# # Step 2: Check if source_path exists and copy dependencies
# if not os.path.exists(source_path):
#     raise FileNotFoundError(f"Source path not found: {source_path}. Ensure dependencies are installed.")

# print(f"Copying dependencies from {source_path} to {layer_python_path}...")
# shutil.copytree(source_path, layer_python_path, dirs_exist_ok=True)

# # Step 3: Zip the layer directory
# print(f"Zipping layer directory to {layer_zip_path}...")
# shutil.make_archive(layer_zip_path.replace(".zip", ""), 'zip', layer_root)

# print(f"Lambda layer .zip file created at {layer_zip_path}")
