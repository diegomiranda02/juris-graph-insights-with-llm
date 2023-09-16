# Import the report JSON generator
from reports.json_reports import DataFromNode4JReport

# Import Model Api with the LLM
from model_api import generate_cypher

query = "Me informe as leis que juiz 3 já se baseou nos processos relativos a Direito do Consumidor"

# Generate the cypher code from the query
cypher_code = generate_cypher(query)

print(cypher_code)

dataFromNode4JReportTitle = "Data from Neo4J Report"
dataFromNode4JReportSubtitle = "Consulta executada no banco: " + cypher_code
dataFromNeo4JReport = DataFromNode4JReport(dataFromNode4JReportTitle, dataFromNode4JReportSubtitle)
dataFromNeo4JReport.resultFromCypherQuery(cypher_code)
data = dataFromNeo4JReport.generateJSONReport()
print(data)