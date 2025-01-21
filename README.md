# Multi_Agents_LLM
Used different types of Multi agents LLM for Generative AI on AWS cloud services

## Creating Multi Agents and integrating with LLMs on AWS cloud services
### AWS Cloud services: 
AWS EC2, S3, SageMaker, Amazon Textract, AWS Lambda

### LLM Models: 
Open AI, Gemini, LLama, Groq

### Multi Agents: 
LangGraph, LLama Graphs Multiagents, Crew AI, AgenticAI

### Embeddings: 
Open AI Embeddings, Hugging Face Embeddings.

### Computer Vision Models: 
OCR, Tesseract OCR, PymuPDF, PyPDF, Yolo Models

### DataBases: 
Neo4j, MongoDB, AWS S3

### CI/CD: 
GitHuB, Docker, AWS Cloudformation

### API Integration: 
FastAPi, RestAPI

### Logs: 
AgentOps, Open Telemetry

FastAPI: uvicorn main:app --reload
"http://127.0.0.1:8000/docs"

CDK: mkdir multi-agents-cdk
cd multi-agents-cdk
cdk init app --language python
source .venv/bin/activate # On Windows, run `.\venv\Scripts\activate` instead
python -m pip install -r requirements.txt


Docker: 
docker build -t fastapi-app 
docker run -d -p 8000:8000 fastapi-app
docker ps
docker stop fastapi-app
docker stop $(docker ps -q)

