# Projeto Lotofácil API

Este projeto fornece uma API para analisar e gerar combinações para a Lotofácil.

## Instalação

1. Clone o repositório
2. Instale as dependências usando `pip install -r requirements.txt`
3. Execute o servidor usando `uvicorn combination:combination --reload`

## Endpoints

- `GET /get_combinations`: Gera e retorna as 10 melhores combinações.

## Modelos

O projeto utiliza um modelo de regressão linear treinado com estatísticas da Lotofácil.

## Banco de Dados

A API se conecta a um banco de dados PostgreSQL, cujas credenciais e configurações devem ser definidas no código.

## Contribuições

Contribuições são bem-vindas! Por favor, abra uma issue ou pull request.

## Licença

[MIT](LICENSE)
