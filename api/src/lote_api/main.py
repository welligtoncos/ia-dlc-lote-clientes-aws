import logging
import sys

from lote_shared.cache.cache_lote import CacheLoteRedis
from lote_shared.persistence.lote_repo import criar_session_factory, LoteRepositorio

from lote_api.application.casos_uso import (
    CasoUsoIngerirClientes,
    CasoUsoListarLotes,
    CasoUsoObterLote,
    CasoUsoRemoverLote,
    CasoUsoReprocessarLote,
)
from lote_api.infrastructure.adapters import AdaptadorCelery, ArmazenamentoArquivoLocal
from lote_api.infrastructure.settings import Configuracoes
from lote_api.presentation.app import criar_app


def montar_aplicacao():
    cfg = Configuracoes()
    cfg.validar_obrigatorios()

    logging.basicConfig(
        stream=sys.stdout,
        level=getattr(logging, cfg.log_level.upper(), logging.INFO),
        format="%(message)s",
    )

    session_factory = criar_session_factory(cfg.database_url)
    repo = LoteRepositorio(session_factory)
    armazenamento = ArmazenamentoArquivoLocal(cfg.storage_path)
    tarefas = AdaptadorCelery(cfg.celery_broker_url)
    cache = CacheLoteRedis(cfg.cache_url)

    ingerir = CasoUsoIngerirClientes(repo, armazenamento, tarefas, cache)
    obter = CasoUsoObterLote(repo, cache)
    listar = CasoUsoListarLotes(repo)
    reprocessar = CasoUsoReprocessarLote(repo, armazenamento, tarefas, cache)
    remover = CasoUsoRemoverLote(repo, cache)

    return criar_app(ingerir, obter, listar, reprocessar, remover)


app = montar_aplicacao()
