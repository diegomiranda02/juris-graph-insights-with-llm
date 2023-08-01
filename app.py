# streamlit library
import streamlit as st

# Import Model Api with the LLM
from model_api import generate_cypher

# Import the report JSON generator
from reports.json_reports import DataFromNode4JReport

st. set_page_config(layout="wide") 

import time

from typing import Dict

# JSON to render the API responde into a Python Object
import json

# Pandas
import pandas as pd

# Numpy
import numpy as np

def get_data(report_name: str, query: str):

    data = None

    # Generate the cypher code from the query
    cypher_code = generate_cypher(query)
    
    # Replace the first part of the query
    cypher_code = cypher_code.replace("Create a Cypher statement to answer the following question:", "")

    dataFromNode4JReportTitle = "Relatório de Consultas em Linguagem Natural"
    dataFromNode4JReportSubtitle = "Dados consultados diretamente do Neo4J"
    dataFromNeo4JReport = DataFromNode4JReport(dataFromNode4JReportTitle, dataFromNode4JReportSubtitle)
    dataFromNeo4JReport.resultFromCypherQuery(cypher_code)
    data = dataFromNeo4JReport.generateJSONReport()

    return json.loads(data)

def generate_report(data_content):
    for key,value in data_content.items():
        if key.startswith("table") and isinstance(value, list):
            st.table(pd.DataFrame(value))

        elif key.startswith("title") and isinstance(value, str):
            # Print text Streamlit
            t = st.empty()
            for i in range(len(value) + 1):
                t.header("%s" % value[0:i])
                time.sleep(0.02)
            #st.header(value)
    
        elif key.startswith("subtitle") and isinstance(value, str):
            # Print text Streamlit
            t = st.empty()
            for i in range(len(value) + 1):
                t.header("%s" % value[0:i])
                time.sleep(0.02)
            #st.header(value)

        elif isinstance(value, str):
            # Print text Streamlit
            t = st.empty()
            for i in range(len(value) + 1):
                t.text("%s" % value[0:i])
                time.sleep(0.02)
        
        elif key.startswith("barchart") and isinstance(value, Dict):
            # Converting list to Dataframe
            chart_data = pd.DataFrame.from_dict(value, orient='tight')
            st.bar_chart(chart_data)


command = st.text_input("O que deseja?", "Me informe as leis que juiz 3 já se baseou nos processos relativos a Direito do Consumidor", disabled=False)

# check if the Send button was pressed and get the API Data
# This code was based on the code presented in the 'Técnicas Avançadas de NLP (Natural Language Processing)' course by Professor Giuliano Ferreira 
# on the Stack Academy website
if st.button("Enviar"):        
    with st.spinner('Consulta em andamento...'):
        # Starting generating the report
        report_name = 'Data from Neo4J Report'
        data_content = get_data(report_name, query=command)
        generate_report(data_content)



