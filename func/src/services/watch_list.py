from src.domain.request.model import WatchListSymbols
from src.domain.watch_list.model import WatchListSymbolModel
from src.repositories.watch_list.repository import WatchListRepository


class WatchListService:
    @classmethod
    async def delete_symbols(cls, watch_list_symbols: WatchListSymbols, unique_id: str):
        symbols_list = [
            WatchListSymbolModel(symbol, unique_id)
            for symbol in watch_list_symbols.symbols
        ]
        await WatchListRepository.remove_symbols_from_watch_list(symbols_list)
        return True
