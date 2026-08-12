from __future__ import annotations

import json
from datetime import datetime

import redis

from lote_shared.domain.lote import Lote
from lote_shared.domain.status_lote import StatusLote


def _serializar(lote: Lote) -> str:
    return json.dumps(
        {
            "id": lote.id,
            "nome_arquivo": lote.nome_arquivo,
            "caminho_arquivo": lote.caminho_arquivo,
            "status": lote.status.value,
            "total_linhas": lote.total_linhas,
            "linhas_validas": lote.linhas_validas,
            "linhas_invalidas": lote.linhas_invalidas,
            "erro": lote.erro,
            "celery_task_id": lote.celery_task_id,
            "criado_em": lote.criado_em.isoformat() if lote.criado_em else None,
            "concluido_em": lote.concluido_em.isoformat()
            if lote.concluido_em
            else None,
        }
    )


def _desserializar(raw: str) -> Lote:
    data = json.loads(raw)
    return Lote(
        id=data["id"],
        nome_arquivo=data["nome_arquivo"],
        caminho_arquivo=data.get("caminho_arquivo"),
        status=StatusLote(data["status"]),
        total_linhas=data.get("total_linhas", 0),
        linhas_validas=data.get("linhas_validas", 0),
        linhas_invalidas=data.get("linhas_invalidas", 0),
        erro=data.get("erro"),
        celery_task_id=data.get("celery_task_id"),
        criado_em=datetime.fromisoformat(data["criado_em"])
        if data.get("criado_em")
        else datetime.utcnow(),
        concluido_em=datetime.fromisoformat(data["concluido_em"])
        if data.get("concluido_em")
        else None,
    )


class CacheLoteRedis:
    def __init__(self, url: str, prefixo: str = "lote:") -> None:
        self._client = redis.Redis.from_url(url, decode_responses=True)
        self._prefixo = prefixo
        self._chave_lista = "lotes:lista"

    def _chave(self, lote_id: int) -> str:
        return f"{self._prefixo}{lote_id}"

    def obter(self, lote_id: int) -> Lote | None:
        raw = self._client.get(self._chave(lote_id))
        return _desserializar(raw) if raw else None

    def gravar(self, lote: Lote, ttl_segundos: int = 60) -> None:
        if lote.id is None:
            return
        self._client.setex(self._chave(lote.id), ttl_segundos, _serializar(lote))

    def invalidar(self, lote_id: int) -> None:
        self._client.delete(self._chave(lote_id))
        self.invalidar_lista()

    def invalidar_lista(self) -> None:
        self._client.delete(self._chave_lista)
