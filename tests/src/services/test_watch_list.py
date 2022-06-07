from unittest.mock import patch

from pytest import mark

from src.domain.request.model import WatchListSymbols
from src.domain.watch_list.model import WatchListSymbolModel
from src.repositories.watch_list.repository import WatchListRepository
from src.services.watch_list import WatchListService

dummy_symbols_to_register = {
    "symbols": [
        {"symbol": "PETR4", "region": "BR"},
        {"symbol": "AAPL", "region": "US"},
        {"symbol": "JBSS3", "region": "BR"},
    ]
}

dummy_watch_list_symbols = WatchListSymbols(**dummy_symbols_to_register)


@mark.asyncio
@patch.object(WatchListRepository, "remove_symbols_from_watch_list")
async def test_register_symbols(remove_symbols_from_watch_list_mock):
    result = await WatchListService.delete_symbols(dummy_watch_list_symbols, "test-id")
    assert remove_symbols_from_watch_list_mock.call_count == 1
    for call in remove_symbols_from_watch_list_mock.call_args[0][0]:
        assert isinstance(call, WatchListSymbolModel)
