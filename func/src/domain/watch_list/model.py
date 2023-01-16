from func.src.domain.request.model import WatchListSymbol


class WatchListSymbolModel:
    def __init__(self, watch_list_symbol: WatchListSymbol, unique_id: str):
        self.__unique_id = unique_id
        self.__symbol = watch_list_symbol.symbol
        self.__region = watch_list_symbol.region

    def get_id(self) -> str:
        _id = f"{self.__symbol}_{self.__region.value}_{self.__unique_id}"
        return _id
