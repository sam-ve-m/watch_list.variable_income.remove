from func.src.domain.enums.region.enum import Region

from pydantic import BaseModel, constr, validator


class WatchListSymbol(BaseModel):
    symbol: constr(min_length=1)
    region: Region

    @validator("symbol")
    def validate_symbols(cls, symbol):
        symbol = symbol.upper()
        return symbol
