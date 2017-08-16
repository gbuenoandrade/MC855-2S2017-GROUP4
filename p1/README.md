## Ideia

Analisar a postura da sociedade com relação a tópicos conservadores a fim de se validar/refutar a tese de que estes estão em alta através de análise de sentimento de tweets.

## Implementação

* Lib *Tweepy* para interagir com a API do Twitter e baixar tweets mencionando tópicos como *racism, immigration, homo-affective union*
* Hadoop MapReduce para escalar a análise de sentimentos
* Libs em Python para remoção de stopwords, stemming e análise propriamente dita
* Ferramenta em Python para plotar gráficos apresentando os resultados (Usuário definirá time frames, região e potencialmente outros parâmetros)

## Plano de trabalho
* @gbuenoandrade - Tweetpy, Hadoop e análise de sentimentos
* @felipefutty - Hadoop e análise de sentimentos
* @danilomendes12 - Pré-processamento e ferramenta para plotar gráficos


## Apresentação de Resultados

Os resultados serão mostrados graficamente de acordo com dois parâmetros: timeframe e região. Além disso, para cada parâmetro selecionado produziremos o word cloud equivalente.
 
### Timeframe

Escolha de um período de tweets para que sejam analisado. Dessa forma, pode-se verificar como o sentimento tem variado ao longo do tempo. 

### Região

Possibilitará a escolha de algumas macro-regiões, as quais serão comparadas para que possa visualizar como cada região se comporta em relação ao tópico analisado.
