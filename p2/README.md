## Tema

Extensão do projeto 1 (análise de sentimento de tweets que tratam certos tópicos) fazendo uso do Sparks e da API oficial do Twitter a fim de por-se a prova o poderio do cluster analisando quantidades massivas de tweets.

## Implementação

* Sparks para escalar a análise de sentimentos
* Lib *Tweepy* para interagir com a API do Twitter e baixar tweets mencionando tópicos como *racism, immigration, homo-affective union*
* Libs em Python para remoção de stopwords, stemming e análise propriamente dita
* Ferramenta em Python para plotar gráficos apresentando os resultados (Usuário definirá time frames, região e potencialmente outros parâmetros)

## Plano de trabalho

* @gbuenoandrade - Tweetpy e Spark
* @felipefutty - Melhora da interface e Spark
* @danilomendes12 - Melhora dos scores e Spark

## Testes iniciais / PoC

* [Experimento com Spark e Python](http://www.ic.unicamp.br/~islene/2s2017-mc855/explorando-spark.html)
* [Introduction to Apache Spark on Databricks](https://docs.databricks.com/_static/notebooks/gentle-introduction-to-apache-spark.html)

## Apresentação de Resultados

Os resultados serão mostrados graficamente de acordo com dois parâmetros: timeframe e tópicos.
 
### Timeframe

Escolha de um período de tweets para que sejam analisado. Dessa forma, pode-se verificar como o sentimento tem variado ao longo do tempo. 