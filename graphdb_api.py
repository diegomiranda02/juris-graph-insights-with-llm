from neo4j import GraphDatabase
import pandas as pd

class Neo4jConnector:
    def __init__(self, uri, username, password):
        self.uri = uri
        self.username = username
        self.password = password
        self.driver = None

    def connect(self):
        self.driver = GraphDatabase.driver(self.uri, auth=(self.username, self.password))

    def disconnect(self):
        if self.driver:
            self.driver.close()

    def _run_query(self, query):
        result = None
        with self.driver.session() as session:
            result = session.run(query)
            records = result.data()
        return records

    def run_query(self, query) -> pd.DataFrame:
        result = self._run_query(query)
        df = pd.DataFrame.from_dict(result)
        return df
    
class Neo4JAPI:
    def __init__(self):
        # The URI, username, and password can be retrieved from system variables or securely stored in a configuration file.
        # In this example, we are directly passing the values for demonstration purposes.
        self.connector = Neo4jConnector("bolt://localhost:7687", "neo4j", "12345678")

    def run_query(self, query) -> pd.DataFrame:
        self.connector.connect()
        result = self.connector.run_query(query)
        self.connector.disconnect()
        return result
