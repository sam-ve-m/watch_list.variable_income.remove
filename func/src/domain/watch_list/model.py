from src.domain.request.model import WatchListSymbol


class WatchListSymbolModel:
    def __init__(self, watch_list_symbol: WatchListSymbol, unique_id: str):
        self.__unique_id = unique_id
        self.__symbol = watch_list_symbol.symbol
        self.__region = watch_list_symbol.region

    def to_dict(self) -> dict:
        dict_representation = {
            "unique_id": self.__unique_id,
            "symbol": self.__symbol,
            "region": self.__region,
            "_id": self.get_id(),
        }
        return dict_representation

    def get_id(self) -> str:
        _id = f"{self.__symbol}_{self.__region.value}_{self.__unique_id}"
        return _id
