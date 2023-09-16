from neo4j import GraphDatabase
import pandas as pd
import random
import numpy as np
import ast

# Establish a connection to the Neo4j database
uri = "bolt://localhost:7687"  # Replace with your Neo4j server URI
username = "neo4j"  # Replace with your Neo4j username
password = "12345678"  # Replace with your Neo4j password

driver = GraphDatabase.driver(uri, auth=(username, password))

def create_node(node_label, node_type, node_properties):
    #Connect to the database and create a session
    with driver.session() as session:
        session.execute_write(_create_node, node_label, node_type, node_properties)

########################################################################
# Private method to create the query and execute the transaction
########################################################################

def _create_node(tx, 
                 node_label, 
                 node_type, 
                 node_properties):

    # The properties of the node in a dictionary format
    properties_string = ', '.join(f'{key}: ${key}' for key in node_properties.keys())
    # Create the query to execute
    query = f"CREATE ({node_label}:{node_type} {{{properties_string}}})"
    # Assign the parameters
    parameters = {**node_properties}
    # Run the query
    tx.run(query, **parameters)


######################################################
# Define a function to create a relationship
######################################################

def create_relationship(from_node_id, 
                        relationship_type, 
                        to_node_id, 
                        direction="UNIDIRECTIONAL", 
                        relationship_properties=None):
    
    with driver.session() as session:
        session.execute_write(_create_relationship, 
                              from_node_id, 
                              relationship_type, 
                              to_node_id, direction, 
                              relationship_properties)
    
######################################################
# Private method to create the query and execute the transaction
######################################################
def _create_relationship(tx, 
                         from_node_id, 
                         relationship_type, 
                         to_node_id, 
                         direction, 
                         relationship_properties):
    
    if direction == "BIDIRECTIONAL":
        relationship_clause = "<-[r:%s]->" % relationship_type
    else:
        relationship_clause = "-[r:%s]->" % relationship_type

    properties_clause = ""
    if relationship_properties:
        relationship_properties = ast.literal_eval(relationship_properties)
        properties_clause = " SET r += $properties"

    query = (
        "MATCH (from {id: '%s'}), (to {id: '%s'}) "
        "CREATE (from)%s(to)%s"
    ) % (from_node_id, 
         to_node_id, 
         relationship_clause, 
         properties_clause)

    parameters = {
        "properties": relationship_properties,
    }

    print(query)

    tx.run(query, **parameters)

###################################################################################
# Using list comprehension to load the data in Neo4J
###################################################################################

# Loading Decisoes Judiciais
def load_decisoes(dataframe):
    [create_node("decisaoJudicial" + str(row["decisao_id"]), "DecisaoJudicial", 
                 {"id": "decisaoJudicial" + str(row["decisao_id"]), 
                  "numero_da_decisao": row["numero_da_decisao"], 
                  "resumo_da_decisao": row["resumo_da_decisao"], 
                  "conteudo_da_decisao": row["conteudo_da_decisao"]}) 
                  for _, row in dataframe.iterrows()]

# Loading Processos
def load_processos(dataframe):
    [create_node("processo" +  str(row["processo_id"]), "Processo", 
                 {"id": "processo" +  str(row["processo_id"]), 
                  "numero_do_processo": row["numero_do_processo"], 
                  "titulo_do_processo": row["titulo_do_processo"], 
                  "tipo_de_direito_do_processo": row["tipo_de_direito_do_processo"]}) 
                  for _, row in dataframe.iterrows()]

# Loading Advogados
def load_advogados(dataframe):
    [create_node("advogado" +  str(row["registro_OAB"]), "Advogado", 
                 {"id": "advogado" +  str(row["registro_OAB"]), 
                  "registro_OAB": row["registro_OAB"], 
                  "nome_advogado": row["nome_advogado"]}) 
                  for _, row in dataframe.iterrows()]

# Loading Partes
def load_partes(dataframe):
    [create_node("parte" +  str(row["documento_parte"]), "Parte", 
                 {"id": "parte" +  str(row["documento_parte"]), 
                  "documento_parte": row["documento_parte"], 
                  "tipo_documento_parte": row["tipo_documento_parte"], 
                  "tipo_parte": row["tipo_parte"], 
                  "nome_da_parte": row["nome_da_parte"], 
                  "endereco_da_parte": row["endereco_da_parte"]}) 
                  for _, row in dataframe.iterrows()]

# Loading Juizes
def load_juizes(dataframe):
    [create_node("juiz" + str(row["juiz_cpf"]), "Juiz", 
                 {"id": "juiz" + str(row["juiz_id"]), 
                  "juiz_nome": row["juiz_nome"], 
                  "juiz_cpf": row["juiz_cpf"], 
                  "juiz_tribunal": row["juiz_tribunal"]}) 
                  for _, row in dataframe.iterrows()]

# Loading Leis
def load_leis(dataframe):
    [create_node("lei" +  str(row["lei_id"]), "Lei", 
                 {"id": "lei" +  str(row["lei_id"]), 
                  "lei_numero": row["lei_numero"], 
                  "lei_titulo": row["lei_titulo"]}) 
                  for _, row in dataframe.iterrows()]

# Loading Artigos
def load_artigos(dataframe):
    [create_node("artigo" +  str(row["artigo_id"]), "Artigo", 
                 {"id": "artigo" +  str(row["artigo_id"]), 
                  "artigo_numero": row["artigo_numero"], 
                  "artigo_conteudo": row["artigo_conteudo"]}) 
                  for _, row in dataframe.iterrows()]

# Loading Paragrafos
def load_paragrafos(dataframe):
    [create_node("paragrafo" +  str(row["paragrafo_id"]), "Paragrafo", 
                 {"id": "paragrafo" +  str(row["paragrafo_id"]), 
                  "paragrafo_numero": row["paragrafo_numero"], 
                  "paragrafo_conteudo": row["paragrafo_conteudo"]}) 
                  for _, row in dataframe.iterrows()]

# Loading Alineas
def load_alineas(dataframe):
    [create_node("alinea" +  str(row["alinea_id"]), "Alinea", 
                 {"id": "alinea" +  str(row["alinea_id"]), 
                  "alinea_numero": row["alinea_numero"], 
                  "alinea_conteudo": row["alinea_conteudo"]}) 
                  for _, row in dataframe.iterrows()]

########################################################
# Read data files
########################################################

DATA_DIR = './data/'

def load_data(file_name, load_function):
    df = pd.read_csv(DATA_DIR + file_name)
    load_function(df)

load_data("decisoes.csv", load_decisoes)
load_data("processos.csv", load_processos)
load_data("advogados.csv", load_advogados)
load_data("partes.csv", load_partes)
load_data("juizes.csv", load_juizes)
load_data("leis.csv", load_leis)
load_data("artigos.csv", load_artigos)
load_data("paragrafos.csv", load_paragrafos)
load_data("alineas.csv", load_alineas)

###############################################################
# RELATIONSHIPS
###############################################################

# Read data from CSV files
alineas_df = pd.read_csv('data/alineas.csv')
paragrafos_df = pd.read_csv('data/paragrafos.csv')
artigos_df = pd.read_csv('data/artigos.csv')
leis_df = pd.read_csv('data/leis.csv')
decisoes_df = pd.read_csv('data/decisoes.csv')
processos_df = pd.read_csv('data/processos.csv')
juizes_df = pd.read_csv('data/juizes.csv')

# Merge DataFrames based on the relationships
merged_df = (
    decisoes_df 
    .merge(processos_df, on='processo_id')
    .merge(juizes_df, on='juiz_id')
    .merge(leis_df, on='lei_id')
    .merge(artigos_df, on='lei_id')
    .merge(paragrafos_df, on='artigo_id')
    .merge(alineas_df, on='paragrafo_id')
)

relationships = set()
for _, row in merged_df.iterrows():
    relationships.add(('juiz'+str(row['juiz_id']), "PROFERE", 'decisaoJudicial'+str(row['decisao_id']),"",""))
    relationships.add(("decisaoJudicial"+str(row['decisao_id']), "FAZ_REFERENCIA_A", 'lei'+str(row['lei_id']), "", "{'qtd_referencias': 2}"))
    relationships.add(("decisaoJudicial"+str(row['decisao_id']), "FAZ_REFERENCIA_A", 'artigo'+str(row['artigo_id']), "", "{'qtd_referencias': 3}"))
    relationships.add(("decisaoJudicial"+str(row['decisao_id']), "FAZ_REFERENCIA_A", 'paragrafo'+str(row['paragrafo_id']), "", "{'qtd_referencias': 1}"))
    relationships.add(("decisaoJudicial"+str(row['decisao_id']), "FAZ_REFERENCIA_A", 'alinea'+str(row['alinea_id']), "", "{'qtd_referencias': 5}"))
    relationships.add(("decisaoJudicial"+str(row['decisao_id']), "PERTENCE_AO_PROCESSO", 'processo'+str(row['processo_id']), "", ""))
    relationships.add(('lei'+str(row['lei_id']), "POSSUI_ARTIGO", "artigo"+str(row['artigo_id']),"",""))
    relationships.add(('lei'+str(row['lei_id']), "POSSUI_PARAGRAFO", 'paragrafo'+str(row['paragrafo_id']),"",""))
    relationships.add(('lei'+str(row['lei_id']), "POSSUI_ALINEA", 'alinea'+str(row['alinea_id']),"",""))
    relationships.add(('advogado'+str(row['registro_OAB']), "ENVOLVIDO_EM", 'processo'+str(row['processo_id']),"",""))
    relationships.add(('parte'+str(row['documento_parte']), "ENVOLVIDA_EM", 'processo'+str(row['processo_id']),"",""))


for row in relationships:
    create_relationship(row[0], row[1], row[2], row[3] if row[3] is not None else "", row[4] if row[4] is not None else "")