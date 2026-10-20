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
- `mard_test` — criado por `docker/postgres/init.sql` (não é usado pelos
  testes, que sobem um banco efêmero via Testcontainers)

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

Os testes sobem um PostgreSQL efêmero com
[Testcontainers](https://testcontainers-python.readthedocs.io/) (imagem
`postgres:17-alpine`) e criam/derrubam o schema a cada teste. Não é preciso
subir o `docker compose` antes.

Pré-requisito: Docker ou Podman com o socket ativo. No Podman rootless:

```bash
systemctl --user enable --now podman.socket
export DOCKER_HOST=unix:///run/user/$UID/podman/podman.sock
```

O Ryuk (limpador automático do Testcontainers) é desabilitado em
`tests/conftest.py`, pois não funciona com Podman rootless.

```bash
poetry run poe test
```

Na primeira execução a imagem `postgres:17-alpine` é baixada.
