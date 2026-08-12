from __future__ import annotations

import logging
import time
import uuid
from typing import Callable

from fastapi import FastAPI, File, HTTPException, Request, Response, UploadFile
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from lote_shared.domain.excecoes import (
    ArquivoAusenteParaReprocessamento,
    ArquivoInvalido,
    ErroDominioLote,
    LoteNaoEncontrado,
    ReprocessamentoNaoPermitido,
    TamanhoExcedido,
    TarefaNaoPermitida,
)
from lote_shared.domain.lote import Lote

logger = logging.getLogger("lote_api")


class LoteResposta(BaseModel):
    lote_id: int
    nome_arquivo: str
    status: str
    total_linhas: int = 0
    linhas_validas: int = 0
    linhas_invalidas: int = 0
    criado_em: str | None = None
    erro: str | None = None


def lote_para_resposta(lote: Lote) -> LoteResposta:
    return LoteResposta(
        lote_id=lote.id or 0,
        nome_arquivo=lote.nome_arquivo,
        status=lote.status.value,
        total_linhas=lote.total_linhas,
        linhas_validas=lote.linhas_validas,
        linhas_invalidas=lote.linhas_invalidas,
        criado_em=lote.criado_em.isoformat() if lote.criado_em else None,
        erro=lote.erro,
    )


def mapear_erro_http(exc: ErroDominioLote) -> HTTPException:
    if isinstance(exc, LoteNaoEncontrado):
        return HTTPException(status_code=404, detail=str(exc))
    if isinstance(exc, TamanhoExcedido):
        return HTTPException(status_code=413, detail=str(exc))
    if isinstance(exc, (ReprocessamentoNaoPermitido, ArquivoAusenteParaReprocessamento)):
        return HTTPException(status_code=409, detail=str(exc))
    if isinstance(exc, (ArquivoInvalido, TarefaNaoPermitida)):
        return HTTPException(status_code=400, detail=str(exc))
    return HTTPException(status_code=400, detail=str(exc))


def criar_app(
    ingerir,
    obter,
    listar,
    reprocessar,
    remover,
) -> FastAPI:
    app = FastAPI(title="lote-api", version="0.1.0")

    @app.middleware("http")
    async def request_id_middleware(request: Request, call_next: Callable):
        request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
        inicio = time.perf_counter()
        response: Response = await call_next(request)
        latencia_ms = int((time.perf_counter() - inicio) * 1000)
        response.headers["X-Request-ID"] = request_id
        logger.info(
            {
                "request_id": request_id,
                "method": request.method,
                "path": request.url.path,
                "status": response.status_code,
                "latencia_ms": latencia_ms,
            }
        )
        return response

    @app.get("/health")
    def health():
        return {"status": "ok"}

    @app.post("/lotes", status_code=202)
    async def post_lotes(arquivo: UploadFile = File(...)):
        conteudo = await arquivo.read()
        try:
            return ingerir.executar(arquivo.filename or "", conteudo)
        except ErroDominioLote as exc:
            raise mapear_erro_http(exc) from exc

    @app.get("/lotes")
    def get_lotes():
        lotes = listar.executar()
        return [lote_para_resposta(l) for l in lotes]

    @app.get("/lotes/{lote_id}")
    def get_lote(lote_id: int):
        try:
            return lote_para_resposta(obter.executar(lote_id))
        except ErroDominioLote as exc:
            raise mapear_erro_http(exc) from exc

    @app.put("/lotes/{lote_id}", status_code=202)
    def put_lote(lote_id: int):
        try:
            return reprocessar.executar(lote_id)
        except ErroDominioLote as exc:
            raise mapear_erro_http(exc) from exc

    @app.delete("/lotes/{lote_id}", status_code=204)
    def delete_lote(lote_id: int):
        try:
            remover.executar(lote_id)
        except ErroDominioLote as exc:
            raise mapear_erro_http(exc) from exc
        return Response(status_code=204)

    @app.exception_handler(Exception)
    async def unhandled(_, exc: Exception):
        logger.exception("erro nao tratado: %s", exc)
        return JSONResponse(status_code=500, content={"detail": "erro interno"})

    return app
