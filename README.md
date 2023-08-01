# juris-graph-insights-with-llm
Legal Insights through Graphs with LLM

# Introdução

No artigo intitulado "[Nome do artigo]", foram abordadas as vantagens do uso de um banco de dados orientado a grafo para análise em um escritório de advocacia. No entanto, identificou-se um obstáculo significativo para a utilização dessa tecnologia: a necessidade de treinamento dos advogados ou responsáveis para construir consultas na linguagem específica do banco de dados em grafo. Ao contrário dos bancos de dados relacionais, que possuem uma linguagem padrão (SQL), cada banco de dados em grafo utiliza sua própria linguagem, o que torna a adoção da tecnologia e a realização da análise mencionada no artigo inviáveis.
A fim de superar esse desafio, propõe-se a implementação de um algoritmo de inteligência artificial capaz de compreender consultas em português e gerar a linguagem específica do banco de dados em grafo, neste caso, a linguagem Cypher do banco Neo4J. A figura abaixo ilustra o funcionamento da solução proposta: 

![alt text](https://github.com/diegomiranda02/juris-graph-insights-with-llm/blob/main/images/exemplo_do_funcionamento_do_modelo.png?raw=true)

Com essa abordagem inovadora, espera-se facilitar o acesso à base de dados e possibilitar consultas de forma mais intuitiva e acessível para os profissionais do escritório de advocacia, eliminando a barreira da complexidade da linguagem de consulta do banco de dados em grafo. Essa solução pode representar um avanço significativo na adoção da tecnologia e na aplicação prática das análises mencionadas no artigo.


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
Com o emprego dessas ferramentas gratuitas, obtivemos resultados promissores e avançados na tradução de textos para a linguagem Cypher, representando um passo importante no desenvolvimento de soluções acessíveis e de alto desempenho na área de inteligência artificial. A utilização de recursos de código aberto e gratuito é fundamental para democratizar o acesso a tecnologias inovadoras, como as apresentadas neste artigo.

# Dataset Utilizado para o Treinamento do Modelo

O treinamento do modelo se baseou em um dataset especialmente criado, composto por duas colunas: uma coluna de instrução e outra de saída, seguindo o exemplo abaixo:
Instrução: Create a cypher to the following command: Retorne os processos de Direito Ambiental que se baseiam na lei 10.350.
Saída:

```
MATCH (p:Processo {tipo_de_direito: 'Direito Ambiental'})<-[:PERTENCE_AO_PROCESSO]-(dj:DecisaoJudicial)-[:BASEIA_SE]->(lei {numero: '10.350'})
MATCH (adv:Advogado)-[:ENVOLVIDO_EM]->(p)
RETURN p.numero as Número, p.titulo as Título, p.tipo_de_direito as Tipo_do_Direito
```

Para o treinamento, foram utilizadas mais de 86 mil linhas de registros no formato mencionado acima.
O prefixo "Create a cypher to the following command:" foi adotado seguindo o mesmo passo a passo detalhado no artigo anterior (fornecer a referência do artigo).

# Modelo após o fine-tuning

Após o processo de fine-tuning, o modelo apresentou um desempenho notável, alcançando uma métrica BLEU de 97. Além disso, devido ao menor número de parâmetros, tornou-se possível executar o modelo treinado em uma CPU, reduzindo o uso de recursos necessários para sua execução e escalabilidade.
Link para o Modelo e Instruções para Testes: [Inserir o link para o modelo e suas respectivas instruções para testes aqui.] (Certifique-se de fornecer um link funcional que direcione os leitores para o modelo e suas instruções detalhadas)
Com o dataset customizado e o modelo otimizado, esse projeto representa um avanço significativo no desenvolvimento de soluções de processamento de linguagem natural, demonstrando como o uso inteligente de dados e tecnologias acessíveis pode impulsionar o campo da inteligência artificial.

# Implementação do Projeto

Nesta seção, apresentaremos uma solução completa para permitir que o usuário digite consultas em linguagem natural em uma aplicação desenvolvida em Streamlit. A consulta inserida é processada por um modelo de linguagem com fine-tuning da Eleuther AI, traduzida para a linguagem Cypher e, em seguida, utilizada para consultar um banco de dados em grafo Neo4j. Os resultados são automaticamente renderizados em formato JSON e visualizados de forma intuitiva na interface do usuário. A figura abaixo mostra as etapas do processo desde a consulta feita pelo usuário até o resultado mostrado na interface:

![alt text](https://github.com/diegomiranda02/juris-graph-insights-with-llm/blob/main/images/fluxo_traducao_portugues_cypher.png?raw=true)

* Etapa 1: Interface de Consulta em Linguagem Natural
Na aplicação Streamlit, criamos uma interface amigável onde o usuário pode inserir suas consultas em linguagem natural. Por exemplo, o usuário pode digitar a seguinte frase: "Me informe as leis que o juiz 3 já se baseou nos processos relativos a Direito do Consumidor". Essa consulta será processada e encaminhada para a próxima etapa.

* Etapa 2: Tradução Automática com o Modelo de Linguagem
Uma aplicação em Python recebe a consulta em linguagem natural e a encaminha para um modelo treinado com fine-tuning da Eleuther AI. Esse modelo tem a função de traduzir a consulta para a linguagem Cypher, adicionando o prefixo "Create a cypher statement to the following command". A consulta em Cypher gerada é enviada para a próxima etapa.

* Etapa 3: Consulta no Banco de Dados Neo4j
O código em Python, com a consulta em linguagem Cypher, é utilizado para consultar o banco de dados em grafo Neo4j. O banco de dados contém os nós e as arestas representando os processos judiciais e suas relações, permitindo consultas eficientes com base na linguagem Cypher.

* Etapa 4: Retorno da Consulta em Cypher
O modelo de linguagem retorna a consulta traduzida na linguagem Cypher para a aplicação desenvolvida em Python.

* Etapa 5: Consulta dos Dados e Geração do JSON
A aplicação em Python utiliza a consulta em Cypher para consultar o banco de dados Neo4j. Os dados obtidos são estruturados em formato JSON para facilitar o processamento e a visualização na interface do usuário.

* Etapa 6: Visualização Automática na Interface do Usuário
Os resultados em formato JSON são enviados para a interface do usuário, onde são automaticamente renderizados utilizando a classe BaseReport e a classe DataFromNode4JReport. Essa renderização possibilita a visualização dos dados de forma clara e intuitiva.

* Etapa 7: Geração Automática do Relatório
Na etapa final, o método generate_report no arquivo app.py recebe como parâmetro o JSON com os dados gerados na etapa anterior. Esse método renderiza automaticamente o relatório, proporcionando ao usuário uma visão completa e organizada dos resultados obtidos a partir da consulta em linguagem natural.

Benefícios da Solução
Com essa solução completa, os usuários podem interagir com o banco de dados Neo4j através de consultas em linguagem natural, sem a necessidade de conhecimento específico da linguagem Cypher. A tradução automática e a visualização dos resultados simplificam o processo de obtenção de informações valiosas e possibilitam a exploração de dados de forma mais acessível e eficiente. A aplicação desenvolvida em Streamlit oferece uma experiência amigável e intuitiva, tornando a interação com o banco de dados em grafo Neo4j uma tarefa simplificada e agradável.
