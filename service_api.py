# fastapi libraries
from fastapi import FastAPI
from fastapi.responses import PlainTextResponse
from fastapi import Response
from fastapi.middleware.cors import CORSMiddleware

import json

# Import Model Api with the LLM
from model_api import generate_cypher

# Import the report JSON generator
from reports.json_reports import DataFromNode4JReport

# Instantiate the API
app = FastAPI()

# Decide who can access te API
origins = [
    "http://localhost",
    "http://localhost:8501"
]

# Insert the access permissions in the API
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Check if the API is Alive
@app.get("/", response_class=PlainTextResponse)
async def root():
    return "API is Alive"

# Return a result for a specific query
@app.get("/llm_api", response_class=PlainTextResponse)
async def query(query: str):
   
    # Generate the cypher code from the query
    cypher_code = generate_cypher(query)

    
    dataFromNode4JReportTitle = "Data from Neo4J Report"
    dataFromNode4JReportSubtitle = "Consulta executada no banco: " + cypher_code
    dataFromNeo4JReport = DataFromNode4JReport(dataFromNode4JReportTitle, dataFromNode4JReportSubtitle)
    dataFromNeo4JReport.resultFromCypherQuery(cypher_code)
    data = dataFromNeo4JReport.generateJSONReport()
    print(data)

    return Response(content=json.dumps(data), media_type="application/json")

