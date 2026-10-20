from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Configurações carregadas de variáveis de ambiente e do arquivo .env."""

    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        extra='ignore',
    )

    project_name: str = 'mard'
    version: str = '0.1.0'
    debug: bool = False

    database_url: str = 'postgresql+asyncpg://mard:mard@localhost:5432/mard'
    test_database_url: str = (
        'postgresql+asyncpg://mard:mard@localhost:5432/mard_test'
    )


settings = Settings()
