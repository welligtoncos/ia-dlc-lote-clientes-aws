from __future__ import annotations

from lote_shared.cache.cache_lote import CacheLoteRedis


class CacheInvalidator:
    def __init__(self, cache_url: str) -> None:
        self._cache = CacheLoteRedis(cache_url)

    def invalidar_lote(self, lote_id: int) -> None:
        try:
            self._cache.invalidar(lote_id)
        except Exception:
            # falha de cache nao reverte MySQL
            pass
