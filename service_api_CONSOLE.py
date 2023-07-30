# Import the report JSON generator
from reports.json_reports import DataFromNode4JReport

# Import Model Api with the LLM
from model_api import generate_cypher


#query = "Quais leis o juiz juiz 3 se baseia nas suas decisões dos processos na área do Direito do Consumidor?"
#query = "Me informe as leis que juiz 3 já se baseou nos processos relativos a Direito do Consumidor"
query = "Quais dispositivos legais na área do Direito do Consumidor juiz 3 referencia na maior parte das suas decisões?"
#query = "Quais leis o juiz 2 se baseia nas suas decisões dos processos na área do Direito Tributário?"

# Generate the cypher code from the query
cypher_code = generate_cypher(query)
        
# Replace the first part of the query
cypher_code = cypher_code.replace("Create a Cypher statement to answer the following question:", "")

print(cypher_code)


dataFromNode4JReportTitle = "Data from Neo4J Report"
dataFromNode4JReportSubtitle = "Consulta executada no banco: " + cypher_code
dataFromNeo4JReport = DataFromNode4JReport(dataFromNode4JReportTitle, dataFromNode4JReportSubtitle)
dataFromNeo4JReport.resultFromCypherQuery(cypher_code)
data = dataFromNeo4JReport.generateJSONReport()
print(data)