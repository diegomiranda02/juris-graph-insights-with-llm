# juris-graph-insights-with-llm
Legal Insights through Graphs with LLM

# Introdução

No artigo "[Nome do artigo]", foram abordadas as vantagens do uso de um banco de dados orientado a grafo para análise em um escritório de advocacia. No entanto, identificou-se um obstáculo para a utilização dessa tecnologia: a necessidade de treinamento dos advogados ou responsáveis pelo levantamento dos dados para construir consultas na linguagem específica do banco de dados em grafo. Ao contrário dos bancos de dados relacionais, que possuem uma linguagem padrão (SQL), cada banco de dados em grafo utiliza sua própria linguagem, o que torna a adoção da tecnologia e a realização da análise mencionada no artigo inviáveis.
A fim de superar esse desafio, propõe-se a implementação de um algoritmo de inteligência artificial capaz de compreender consultas em português e gerar a linguagem específica do banco de dados em grafo, neste caso, a linguagem Cypher do banco Neo4J. A figura abaixo ilustra o funcionamento da solução proposta: 

![alt text](https://github.com/diegomiranda02/juris-graph-insights-with-llm/blob/main/images/exemplo_do_funcionamento_do_modelo.png?raw=true)

Com essa abordagem, espera-se facilitar o acesso à base de dados e possibilitar consultas de forma mais intuitiva e acessível para os profissionais do escritório de advocacia, eliminando a barreira da complexidade da linguagem de consulta do banco de dados em grafo. Essa solução pode representar um avanço na adoção da tecnologia e na aplicação prática das análises mencionadas no artigo.


# Ferramentas Utilizadas

Neste artigo, descreveremos as ferramentas gratuitas que foram empregadas no desenvolvimento do projeto, permitindo a construção de uma solução eficiente e acessível. Abaixo estão as principais ferramentas utilizadas:

* H2O LLM Studio para Treinar o Modelo e Fazer Upload na Hugging Face
O software H2O LLM Studio desempenhou um papel fundamental no processo de fine-tuning do modelo para tradução do português para a linguagem Cypher. O modelo específico adotado foi o da Eleuther AI (faça referência ao modelo utilizado).

* Google Colab
Para o treinamento do modelo, foi essencial o uso de uma Unidade de Processamento Gráfico (GPU). O Google Colab ofereceu uma GPU de forma gratuita, que se mostrou mais que suficiente para o treinamento necessário. Para utilizar o Google Colab, foram executados os passos utilizando a interface de linha de comando (CLI). Existem duas opções para utilizar essa interface: a primeira, seguindo o tutorial disponível em https://github.com/diegomiranda02/cli_HF_h2o_llm_studio; e a segunda, baixando o fork do projeto em https://github.com/diegomiranda02/h2o-llmstudio e seguindo o passo a passo detalhado na seção "Run H2O LLM Studio with command line interface (CLI)."

* Neo4J
Para armazenar os nós e as arestas representando a relação dos dados, utilizamos um banco de dados orientado a grafos, o Neo4J.

* Conta na Hugging Face para Disponibilizar o Modelo de Inteligência Artificial Treinado
A plataforma Hugging Face foi a escolha para disponibilizar o modelo de inteligência artificial treinado. Criamos uma conta em seu site e, por meio do software H2O LLM Studio, realizamos o upload do modelo.

* Modelo Pré-Treinado
Neste projeto, utilizamos o modelo pré-treinado "EleutherAI/pythia-70m-deduped," que pode ser encontrado no seguinte link: https://huggingface.co/EleutherAI/pythia-70m-deduped-v0.
Com o emprego dessas ferramentas gratuitas, obtivemos resultados e avançados na tradução de textos para a linguagem Cypher, representando um passo importante no desenvolvimento de soluções acessíveis e de alto desempenho na área de inteligência artificial. A utilização de recursos de código aberto e gratuito é fundamental para democratizar o acesso a tecnologias, como as apresentadas neste artigo.

# Dataset Utilizado para o Treinamento do Modelo

O treinamento do modelo se baseou em um dataset criado especificamente para esse projeto, composto por duas colunas: uma coluna de instrução e outra de saída, seguindo o exemplo abaixo:
Instrução: Create a cypher to the following command: Retorne os processos de Direito Ambiental que se baseiam na lei 939 de 1992.
Saída:

```
MATCH (p:Processo {tipo_de_direito_do_processo: 'Direito Tributário'})<-[:PERTENCE_AO_PROCESSO]-(dj:DecisaoJudicial)-[:FAZ_REFERENCIA_A]->(l:Lei {lei_numero: '939 de 1992'}) RETURN p.numero_do_processo as Processo, p.titulo_do_processo as Título, p.tipo_de_direito_do_processo as Tipo_do_Direito
```

Para o treinamento, foram utilizadas mais de 86 mil linhas de registros no formato mencionado acima.
O prefixo "Create a cypher to the following command:" foi adotado seguindo o mesmo passo a passo detalhado no artigo anterior (fornecer a referência do artigo).

# Modelo após o fine-tuning

Após o processo de fine-tuning, o modelo apresentou um bom desempenho, alcançando uma métrica BLEU de 97. Além disso, devido ao menor número de parâmetros, tornou-se possível executar o modelo treinado em uma CPU, reduzindo o uso de recursos necessários para sua execução e escalabilidade.
Link para o Modelo e Instruções para Testes: [Inserir o link para o modelo e suas respectivas instruções para testes aqui.] (Certifique-se de fornecer um link funcional que direcione os leitores para o modelo e suas instruções detalhadas)

# Implementação do Projeto

Nesta seção, apresentaremos uma solução para permitir que o usuário digite consultas em linguagem natural em uma aplicação desenvolvida em Streamlit. A consulta inserida é processada por um modelo de linguagem com fine-tuning da Eleuther AI, traduzida para a linguagem Cypher e, em seguida, utilizada para consultar um banco de dados em grafo Neo4j. Os resultados são automaticamente renderizados em formato JSON e visualizados de forma intuitiva na interface do usuário. A figura abaixo mostra as etapas do processo desde a consulta feita pelo usuário até o resultado mostrado na interface:

![alt text](https://github.com/diegomiranda02/juris-graph-insights-with-llm/blob/main/images/fluxo_traducao_portugues_cypher.png?raw=true)

* Etapa 1: A interface de consulta em linguagem natural desenvolvida no ambiente Streamlit permite que os usuários insiram suas consultas de forma intuitiva. Ao utilizar a aplicação, o usuário tem a liberdade de digitar perguntas em linguagem natural, como por exemplo: "Me informe as leis que o juiz 3 já se baseou nos processos relativos a Direito do Consumidor". A partir desse ponto, a consulta é submetida a um processo de processamento e encaminhada para a próxima etapa do fluxo de execução.

```python
command = st.text_input("O que deseja?", "Me informe as leis que juiz 3 já se baseou nos processos relativos a Direito do Consumidor", disabled=False)
```

Nesta linha, é criado um campo de entrada de texto usando a função text_input do Streamlit. Esse campo permite que o usuário digite sua consulta em linguagem natural. O primeiro argumento da função é o rótulo ou instrução que aparecerá ao lado do campo de entrada. O segundo argumento é o texto padrão que aparecerá no campo de entrada, caso o usuário não digite nada. O parâmetro disabled é definido como False, o que significa que o campo não estará desativado para edição pelo usuário.

```python
if st.button("Enviar"):
```

Nesta linha, é criado um botão "Enviar" usando a função button do Streamlit. Esse botão será usado para enviar a consulta digitada pelo usuário.

```python
with st.spinner('Consulta em andamento...'):
```

Aqui, é utilizada a função spinner do Streamlit para exibir uma animação de carregamento (um spinner) enquanto a consulta está sendo processada. Isso fornece uma resposta visual ao usuário de que a consulta está em andamento.

* Etapa 2: Tradução Automática com o Modelo de Linguagem
Uma aplicação em Python recebe a consulta em linguagem natural e a encaminha para um modelo treinado com fine-tuning da Eleuther AI. Esse modelo tem a função de traduzir a consulta para a linguagem Cypher, adicionando o prefixo "Create a cypher statement to the following command". A consulta em Cypher gerada é enviada para a próxima etapa.

Este código utiliza a biblioteca PyTorch e a biblioteca Hugging Face Transformers para criar um modelo de geração de linguagem capaz de traduzir consultas em linguagem natural para a linguagem Cypher, que é uma linguagem de consulta usada em bancos de dados em grafo, como o Neo4j. Vamos explicar cada parte do código:

```python
device = "cuda:0" if torch.cuda.is_available() else "cpu"
```

Nesta linha, é verificado se há uma GPU (unidade de processamento gráfico) disponível usando a função torch.cuda.is_available(). Se uma GPU estiver disponível, o dispositivo é definido como "cuda:0", caso contrário, é definido como "cpu". Essa definição é importante para determinar onde o modelo será executado, se na GPU ou na CPU.

```python
tokenizer = AutoTokenizer.from_pretrained("diegomiranda/eleuther_70m_cypher_generator")
```

Nesta linha, é carregado um tokenizador pré-treinado da Hugging Face para o modelo "diegomiranda/eleuther_70m_cypher_generator". O tokenizador é responsável por transformar o texto em tokens que o modelo pode entender.

```python
model = AutoModelForCausalLM.from_pretrained("diegomiranda/eleuther_70m_cypher_generator").to(device)
```

Aqui, o modelo pré-treinado "diegomiranda/eleuther_70m_cypher_generator" é carregado da Hugging Face e colocado no dispositivo definido anteriormente (GPU ou CPU) usando o método .to(device).

```python
prefix = "\nCreate a Cypher statement to answer the following question:"
```

O código define um prefixo que será adicionado à consulta em linguagem natural antes de ser traduzida para Cypher.

```python
def generate_cypher(prompt): ...
```

Esta função chamada generate_cypher recebe como entrada um texto de "prompt", que representa a consulta em linguagem natural que o usuário deseja traduzir para Cypher.

```python
inputs = tokenizer(f"{prefix}{prompt}", return_tensors="pt", add_special_tokens=False).to(device)
```

O texto de "prompt" é pré-processado pelo tokenizador, incluindo o prefixo definido anteriormente. Os tokens são convertidos em tensores PyTorch e movidos para o dispositivo definido.

```python
tokens = model.generate(**inputs, max_new_tokens=256, temperature=0.0, repetition_penalty=1.0, num_beams=4)[0]
```

O modelo de geração de linguagem é usado para traduzir o texto em tokens para a linguagem Cypher. Os parâmetros como max_new_tokens, temperature, repetition_penalty e num_beams controlam a geração dos tokens.

```python
tokens = tokens[inputs["input_ids"].shape[1]:]
```

Os tokens resultantes são extraídos, excluindo os tokens adicionados pelo tokenizador.

```python
result_test = tokenizer.decode(tokens, skip_special_tokens=True)
```

Os tokens são decodificados de volta para texto usando o tokenizador, excluindo os tokens especiais adicionados durante o processamento.

```python
return result_test
```

A função retorna a tradução final em linguagem Cypher como texto.

* Etapa 3: Consulta no Banco de Dados Neo4j
O código em Python, com a consulta em linguagem Cypher, é utilizado para consultar o banco de dados em grafo Neo4j. O banco de dados contém os nós e as arestas representando os processos judiciais e suas relações, permitindo consultas eficientes com base na linguagem Cypher.

Este trecho de código estabelece uma conexão com um banco de dados Neo4j, executa consultas no banco de dados e retorna os resultados em formato de tabela (DataFrame) usando a biblioteca Pandas. A função _run_query executa a consulta no banco de dados, e a função run_query chama a função anterior e retorna o resultado em formato tabular para análise e manipulação dos dados.

```python
# Establish a connection to the Neo4j database
uri = "bolt://localhost:7687"  # Replace with your Neo4j server URI
username = "neo4j"  # Replace with your Neo4j username
password = "12345678"  # Replace with your Neo4j password

driver = GraphDatabase.driver(uri, auth=(username, password))

def _run_query(query: str):
    result = None
    with driver.session() as session:
        result = session.run(query)
        records = result.data()
    # Close the database connection
    driver.close()

    return records

def run_query(query: str) -> pd.DataFrame:
    result = _run_query(query)
    df = pd.DataFrame.from_dict(result)
    
    return df
```

* Etapa 4: Retorno da Consulta em Cypher
O modelo de linguagem retorna a consulta traduzida na linguagem Cypher para a aplicação desenvolvida em Python.

* Etapa 5: Consulta dos Dados e Geração do JSON
A aplicação em Python utiliza a consulta em Cypher para consultar o banco de dados Neo4j. Os dados obtidos são estruturados em formato JSON para facilitar o processamento e a visualização na interface do usuário.

O objetivo deste código é criar uma classe chamada DataFromNode4JReport, que herda de uma classe chamada BaseJSONReport. A classe DataFromNode4JReport é projetada para receber um DataFrame resultante de uma consulta no banco de dados Neo4j e gerar um JSON no formato específico que facilita a renderização automática da interface do usuário em uma aplicação Streamlit.

Vamos explicar o que cada parte do código faz:

```python
def __init__(self, title:str, subtitle:str):
```

O método __init__ é o construtor da classe DataFromNode4JReport. Ele recebe como parâmetros title e subtitle, que são usados para definir o título e o subtítulo do relatório.

```python
super(DataFromNode4JReport, self).__init__(title, subtitle)
```

Na linha acima, o construtor da classe pai (BaseJSONReport) é chamado usando a função super(). Isso é feito para inicializar as propriedades da classe pai e garantir que a classe filha (DataFromNode4JReport) herde suas funcionalidades.

```python
def resultFromCypherQuery(self, query: str) -> None:
```

Este método, chamado resultFromCypherQuery, é responsável por receber a consulta em linguagem Cypher (query) e executá-la no banco de dados Neo4j. O resultado da consulta é convertido em um dicionário e armazenado internamente para ser usado na geração do JSON.

```python
result = run_query(query)
```

A função run_query é chamada para executar a consulta no banco de dados Neo4j e o resultado é armazenado na variável result.

```python
result_dict = result.to_dict(orient='records')
```

O resultado da consulta (que é um DataFrame) é convertido em um dicionário usando o método to_dict, com orientação 'records'. Essa orientação resulta em um dicionário onde cada registro do DataFrame se torna um item na lista de dicionários.

```python
self.addTextData(str(query))
```

A consulta original em linguagem Cypher é adicionada ao relatório usando o método addTextData, para que o usuário possa visualizar a consulta que foi executada.

```python
self.addTableData("Result", result_dict)
```

Os dados resultantes da consulta em forma de dicionário são adicionados ao relatório como uma tabela, usando o método addTableData.

```python
def generateJSONReport(self) -> Dict:
```

Este método, chamado generateJSONReport, é responsável por gerar o JSON final do relatório. Ele retorna o resultado gerado a partir da chamada do método generateJSONReport da classe pai (BaseJSONReport), que foi herdado.

A classe DataFromNode4JReport é projetada para receber consultas em linguagem Cypher, executá-las no banco de dados Neo4j, converter o resultado em um formato de dicionário e gerar um JSON que representa o relatório. Esse JSON específico é concebido para ser facilmente renderizado automaticamente pela interface do usuário em Streamlit, proporcionando uma visualização clara e organizada dos dados obtidos no banco de dados Neo4j.

* Etapa 6: Visualização Automática na Interface do Usuário
Os resultados em formato JSON são enviados para a interface do usuário, onde são automaticamente estruturados utilizando a classe BaseReport e a classe DataFromNode4JReport. Essa padronização possibilita a visualização dos dados de forma clara e intuitiva.

Neste trecho de código, a função get_data recebe uma consulta em linguagem natural, converte-a para uma consulta em linguagem Cypher, executa a consulta no banco de dados Neo4j e gera um JSON com os dados obtidos. O JSON é preparado para ser exibido na interface do usuário, facilitando a visualização dos resultados da consulta do banco de dados.

```python
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
```

* Etapa 7: Geração Automática do Relatório
Na etapa final, o método generate_report no arquivo app.py recebe como parâmetro o JSON com os dados gerados na etapa anterior. Esse método renderiza automaticamente o relatório, proporcionando ao usuário uma visão completa e organizada dos resultados obtidos a partir da consulta em linguagem natural.

Este trecho de código recebe um JSON no formato especificado com a classe BaseReport e renderiza cada componente na biblioteca Streamlit automaticamente.

Ele percorre as chaves e valores do JSON, identifica o tipo de cada componente (tabela, título, subtítulo, texto ou gráfico de barras) e utiliza a biblioteca Streamlit para exibir cada componente na interface do usuário.

Se a chave começa com "table" e o valor é uma lista, o código exibe uma tabela usando a função st.table do Streamlit.
Se a chave começa com "title" ou "subtitle" e o valor é uma string, o código exibe um título ou subtítulo formatado gradualmente na interface.
Se o valor é uma string, o código exibe o texto formatado gradualmente na interface.
Se a chave começa com "barchart" e o valor é um dicionário, o código converte os dados em um DataFrame e exibe um gráfico de barras usando st.bar_chart.
Esse código automatiza o processo de exibição dos componentes do relatório, permitindo que o usuário visualize os dados e informações de forma organizada e interativa na interface do Streamlit.

```python
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
```

Benefícios da Solução
Com essa solução, os usuários podem interagir com o banco de dados Neo4j através de consultas em linguagem natural, sem a necessidade de conhecimento específico da linguagem Cypher. A tradução automática e a visualização dos resultados simplificam o processo de obtenção de informações importantes para o negócio e possibilitam a exploração de dados de forma mais acessível e prática. A aplicação desenvolvida em Streamlit oferece uma experiência intuitiva, tornando a interação com o banco de dados em grafo Neo4j uma tarefa simplificada.
