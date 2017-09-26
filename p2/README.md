##Notebook
* [P2_shared](https://databricks-prod-cloudfront.cloud.databricks.com/public/4027ec902e239c93eaaa8714f173bcfc/5192146202502476/1360120709539235/3726768190525689/latest.html)

## Tema

Extensão do projeto 1 (análise de sentimento de tweets que tratam certos tópicos) fazendo uso do Sparks e da API oficial do Twitter a fim de por-se a prova o poderio do cluster analisando quantidades massivas de tweets.

## Implementação

* Sparks para escalar a análise de sentimentos
* Lib *Tweepy* para interagir com a API do Twitter e baixar tweets mencionando tópicos como *racism, immigration, homo-affective union*
* Libs em Python para remoção de stopwords, stemming e análise propriamente dita
* Ferramenta em Python para plotar gráficos apresentando os resultados (Usuário definirá time frames, região e potencialmente outros parâmetros)

## Plano de trabalho

* @gbuenoandrade - Melhoramentos na  base de dados e estudo/implementação do Spark
* @felipefutty - Melhoramento na base de dados e treinamenento e adicionar processamento no projeto distribuído
* @danilomendes12 - Melhoramentos no Pré-processamento e ferramenta para plotar gráficos

## Testes iniciais / PoC
* Leitura e instalação do ``Spark`` **DONE**
* [Experimento com Spark e Python](http://www.ic.unicamp.br/~islene/2s2017-mc855/explorando-spark.html)
* [Introduction to Apache Spark on Databricks](https://docs.databricks.com/_static/notebooks/gentle-introduction-to-apache-spark.html)
* Reimplementação do projeto 1 em ``Spark``
* Melhoramento da base de dados de trainemento
* Implementação em um cluster com máquinas dos integrantes do grupo
* Comparação de resultados com o obtido no ``Hadoop```

## Apresentação de Resultados

Os resultados serão mostrados graficamente de acordo com dois parâmetros: timeframe e tópicos.
 
### Timeframe

Escolha de um período de tweets para que sejam analisado. Dessa forma, pode-se verificar como o sentimento tem variado ao longo do tempo. 