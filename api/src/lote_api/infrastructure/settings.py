from pydantic_settings import BaseSettings, SettingsConfigDict


class Configuracoes(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    database_url: str
    celery_broker_url: str
    cache_url: str = "redis://localhost:6379/1"
    storage_path: str
    log_level: str = "INFO"

    def validar_obrigatorios(self) -> None:
        faltando = [
            nome
            for nome, valor in {
                "DATABASE_URL": self.database_url,
                "CELERY_BROKER_URL": self.celery_broker_url,
                "STORAGE_PATH": self.storage_path,
            }.items()
            if not valor
        ]
        if faltando:
            raise RuntimeError(f"Variaveis obrigatorias ausentes: {', '.join(faltando)}")
