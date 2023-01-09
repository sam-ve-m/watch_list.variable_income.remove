from func.src.domain.request.model import WatchListSymbol
from func.src.domain.watch_list.model import WatchListSymbolModel
from func.src.repositories.watch_list.repository import WatchListRepository


class WatchListService:
    @classmethod
    async def delete_symbols(cls, watch_list_symbol: WatchListSymbol, unique_id: str):
        symbol = WatchListSymbolModel(watch_list_symbol, unique_id)
        await WatchListRepository.remove_symbol_from_watch_list(symbol)
        return True
