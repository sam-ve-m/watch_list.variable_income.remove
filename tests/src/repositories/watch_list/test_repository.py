from unittest.mock import patch, AsyncMock

import pytest
from etria_logger import Gladsheim
from nidavellir import Sindri
from pytest import mark

from func.src.domain.request.model import WatchListSymbol
from func.src.domain.watch_list.model import WatchListSymbolModel
from func.src.infrastructures.mongo_db.infrastructure import MongoDBInfrastructure
from func.src.repositories.watch_list.repository import WatchListRepository

dummy_symbol_to_insert = {"symbol": "PETR4", "region": "BR"}

dummy_watch_list_symbol_model = WatchListSymbolModel(
    WatchListSymbol(**dummy_symbol_to_insert), "test_id"
)
dummy_insert = str(
    Sindri.dict_to_primitive_types(dummy_watch_list_symbol_model.to_dict())
)


@mark.asyncio
@patch.object(WatchListRepository, "_WatchListRepository__get_collection")
async def test_insert_all_symbols_in_watch_list(get_collection_mock, monkeypatch):
    class TransactionMock:
        async def __aenter__(self):
            return AsyncMock()

        async def __aexit__(self, exc_type, exc_val, exc_tb):
            return

    class ActuallySessionMock:
        def start_transaction(self):
            return TransactionMock()

        async def __aenter__(self):
            return AsyncMock()

        async def __aexit__(self, exc_type, exc_val, exc_tb):
            pass

    class SessionMock:
        session = ActuallySessionMock()

        async def __aenter__(self):
            return self.session

        async def __aexit__(self, exc_type, exc_val, exc_tb):
            pass

    class ClientMock:
        session = SessionMock()

        async def start_session(self):
            return self.session

        async def __aenter__(self):
            pass

        async def __aexit__(self, exc_type, exc_val, exc_tb):
            pass

    def get_client_mock():
        return ClientMock()

    collection_mock = AsyncMock()
    collection_mock.delete_one.return_value = True
    get_collection_mock.return_value = collection_mock

    monkeypatch.setattr(MongoDBInfrastructure, "get_client", get_client_mock)

    await WatchListRepository.remove_symbol_from_watch_list(
        dummy_watch_list_symbol_model
    )
    get_collection_mock.assert_called_once_with()
    assert collection_mock.delete_one.call_count == 1


@mark.asyncio
@patch.object(Gladsheim, "error")
@patch.object(WatchListRepository, "_WatchListRepository__get_collection")
async def test_insert_all_symbols_in_watch_list_exception(
    get_collection_mock, etria_error_mock, monkeypatch
):
    class ActuallySessionMock:
        def start_transaction(self):
            raise Exception("ERROR")

        async def __aenter__(self):
            return AsyncMock()

        async def __aexit__(self, exc_type, exc_val, exc_tb):
            pass

    class SessionMock:
        session = ActuallySessionMock()

        async def __aenter__(self):
            return self.session

        async def __aexit__(self, exc_type, exc_val, exc_tb):
            pass

    class ClientMock:
        session = SessionMock()

        async def start_session(self):
            return self.session

        async def __aenter__(self):
            pass

        async def __aexit__(self, exc_type, exc_val, exc_tb):
            pass

    def get_client_mock():
        return ClientMock()

    collection_mock = AsyncMock()
    collection_mock.delete_one.return_value = True
    get_collection_mock.return_value = collection_mock

    monkeypatch.setattr(MongoDBInfrastructure, "get_client", get_client_mock)

    with pytest.raises(Exception):
        await WatchListRepository.remove_symbol_from_watch_list(
            dummy_watch_list_symbol_model
        )

        get_collection_mock.assert_called_once_with()
        get_collection_mock.assert_called_once_with()
        collection_mock.delete_one.assert_not_called()
        collection_mock.delete_one.assert_not_awaited()
        etria_error_mock.assert_called()
