# Jormungandr
from src.domain.enums.region.enum import Region

# Third party
from pydantic import BaseModel, constr, validator

from typing import List


class WatchListSymbol(BaseModel):
    symbol: constr(min_length=1)
    region: Region

    @validator("symbol")
    def validate_symbols(cls, symbol):
        symbol = symbol.upper()
        return symbol


class WatchListSymbols(BaseModel):
    symbols: List[WatchListSymbol]
