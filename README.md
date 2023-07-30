# juris-graph-insights-with-llm
Legal Insights through Graphs with LLM

# Introdução

No artigo intitulado "[Nome do artigo]", foram abordadas as vantagens do uso de um banco de dados orientado a grafo para análise em um escritório de advocacia. No entanto, identificou-se um obstáculo significativo para a utilização dessa tecnologia: a necessidade de treinamento dos advogados ou responsáveis para construir consultas na linguagem específica do banco de dados em grafo. Ao contrário dos bancos de dados relacionais, que possuem uma linguagem padrão (SQL), cada banco de dados em grafo utiliza sua própria linguagem, o que torna a adoção da tecnologia e a realização da análise mencionada no artigo inviáveis.
A fim de superar esse desafio, propõe-se a implementação de um algoritmo de inteligência artificial capaz de compreender consultas em português e gerar a linguagem específica do banco de dados em grafo, neste caso, a linguagem Cypher do banco Neo4J. A figura abaixo ilustra o funcionamento da solução proposta: [Inserir a figura que ilustra o funcionamento da solução].
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
