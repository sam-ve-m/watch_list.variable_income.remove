from unittest.mock import patch

from pytest import mark

from func.src.domain.request.model import WatchListSymbol
from func.src.domain.watch_list.model import WatchListSymbolModel
from func.src.repositories.watch_list.repository import WatchListRepository
from func.src.services.watch_list import WatchListService

dummy_symbols_to_register = {"symbol": "PETR4", "region": "BR"}
dummy_watch_list_symbols = WatchListSymbol(**dummy_symbols_to_register)


@mark.asyncio
@patch.object(WatchListRepository, "remove_symbol_from_watch_list")
async def test_register_symbols(remove_symbols_from_watch_list_mock):
    result = await WatchListService.delete_symbols(dummy_watch_list_symbols, "test-id")
    assert remove_symbols_from_watch_list_mock.call_count == 1
    for call in remove_symbols_from_watch_list_mock.call_args[0]:
        assert isinstance(call, WatchListSymbolModel)
    assert result is True
