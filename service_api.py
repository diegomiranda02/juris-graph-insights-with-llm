# fastapi libraries
from fastapi import FastAPI
from fastapi.responses import PlainTextResponse
from fastapi import Response
from fastapi.middleware.cors import CORSMiddleware

import json

# Import Model Api with the LLM
from model_api import generate_cypher

# Import the Graph Database Api to send the queries to
from graphdb_api import run_query

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
    cypher_code = cypher_code.replace("Create a Cypher statement to answer the following question:", "")

    # Send the query to the Neo4J Database
    result = run_query(cypher_code)

    print(result)
    return Response(content=json.dumps(result), media_type="application/json")

