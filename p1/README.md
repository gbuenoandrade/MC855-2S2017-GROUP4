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
* @danilomendes - Pré-processamento e ferramenta para plotar gráficos
* @zorba - Pré-processamento e ferramenta para plotar gráficos
