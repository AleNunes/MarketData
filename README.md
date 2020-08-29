# GS_Tech
 Desafio

## Solução dividida em duas partes.

1 - A Primeira é a disponilização de um API, onde serão calculados os retornos e demais métricas do fundo.
- app.py: Arquivo principal que disponibiliza a API e consulta as outras classes.
- cdi.py: Classe para consultar a serie histórica do CDI e retornar calculos e fatores
- fundo.py: Classe que irá consultar o Histórico de cotas e retornar os calculos solicitados no desafio.
- funcions.py: Arquivo com funções uteis para as demais classes

2 - A segunda parte é o Notebook que servirá como interface para consultar a API
Optei por utilizar o jupyter notebook como interface, para facilitar a construção de gráficos para comparação com Benchmark ou outros ativos.

TODO (pessoal)

- Alterar API para generalizar e consultar histórico de Cotas de outros fundos 555 da CVM.
- Alterar API para consultar o fundo pelo CNPJ.
- Adicionar Ibov, Ptax, IHFA
- Adicionar calculos de vol
- add Max drawdown
