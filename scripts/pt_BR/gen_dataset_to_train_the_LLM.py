import pandas as pd

def generate_cypher_query(label, relationship, numero, tipo_de_direito_do_processo):
    text_inputs = [f"Retorne os processos de {tipo_de_direito_do_processo} que se baseiam em {labelToText(label)} {numero}",
                   f"Quais processos que fazem referencia a {labelToText(label)} {numero} na área de {tipo_de_direito_do_processo}",
                   f"Me informe os processos de {tipo_de_direito_do_processo} que terão impactos com a mudança de {labelToText(label)} {numero}"]
        
    cypher_query = (
        f"MATCH (p:Processo {{tipo_de_direito_do_processo: '{tipo_de_direito_do_processo}'}})<-[:PERTENCE_AO_PROCESSO]-(dj:DecisaoJudicial)-[:{relationship}]->({label} {{{labelToText(label)}_numero: '{numero}'}}) "
        "RETURN p.numero_do_processo as Processo, p.titulo_do_processo as Título, p.tipo_de_direito_do_processo as Tipo_do_Direito"
    )

    prefix = "Create a Cypher statement to answer the following question:"

    result = []
    for text_input in text_inputs:
        result.append({'instruction': prefix + "" + text_input, 'output': cypher_query})
    
    return result

def labelToText(label: str) -> str:
    label_map = {
        "art:Artigo": "artigo",
        "par:Paragrafo": "paragrafo",
        "al:Alinea": "alinea",
        "l:Lei": "lei"
    }
    return label_map.get(label, "")

def generate_cypher_query_juiz_tipo_de_direito_do_processo(juiz_nome, tipo_de_direito_do_processo):
    text_inputs = [f"Quais leis {juiz_nome} se baseia nas suas decisões dos processos na área do {tipo_de_direito_do_processo}?",
                   f"Me informe as leis que {juiz_nome} já se baseou nos processos relativos a {tipo_de_direito_do_processo}",
                   f"Quais dispositivos legais na área do {tipo_de_direito_do_processo} {juiz_nome} referencia na maior parte das suas decisões?"]
        
    cypher_query = (
        "MATCH (j:Juiz {juiz_nome: '%s'})-[:PROFERE]->(d:DecisaoJudicial)-[:FAZ_REFERENCIA_A]->(l:Lei) "
        "MATCH (p:Processo)<-[:PERTENCE_AO_PROCESSO]-(d) "
        "WHERE (p.tipo_de_direito_do_processo = '%s') "
        "RETURN l.lei_titulo" % (juiz_nome, tipo_de_direito_do_processo)
    )

    prefix = "Create a Cypher statement to answer the following question:"

    result = []
    for text_input in text_inputs:
        result.append({'instruction': prefix + "" + text_input, 'output': cypher_query})
        #print('instruction' + text_input + " " +  'output' + prefix + "" + cypher_query)
    
    return result

def generate_cypher_query_decisoes_associadas_a_processo(numero_do_processo):
    text_inputs = [f"Quais decisões estão associadas ao processo {numero_do_processo}?",
                   f"Me informe as decisões que estão associadas ao processo {numero_do_processo}"]
        
    cypher_query = (
        f"MATCH (p:Processo {{numero_do_processo: {numero_do_processo}}})<-[:PERTENCE_AO_PROCESSO]-(dj:DecisaoJudicial) " \
        f"RETURN dj.numero_da_decisao as Decisão, p.numero_do_processo as Processo"
    )

    prefix = "Create a Cypher statement to answer the following question:"

    result = []
    for text_input in text_inputs:
        result.append({'instruction': prefix + "" + text_input, 'output': cypher_query})
        #print('instruction' + text_input + " " +  'output' + prefix + "" + cypher_query)
    
    return result

def generate_cypher_query_advogados_envolvidos_em_processo(numero_do_processo):
    text_inputs = [f"Quais advogados estão envolvidos no processo {numero_do_processo}?",
                   f"Me informe os advogados que estão envolvidos no processo {numero_do_processo}"]
        
    cypher_query = (
        f"MATCH (p:Processo {{numero_do_processo: '{numero_do_processo}'}})<-[:ENVOLVIDO_EM]-(a:Advogado) " \
        f"RETURN a.nome_advogado as Advogado, a.registro_OAB as OAB"
    )

    prefix = "Create a Cypher statement to answer the following question:"

    result = []
    for text_input in text_inputs:
        result.append({'instruction': prefix + "" + text_input, 'output': cypher_query})
        #print('instruction' + text_input + " " +  'output' + prefix + "" + cypher_query)
    
    return result

def generate_cypher_query_partes_relacionadas_ao_processo(numero_do_processo):
    text_inputs = [f"Quais partes estão relacionadas ao processo {numero_do_processo}?",
                   f"Me informe as partes que estão relacionadas ao processo {numero_do_processo}"]
        
    cypher_query = (
        f"MATCH (p:Processo {{numero_do_processo: '{numero_do_processo}'}})<-[:ENVOLVIDA_EM]-(pa:Parte) " \
        f"RETURN pa.nome_da_parte as Parte, p.numero_do_processo as Processo"
    )

    prefix = "Create a Cypher statement to answer the following question:"

    result = []
    for text_input in text_inputs:
        result.append({'instruction': prefix + "" + text_input, 'output': cypher_query})
    
    return result

def generate_cypher_query_leis_associadas_decisao_judicial_especifica(numero_da_decisao):
    text_inputs = [f"Quais leis estão associadas a esta decisão judicial {numero_da_decisao}?",
                   f"Me informe as leis que estão associadas a esta decisão judicial {numero_da_decisao}"]
    
    cypher_query = (
        f"MATCH (dj:DecisaoJudicial {{numero_da_decisao: '{numero_da_decisao}'}})-[:FAZ_REFERENCIA_A]->(l:Lei) " \
        f"RETURN dj.numero_da_decisao as Decisão, l.lei_numero as Lei, l.lei_titulo as Título"
    )

    prefix = "Create a Cypher statement to answer the following question:"

    result = []
    for text_input in text_inputs:
        result.append({'instruction': prefix + "" + text_input, 'output': cypher_query})
    
    return result

def generate_cypher_query_artigos_associados_decisao_judicial_especifica(numero_da_decisao):
    text_inputs = [f"Quais artigos estão associados a esta decisão judicial {numero_da_decisao}?",
                   f"Me informe os artigos que estão associados a esta decisão judicial {numero_da_decisao}"]
    
    cypher_query = (
        f"MATCH (dj:DecisaoJudicial {{numero_da_decisao: '{numero_da_decisao}'}})-[:FAZ_REFERENCIA_A]->(a:Artigo) " \
        f"RETURN dj.numero_da_decisao as Decisão, a.artigo_numero as Artigo"
    )

    prefix = "Create a Cypher statement to answer the following question:"

    result = []
    for text_input in text_inputs:
        result.append({'instruction': prefix + "" + text_input, 'output': cypher_query})
    
    return result

def generate_cypher_query_paragrafos_associados_decisao_judicial_especifica(numero_da_decisao):
    text_inputs = [f"Quais paragrafos estão associados a esta decisão judicial {numero_da_decisao}?",
                   f"Me informe os paragrafos estão associados a esta decisão judicial {numero_da_decisao}"]
    
    cypher_query = (
        f"MATCH (dj:DecisaoJudicial {{numero_da_decisao: '{numero_da_decisao}'}})-[:FAZ_REFERENCIA_A]->(p:Paragrafo) " \
        f"RETURN dj.numero_da_decisao as Decisão, p.paragrafo_numero as Parágrafo"
    )

    prefix = "Create a Cypher statement to answer the following question:"

    result = []
    for text_input in text_inputs:
        result.append({'instruction': prefix + "" + text_input, 'output': cypher_query})
    
    return result

def generate_cypher_query_alineas_associadas_decisao_judicial_especifica(numero_da_decisao):
    text_inputs = [f"Quais alineas estão associadas a esta decisão judicial {numero_da_decisao}?",
                   f"Me informe as alineas estão associadas a esta decisão judicial {numero_da_decisao}"]
    
    cypher_query = (
        f"MATCH (dj:DecisaoJudicial {{numero_da_decisao: '{numero_da_decisao}'}})-[:FAZ_REFERENCIA_A]->(al:Alinea) " \
        f"RETURN dj.numero_da_decisao as Decisão, al.alinea_numero as Alínea"
    )

    prefix = "Create a Cypher statement to answer the following question:"

    result = []
    for text_input in text_inputs:
        result.append({'instruction': prefix + "" + text_input, 'output': cypher_query})
    
    return result
   

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

# Generate Cypher queries for different node types
cypher_queries = []
for _, row in merged_df.iterrows():
    tipo_de_direito_do_processo = row["tipo_de_direito_do_processo"]
    
    cypher_queries.extend(generate_cypher_query("art:Artigo", "FAZ_REFERENCIA_A", str(row["artigo_numero"]), tipo_de_direito_do_processo))
    cypher_queries.extend(generate_cypher_query("par:Paragrafo", "FAZ_REFERENCIA_A", str(row["paragrafo_numero"]), tipo_de_direito_do_processo))
    cypher_queries.extend(generate_cypher_query("al:Alinea", "FAZ_REFERENCIA_A", str(row["alinea_numero"]), tipo_de_direito_do_processo))
    cypher_queries.extend(generate_cypher_query("l:Lei", "FAZ_REFERENCIA_A", str(row["lei_numero"]), tipo_de_direito_do_processo))
    cypher_queries.extend(generate_cypher_query_juiz_tipo_de_direito_do_processo(row["juiz_nome"], tipo_de_direito_do_processo))
    cypher_queries.extend(generate_cypher_query_decisoes_associadas_a_processo(str(row["numero_do_processo"])))
    cypher_queries.extend(generate_cypher_query_advogados_envolvidos_em_processo(str(row["numero_do_processo"])))
    cypher_queries.extend(generate_cypher_query_partes_relacionadas_ao_processo(str(row["numero_do_processo"])))
    cypher_queries.extend(generate_cypher_query_leis_associadas_decisao_judicial_especifica(str(row["numero_da_decisao"])))
    cypher_queries.extend(generate_cypher_query_artigos_associados_decisao_judicial_especifica(str(row["numero_da_decisao"])))
    cypher_queries.extend(generate_cypher_query_paragrafos_associados_decisao_judicial_especifica(str(row["numero_da_decisao"])))
    cypher_queries.extend(generate_cypher_query_alineas_associadas_decisao_judicial_especifica(str(row["numero_da_decisao"])))

# Create a DataFrame from the list of dictionaries
df = pd.DataFrame(cypher_queries, columns=['instruction', 'output'])

# Export the DataFrame to a CSV file
df.to_csv('result.csv', index=False)
