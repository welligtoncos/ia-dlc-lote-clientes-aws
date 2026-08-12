from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

from lote_shared.domain.status_lote import StatusLote


@dataclass
class Lote:
    nome_arquivo: str
    id: Optional[int] = None
    caminho_arquivo: Optional[str] = None
    status: StatusLote = StatusLote.PENDENTE
    total_linhas: int = 0
    linhas_validas: int = 0
    linhas_invalidas: int = 0
    erro: Optional[str] = None
    celery_task_id: Optional[str] = None
    criado_em: datetime = field(default_factory=datetime.utcnow)
    concluido_em: Optional[datetime] = None

    @classmethod
    def criar_pendente(cls, nome_arquivo: str) -> "Lote":
        if not nome_arquivo or not nome_arquivo.strip():
            raise ValueError("nome_arquivo obrigatorio")
        return cls(nome_arquivo=nome_arquivo.strip(), status=StatusLote.PENDENTE)

    def pode_reprocessar(self) -> bool:
        return self.status == StatusLote.ERRO

    def preparar_reprocessamento(self) -> None:
        if not self.pode_reprocessar():
            raise ValueError("somente lotes em ERRO podem ser reprocessados")
        self.status = StatusLote.PENDENTE
        self.erro = None
        self.total_linhas = 0
        self.linhas_validas = 0
        self.linhas_invalidas = 0
        self.concluido_em = None
        self.celery_task_id = None

    def associar_task(self, task_id: str) -> None:
        self.celery_task_id = task_id

    def marcar_processando(self) -> None:
        self.status = StatusLote.PROCESSANDO

    def marcar_concluido(
        self, total: int, validas: int, invalidas: int
    ) -> None:
        self.total_linhas = total
        self.linhas_validas = validas
        self.linhas_invalidas = invalidas
        self.status = StatusLote.CONCLUIDO
        self.concluido_em = datetime.utcnow()
        self.erro = None

    def marcar_erro(self, mensagem: str) -> None:
        self.status = StatusLote.ERRO
        self.erro = mensagem
        self.concluido_em = datetime.utcnow()
