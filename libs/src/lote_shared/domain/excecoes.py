class ErroDominioLote(Exception):
    """Erro de negocio base do dominio de lotes."""


class LoteNaoEncontrado(ErroDominioLote):
    def __init__(self, lote_id: int) -> None:
        self.lote_id = lote_id
        super().__init__(f"Lote {lote_id} nao encontrado")


class ArquivoInvalido(ErroDominioLote):
    pass


class TamanhoExcedido(ErroDominioLote):
    def __init__(self, tamanho_bytes: int, limite_bytes: int) -> None:
        self.tamanho_bytes = tamanho_bytes
        self.limite_bytes = limite_bytes
        super().__init__(
            f"Arquivo com {tamanho_bytes} bytes excede limite de {limite_bytes} bytes"
        )


class ReprocessamentoNaoPermitido(ErroDominioLote):
    def __init__(self, lote_id: int, status: str) -> None:
        self.lote_id = lote_id
        self.status = status
        super().__init__(
            f"Lote {lote_id} com status {status} nao pode ser reprocessado"
        )


class ArquivoAusenteParaReprocessamento(ErroDominioLote):
    def __init__(self, lote_id: int, caminho: str) -> None:
        self.lote_id = lote_id
        self.caminho = caminho
        super().__init__(
            f"Arquivo ausente para reprocessar lote {lote_id}: {caminho}"
        )


class TarefaNaoPermitida(ErroDominioLote):
    def __init__(self, nome_tarefa: str) -> None:
        self.nome_tarefa = nome_tarefa
        super().__init__(f"Tarefa nao permitida: {nome_tarefa}")


class ErroArmazenamento(ErroDominioLote):
    """Falha de I/O ou configuracao do armazenamento."""


class ObjetoNaoEncontrado(ErroDominioLote):
    def __init__(self, ref: str) -> None:
        self.ref = ref
        super().__init__(f"Objeto de armazenamento nao encontrado: {ref}")
