# mard

API em FastAPI para gerenciar uma livraria online com SQLAlchemy 2 e PostgreSql.

## Requisitos

- Python 3.14+
- [Poetry](https://python-poetry.org/) 
- Docker (ou Podman) com Compose

## Primeiros passos

```bash

poetry install

cp .env.example .env

poetry run poe db-up

poetry run poe migrate

poetry run poe serve
```

## Banco de dados

O `docker-compose.yml` sobe um PostgreSQL 17 na porta 5432

- `mard` — desenvolvimento
- `mard_test` — container de testes (criado por `docker/postgres/init.sql`)

As URLs ficam no `.env`:

```dotenv
DATABASE_URL=postgresql+asyncpg://mard:mard@localhost:5432/mard
TEST_DATABASE_URL=postgresql+asyncpg://mard:mard@localhost:5432/mard_test
```

As credenciais são apenas para desenvolvimento local.

```bash
poetry run poe migration "cria tabela users"
poetry run poe migrate
```

### Testes

Os testes usam o banco `mard_test` e criam/derrubam o schema da `Base`
automaticamente a cada sessão de testes. Suba o banco antes de rodar:

```bash
poetry run poe db-up
poetry run poe test
```
