## Isssue tipo Bug

A issue escolhida foi [YARN-6650](https://issues.apache.org/jira/browse/YARN-6650). Ele não apresenta um problema na versão corrente, mas sim possíveis problemas com upgrades. 

O bug é do tipo de ``security``, adicionado como prioridade ``Major``. Ela afeta a versão 2.8.0.

Ela foi reportada por [Jason Lowe](https://issues.apache.org/jira/secure/ViewProfile.jspa?name=jlowe) na data de 25 de maio de 2017. O usuário possui histórico de algumas issues nos projetos apache, o que credibiliza o problema reportado.

Para reproduzir o bug, iremos configurar um RM e um NM simples, sendo que cada um possui versões diferentes do protocolo de serialização ContainerTokenIdentifier. Isso deve causar um conflito.

A solução possível (proposta pelo autor), que os bytes recebidos via RPC precisaria ser usado para o processo de verificação, não os bytes gerados pela recodificação (o que força ter que coincidir o RM e NM).

## Plano de trabalho

* Leitura e instalação do ``Yarn``
* Estudo do bug no código
* Configuração de um RM e NM com versões conflitantes
* Verificar o conflito esperado
* Adiconar e verificar possível solução