# Import the report JSON generator
from reports.json_reports import DataFromNode4JReport

# Import Model Api with the LLM
from model_api import generate_cypher


# command = "Gere um relatorio financeiro do mes de abril e no ano de 2023"
query = "Quais leis o juiz 2 se baseia nas suas decisões dos processos na área do Direito Tributário?"

# Generate the cypher code from the query
cypher_code = generate_cypher(query)
        
# Replace the first part of the query
cypher_code = cypher_code.replace("Create a Cypher statement to answer the following question:", "")


dataFromNode4JReportTitle = "Data from Neo4J Report"
dataFromNode4JReportSubtitle = "Consulta executada no banco: " + cypher_code
dataFromNeo4JReport = DataFromNode4JReport(dataFromNode4JReportTitle, dataFromNode4JReportSubtitle)
dataFromNeo4JReport.resultFromCypherQuery(cypher_code)
data = dataFromNeo4JReport.generateJSONReport()
print(data)