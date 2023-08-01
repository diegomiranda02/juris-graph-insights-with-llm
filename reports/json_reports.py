from typing import Dict
from reports.base_report import BaseJSONReport

# Import the Graph Database Api to send the queries to
from graphdb_api import Neo4JAPI

import pandas as pd

class DataFromNode4JReport(BaseJSONReport):

    def __init__(self, title:str, subtitle:str):
        super(DataFromNode4JReport, self).__init__(title, subtitle)

    def resultFromCypherQuery(self, query: str) -> None:
        # Instantiate the Neo4JAPI class
        neo4jApi = Neo4JAPI()

        # Send the query to the Neo4J Database
        result = neo4jApi.run_query(query)
        
        # Convert the dataframe to a dictionary
        result_dict = result.to_dict(orient='records')

        self.addTextData(str(query))
        self.addTableData("Result", result_dict)
    
    def generateJSONReport(self) -> Dict:
        return super().generateJSONReport()