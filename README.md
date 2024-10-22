
<div align="center">

[![MockyEnd Application](https://github.com/MockyEnd/mockyend-server/actions/workflows/run-mockyend-tests.yml/badge.svg)](https://github.com/MockyEnd/mockyend-server/actions/workflows/run-mockyend-tests.yml)
[![codecov](https://codecov.io/gh/MockyEnd/mockyend-server/graph/badge.svg?token=UI2IWPX7YK)](https://codecov.io/gh/MockyEnd/mockyend-server)

</div>



# MockyEnd

> MockyEnd é uma aplicação que visa facilitar a criação e gerenciamento de endpoints mockados para testes de API. 
> Ele permite que desenvolvedores criem rapidamente respostas mockadas para endpoints HTTP, 
> ideal para ambientes de desenvolvimento e testes.

## Tecnologias Usadas

- Python 3.11
- FastAPI
- Docker
- Poetry

## Como Rodar a Aplicação

1. Clone o repositório e instale as dependências necessárias:
   ```sh
   git clone https://github.com/MockyEnd/mockyend-server.git
   cd mockyend-server
   poetry install
   ```

2. Configure as variáveis de ambiente necessárias, como detalhes de conexão com o banco de dados, se aplicável.

3. Inicie o servidor (local):
   ```sh
   poetry run uvicorn app.main:app --host localhost --port 8009 --reload
   ```

## Execução dos Testes Unitários

1. Certifique-se de ter todas as dependências de teste instaladas:
   ```sh
   TODO
   ```

2. Executando os testes:
   ```sh
   pytest
   ```
   
   Rodando os teste com geração do relatório de cobertura
   ```sh
   pytest --cov=app --cov-report=term-missing
   ```
   