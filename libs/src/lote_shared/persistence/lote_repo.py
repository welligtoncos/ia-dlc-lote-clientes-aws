from __future__ import annotations

from datetime import datetime

from sqlalchemy import DateTime, Integer, String, Text, create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column, sessionmaker

from lote_shared.domain.lote import Lote
from lote_shared.domain.status_lote import StatusLote


class Base(DeclarativeBase):
    pass


class LoteORM(Base):
    __tablename__ = "lotes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nome_arquivo: Mapped[str] = mapped_column(String(255), nullable=False)
    caminho_arquivo: Mapped[str | None] = mapped_column(String(512), nullable=True)
    status: Mapped[str] = mapped_column(String(20), nullable=False, default="PENDENTE")
    total_linhas: Mapped[int] = mapped_column(Integer, default=0)
    linhas_validas: Mapped[int] = mapped_column(Integer, default=0)
    linhas_invalidas: Mapped[int] = mapped_column(Integer, default=0)
    erro: Mapped[str | None] = mapped_column(Text, nullable=True)
    celery_task_id: Mapped[str | None] = mapped_column(String(155), nullable=True)
    criado_em: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    concluido_em: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)


def criar_engine(database_url: str):
    return create_engine(database_url, pool_pre_ping=True)


def criar_session_factory(database_url: str):
    engine = criar_engine(database_url)
    Base.metadata.create_all(engine)
    return sessionmaker(bind=engine, expire_on_commit=False)


def _para_dominio(row: LoteORM) -> Lote:
    return Lote(
        id=row.id,
        nome_arquivo=row.nome_arquivo,
        caminho_arquivo=row.caminho_arquivo,
        status=StatusLote(row.status),
        total_linhas=row.total_linhas,
        linhas_validas=row.linhas_validas,
        linhas_invalidas=row.linhas_invalidas,
        erro=row.erro,
        celery_task_id=row.celery_task_id,
        criado_em=row.criado_em,
        concluido_em=row.concluido_em,
    )


def _aplicar(row: LoteORM, lote: Lote) -> None:
    row.nome_arquivo = lote.nome_arquivo
    row.caminho_arquivo = lote.caminho_arquivo
    row.status = lote.status.value
    row.total_linhas = lote.total_linhas
    row.linhas_validas = lote.linhas_validas
    row.linhas_invalidas = lote.linhas_invalidas
    row.erro = lote.erro
    row.celery_task_id = lote.celery_task_id
    row.criado_em = lote.criado_em
    row.concluido_em = lote.concluido_em


class LoteRepositorio:
    def __init__(self, session_factory: sessionmaker[Session]) -> None:
        self._session_factory = session_factory

    def salvar(self, lote: Lote) -> Lote:
        with self._session_factory() as session:
            if lote.id is None:
                row = LoteORM()
                _aplicar(row, lote)
                session.add(row)
                session.commit()
                session.refresh(row)
                return _para_dominio(row)
            row = session.get(LoteORM, lote.id)
            if row is None:
                raise KeyError(lote.id)
            _aplicar(row, lote)
            session.commit()
            session.refresh(row)
            return _para_dominio(row)

    def obter_por_id(self, lote_id: int) -> Lote | None:
        with self._session_factory() as session:
            row = session.get(LoteORM, lote_id)
            return _para_dominio(row) if row else None

    def listar_ordenados_por_criacao_desc(self) -> list[Lote]:
        with self._session_factory() as session:
            rows = (
                session.query(LoteORM)
                .order_by(LoteORM.criado_em.desc())
                .all()
            )
            return [_para_dominio(r) for r in rows]

    def remover(self, lote_id: int) -> bool:
        with self._session_factory() as session:
            row = session.get(LoteORM, lote_id)
            if row is None:
                return False
            session.delete(row)
            session.commit()
            return True
