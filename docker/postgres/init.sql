-- Executado apenas na primeira inicialização do volume (docker-entrypoint-initdb.d).
-- Cria o banco usado pelos testes; o banco `mard` já é criado via POSTGRES_DB.
CREATE DATABASE mard_test OWNER mard;
