from __future__ import annotations

import os

from pydantic_settings import BaseSettings, SettingsConfigDict


class Configuracoes(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    database_url: str
    celery_broker_url: str
    cache_url: str = "redis://localhost:6379/1"
    storage_path: str = ""
    storage_local_dir: str = ""
    storage_backend: str = "fs"
    s3_bucket: str = ""
    aws_region: str = "us-east-1"
    s3_prefix: str = "lotes/"
    aws_access_key_id: str = ""
    aws_secret_access_key: str = ""
    log_level: str = "INFO"

    @property
    def diretorio_storage(self) -> str:
        return self.storage_local_dir or self.storage_path

    def validar_obrigatorios(self) -> None:
        faltando = [
            nome
            for nome, valor in {
                "DATABASE_URL": self.database_url,
                "CELERY_BROKER_URL": self.celery_broker_url,
            }.items()
            if not valor
        ]
        backend = (self.storage_backend or "fs").lower()
        if backend == "fs" and not self.diretorio_storage:
            faltando.append("STORAGE_LOCAL_DIR ou STORAGE_PATH")
        if backend == "s3":
            if not self.s3_bucket:
                faltando.append("S3_BUCKET")
            # Q6=B: keys obrigatorias na API quando s3 (env ou ja exportadas)
            access = self.aws_access_key_id or os.environ.get("AWS_ACCESS_KEY_ID", "")
            secret = self.aws_secret_access_key or os.environ.get(
                "AWS_SECRET_ACCESS_KEY", ""
            )
            if not access:
                faltando.append("AWS_ACCESS_KEY_ID")
            if not secret:
                faltando.append("AWS_SECRET_ACCESS_KEY")
        if faltando:
            raise RuntimeError(f"Variaveis obrigatorias ausentes: {', '.join(faltando)}")
