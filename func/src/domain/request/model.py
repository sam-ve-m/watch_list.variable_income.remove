# Jormungandr
from src.domain.enums.region.enum import Region

# Third party
from pydantic import BaseModel, constr

from typing import List


class WatchListSymbol(BaseModel):
    symbol: constr(min_length=1)
    region: Region


class WatchListSymbols(BaseModel):
    symbols: List[WatchListSymbol]
