# Análise de Dados na Área Jurídica com a Utilização de Gráficos e LLM

## Introdução

No artigo [Análise de Dados em Grafo com Python na Área do Direito](https://medium.com/p/8eeafbc14601), foram abordadas as vantagens do uso de um banco de dados orientado a grafo para análise em um escritório de advocacia. No entanto, identificou-se um obstáculo para a utilização dessa tecnologia: a necessidade de treinamento dos advogados ou responsáveis pelo levantamento dos dados para construir consultas na linguagem específica do banco de dados em grafo. Ao contrário dos bancos de dados relacionais, que possuem uma linguagem padrão (SQL), cada banco de dados em grafo utiliza sua própria linguagem, o que torna a adoção da tecnologia e a realização da análise mencionada no artigo inviáveis.
A fim de superar esse desafio, propõe-se a implementação de um algoritmo de inteligência artificial capaz de compreender consultas em português e gerar a linguagem específica do banco de dados em grafo, neste caso, a linguagem Cypher do banco Neo4J. A figura abaixo ilustra o funcionamento da solução proposta: 

![alt text](https://github.com/diegomiranda02/juris-graph-insights-with-llm/blob/main/images/exemplo_do_funcionamento_do_modelo.png?raw=true)

Com essa abordagem, espera-se facilitar o acesso à base de dados e possibilitar consultas de forma mais intuitiva e acessível para os profissionais do escritório de advocacia, eliminando a barreira da complexidade da linguagem de consulta do banco de dados em grafo. Essa solução pode representar um avanço na adoção da tecnologia e na aplicação prática das análises mencionadas no artigo.


## Ferramentas Utilizadas

Neste artigo, descreveremos as ferramentas gratuitas que foram empregadas no desenvolvimento do projeto, permitindo a construção de uma solução eficiente e acessível. Abaixo estão as principais ferramentas utilizadas:

* **H2O LLM Studio para treinar o modelo e fazer upload na Hugging Face:**
O software H2O LLM Studio desempenhou um papel fundamental no processo de fine-tuning do modelo para tradução do português para a linguagem Cypher. O modelo específico adotado foi o da [Eleuther AI](https://huggingface.co/EleutherAI).

* **Google Colab:**
Para o treinamento do modelo, foi essencial o uso de uma Unidade de Processamento Gráfico (GPU). O Google Colab ofereceu uma GPU de forma gratuita, que se mostrou mais que suficiente para o treinamento necessário. Para utilizar o Google Colab, foram executados os passos utilizando a interface de linha de comando (CLI). Para utilizar a interface CLI acesse o link https://github.com/h2oai/h2o-llmstudio.git e execute o passo a passo detalhado na seção "Run H2O LLM Studio with command line interface (CLI)". A H2O disponibiliza o seguinte tutorial como exemplo https://colab.research.google.com/drive/1-OYccyTvmfa3r7cAquw8sioFFPJcn4R9?usp=sharing.

* **Neo4J:**
A escolha para armazenar os nós e as arestas representando a relação dos dados foi o banco de dados orientado a grafos Neo4J.

* **Conta na Hugging Face para disponibilizar o modelo de Inteligência Artificial treinado:**
A plataforma Hugging Face foi a escolha para disponibilizar o modelo de inteligência artificial treinado. Foi criada uma conta no site e, por meio do software H2O LLM Studio, foi realizado o upload do modelo.

* **Modelo Pré-Treinado:**
Neste projeto, foi utilizado o modelo pré-treinado "EleutherAI/pythia-70m-deduped," que pode ser encontrado no seguinte link https://huggingface.co/EleutherAI/pythia-70m-deduped-v0.

Com o emprego dessas ferramentas gratuitas, foram obtidos resultados relevantes na tradução de textos para a linguagem Cypher, tornando possível o desenvolvimento de soluções acessíveis e de baixo custo na área de inteligência artificial. A utilização de recursos de código aberto e gratuito é fundamental para democratizar o acesso a tecnologias, como as apresentadas neste artigo.

# Dataset Utilizado para o Treinamento do Modelo

O treinamento do modelo se baseou em um dataset criado especificamente para esse projeto, composto por duas colunas: uma coluna de instrução e outra de saída, seguindo o exemplo abaixo:
Instrução: Create a cypher to the following command: Retorne os processos de Direito Ambiental que se baseiam na lei 939 de 1992.
Saída:

```
MATCH (p:Processo {tipo_de_direito_do_processo: 'Direito Tributário'})<-[:PERTENCE_AO_PROCESSO]-(dj:DecisaoJudicial)-[:FAZ_REFERENCIA_A]->(l:Lei {lei_numero: '939 de 1992'})
RETURN p.numero_do_processo as Processo, p.titulo_do_processo as Título, p.tipo_de_direito_do_processo as Tipo_do_Direito
```

Para o treinamento, foram utilizadas mais de 86 mil linhas de registros no formato mencionado acima.
O prefixo "Create a cypher to the following command:" foi adotado seguindo o mesmo passo a passo detalhado no artigo [Fine-tuning an LLM model with H2O LLM Studio to generate Cypher statements](https://towardsdatascience.com/fine-tuning-an-llm-model-with-h2o-llm-studio-to-generate-cypher-statements-3f34822ad5).

Para gerar o dataset utilizado neste projeto para o processo de fine tuning do algoritmo BERT, execute o seguinte comando:

```python
python scripts/pt_BR/gen_dataset_to_train_the_LLM.py
```

O dataset será gerado em um arquivo .csv com o nome 'result.csv'.

## Modelo após o fine-tuning

Após o processo de fine-tuning, o modelo apresentou um bom desempenho, alcançando uma métrica BLEU de 97. Além disso, devido ao menor número de parâmetros, tornou-se possível executar o modelo treinado em uma CPU, reduzindo o uso de recursos necessários para sua execução e escalabilidade.
Link para o Modelo e Instruções para Testes: [diegomiranda/text-to-cypher](https://huggingface.co/diegomiranda/text-to-cypher) 

## Implementação do Projeto

Nesta seção, descreve-se a solução para permitir que o usuário digite consultas em linguagem natural em uma aplicação desenvolvida em Streamlit. A consulta inserida é processada por um modelo de linguagem com fine-tuning da Eleuther AI, traduzida para a linguagem Cypher e, em seguida, utilizada para consultar um banco de dados em grafo Neo4j. Os resultados são automaticamente renderizados em formato JSON e visualizados de forma intuitiva na interface do usuário. A figura abaixo mostra as etapas do processo desde a consulta feita pelo usuário até o resultado mostrado na interface:

![alt text](https://github.com/diegomiranda02/juris-graph-insights-with-llm/blob/main/images/fluxo_traducao_portugues_cypher.png?raw=true)

## Interface de Consulta em Linguagem Natural

A implementação começa com a criação de uma interface de consulta em linguagem natural, desenvolvida no ambiente Streamlit, que permite que os usuários insiram suas consultas de maneira intuitiva. Através dessa aplicação, os usuários têm a liberdade de digitar perguntas em linguagem natural, por exemplo: "Quais processos que fazem referência à lei 939 de 1992 na área de Direito do Consumidor?". 

```python
command = st.text_input("O que deseja?", "Quais processos que fazem referência à lei 939 de 1992 na área de Direito do Consumidor?", disabled=False)

if st.button("Enviar"):
    with st.spinner('Consulta em andamento...'):
        # Processamento da consulta e geração dos resultados

```

Neste trecho de código, um campo de entrada de texto é criado usando a função text_input do Streamlit. Isso permite que o usuário digite sua consulta em linguagem natural. Um botão "Enviar" é criado usando a função button do Streamlit para permitir ao usuário enviar a consulta. Durante o processamento da consulta, uma animação de carregamento é exibida utilizando a função spinner do Streamlit para fornecer feedback visual de que a consulta está sendo processada.

## Tradução Automática com o Modelo de Linguagem

  Em seguida, utilizamos um modelo de linguagem da Eleuther AI após um processo de fine-tuning para realizar a tradução automática da consulta em linguagem natural para a linguagem Cypher. Isso é necessário para que a consulta possa ser executada em um banco de dados Neo4j baseado em grafo. Aqui está o código para executar o modelo:

```python
def generate_response(prompt, model_name):
    tokenizer = AutoTokenizer.from_pretrained(
        model_name,
        use_fast=True,
        trust_remote_code=True,
    )
    
    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        torch_dtype=torch.float32,
        device_map={"": "cpu"},
        trust_remote_code=True,
    )
    model.cpu().eval()
    
    inputs = tokenizer(prompt, return_tensors="pt", add_special_tokens=False).to("cpu")
    
    tokens = model.generate(
        input_ids=inputs["input_ids"],
        attention_mask=inputs["attention_mask"],
        min_new_tokens=2,
        max_new_tokens=500,
        do_sample=False,
        num_beams=2,
        temperature=float(0.0),
        repetition_penalty=float(1.0),
        renormalize_logits=True
    )[0]
    
    tokens = tokens[inputs["input_ids"].shape[1]:]
    answer = tokenizer.decode(tokens, skip_special_tokens=True)
    
    return answer
```

A função retorna a tradução final em linguagem Cypher como texto.

```python
model_name = "diegomiranda/EleutherAI-70M-cypher-generator"
prompt = "Create a Cypher statement to answer the following question:Retorne os processos de Direito Tributário que se baseiam em lei 939 de 1992?<|endoftext|>"
response = generate_response(prompt, model_name)
print(response)
```

## Consulta no Banco de Dados Neo4j
O código em Python, com a consulta em linguagem Cypher, é utilizado para consultar o banco de dados em grafo Neo4j. O banco de dados contém os nós e as arestas representando os processos judiciais e suas relações, permitindo consultas eficientes com base na linguagem Cypher.

Este trecho de código estabelece uma conexão com um banco de dados Neo4j, executa consultas no banco de dados e retorna os resultados em formato de tabela (DataFrame) usando a biblioteca Pandas. 

```python
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
```

## Consulta dos Dados e Geração do JSON
O objetivo deste código é criar uma classe chamada DataFromNode4JReport, que herda de uma classe chamada BaseJSONReport (ver artigo [Automating Business Reports Visualization with Streamlit](https://medium.com/@diego.miranda02/automating-business-reports-visualization-with-streamlit-c44e92d6b281). A classe DataFromNode4JReport é projetada para receber um DataFrame resultante de uma consulta no banco de dados Neo4j e gerar um JSON no formato específico que facilita a renderização automática da interface do usuário em uma aplicação Streamlit. 


```python
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
```

Este método, chamado generateJSONReport, é responsável por gerar o JSON final do relatório. Ele retorna o resultado gerado a partir da chamada do método generateJSONReport da classe pai (BaseJSONReport), que foi herdado.

A classe DataFromNode4JReport é projetada para receber consultas em linguagem Cypher, executá-las no banco de dados Neo4j, converter o resultado em um formato de dicionário e gerar um JSON que representa o relatório. Esse JSON específico é concebido para ser facilmente renderizado automaticamente pela interface do usuário em Streamlit, proporcionando uma visualização clara e organizada dos dados obtidos no banco de dados Neo4j.

# Geração dos resultados em formato JSON padronizado
Os resultados em formato JSON são enviados para a interface do usuário, onde são automaticamente estruturados utilizando a classe BaseReport e a classe DataFromNode4JReport. Essa padronização possibilita a visualização dos dados de forma clara e intuitiva.

Neste trecho de código, a função get_data recebe uma consulta em linguagem natural, converte-a para uma consulta em linguagem Cypher, executa a consulta no banco de dados Neo4j e gera um JSON com os dados obtidos. 

```python
def get_data(report_name: str, query: str):

    data = None

    # Generate the cypher code from the query
    cypher_code = generate_cypher(query)

    dataFromNode4JReportTitle = "Relatório de Consultas em Linguagem Natural"
    dataFromNode4JReportSubtitle = "Dados consultados diretamente do Neo4J"
    dataFromNeo4JReport = DataFromNode4JReport(dataFromNode4JReportTitle, dataFromNode4JReportSubtitle)
    dataFromNeo4JReport.resultFromCypherQuery(cypher_code)
    data = dataFromNeo4JReport.generateJSONReport()

    return json.loads(data)
```

## Geração Automática do Relatório
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

## Benefícios da Solução
Com essa solução, os usuários podem interagir com o banco de dados Neo4j através de consultas em linguagem natural, sem a necessidade de conhecimento específico da linguagem Cypher. A tradução automática e a visualização dos resultados simplificam o processo de obtenção de informações importantes para o negócio e possibilitam a exploração de dados de forma mais acessível e prática. A aplicação desenvolvida em Streamlit oferece uma experiência intuitiva, tornando a interação com o banco de dados em grafo Neo4j uma tarefa simplificada.

## Preparação do ambiente de desenvolvimento

1. Instalar Docker: Visite o site oficial (https://docs.docker.com/get-docker/) e siga as instruções para instalar o Docker no seu sistema.

2. Instalar Neo4J com Docker: Visite o site oficial (https://neo4j.com/docs/operations-manual/current/docker/introduction/#docker-image) e siga as instruções para instalar o servidor de banco de dados em grafo Neo4J com Docker.

3. Instalar Git: Instalar o Git do site oficial (https://git-scm.com/downloads).

4. Anaconda: Instalar o software Anaconda do site oficial (https://www.anaconda.com/download).

5. Clone o projeto do repositório do GitHub:

- Abra um terminal ou prompt de comando
- Mude o diretório para o qual você clonou o projeto.
- Execute o seguinte comando para clonar o projeto:

``` 
git clone https://github.com/diegomiranda02/juris-graph-insights-with-llm.git
```
Uma vez que o download foi finalizado, mude para o diretório do projeto:

```
cd <diretorio_do_projeto>
```

6. Crie um ambiente para executar o projeto com o seguinte comando:

```bash
conda create -f config/environment.yaml
conda activate cypher_llm_env
```

7. Acesse o servidor do banco de dados Neo4J acessando http://localhost:7474/ para verificar se a instalação está correta.

8. Modificar a senha do banco no seguinte trecho dos scripts 'insert_data.py' e 'delete_data.py'

```
username = MUDAR_LOGIN  # Substitua pelo seu nome de usuário Neo4j
password = MUDAR_SENHA  # Substitua pela sua senha do Neo4j
```

9. Gerar os dados do banco:

```python
python cypher_python/pt_BR/insert_data.py
```

10. Para deletar os dados do banco execute o seguindo comando:

```python
python cypher_python/pt_BR/delete_data.py
```

Há três formas para executar a aplicação: via linha de comando, através do aplicativo web desenvolvido com Streamlit ou iniciando um serviço REST.

1. Pela linha de comando, execute o seguinte comando:

```python
python service_api_CONSOLE.py
```

2. Através do aplicativo web desenvolvido com Streamlit, execute o seguinte comando:

```python
streamlit run app.py
```

3. Iniciando um serviço REST:

```python
uvicorn service_api:app
```
Acesse http://127.0.0.1:8000/llm_api?query="Retorne os processos de Direito Tributário que se baseiam na lei 939 de 1992". 

Abaixo um vídeo demonstrando a execução da aplicação: 

[Execução da aplicação](https://github.com/diegomiranda02/juris-graph-insights-with-llm/blob/main/video/aplicacao_em_streamlit.mp4?raw=true)

## Conclusão

A proposta de implementar um algoritmo de inteligência artificial capaz de compreender consultas em português e gerar a linguagem específica do banco de dados em grafo, como o Cypher do Neo4J, é uma solução promissora para a adoção da solução em escritórios de advocacia.

Ao empregar ferramentas gratuitas, como o H2O LLM Studio, Google Colab, Neo4J e a plataforma Hugging Face, o projeto demonstra que é possível desenvolver uma solução eficiente e acessível para simplificar o acesso aos dados e permitir consultas mais intuitivas na área do Direito. O uso de um modelo pré-treinado da Eleuther AI e a disponibilização do modelo na Hugging Face mostram como a colaboração e o compartilhamento de recursos podem impulsionar a inovação.

Além disso, a ênfase na utilização de recursos de código aberto e gratuito ressalta a importância de democratizar o acesso à tecnologia e promover a aplicação prática de análises de dados em grafos no campo jurídico. Essa abordagem pode representar um avanço na eficiência e na capacidade de análise das informações em escritórios de advocacia, eliminando barreiras de complexidade e tornando a tecnologia mais acessível a todos os profissionais da área.
