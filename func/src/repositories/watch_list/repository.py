# Jormungandr
from src.domain.watch_list.model import WatchListSymbolModel
from src.infrastructures.mongo_db.infrastructure import MongoDBInfrastructure
from decouple import config
from nidavellir import Sindri

# Third party
from etria_logger import Gladsheim


class WatchListRepository:

    infra = MongoDBInfrastructure

    @classmethod
    async def __get_collection(cls):
        mongo_client = cls.infra.get_client()
        try:
            database = mongo_client[config("MONGODB_DATABASE_NAME")]
            collection = database[config("MONGODB_WATCH_LIST_COLLECTION")]
            return collection
        except Exception as ex:
            message = f'UserRepository::_get_collection::Error when trying to get collection'
            Gladsheim.error(error=ex, message=message)
            raise ex

    @classmethod
    async def remove_one_symbol_from_watch_list(cls, watch_list_symbol: WatchListSymbolModel):
        collection = await cls.__get_collection()
        try:
            watch_list_symbol_dict = watch_list_symbol.to_dict()
            Sindri.dict_to_primitive_types(watch_list_symbol_dict)
            await collection.delete_one(watch_list_symbol_dict)
        except Exception as ex:
            message = f'UserRepository::insert_one_symbol_in_watch_list::with this query::"user":{watch_list_symbol_dict}'
            Gladsheim.error(error=ex, message=message)
            raise ex

    @classmethod
    async def exists(cls, watch_list_symbol: WatchListSymbolModel):
        collection = await cls.__get_collection()
        try:
            _id = watch_list_symbol.id
            return bool(await collection.find_one({"_id": _id}))
        except Exception as ex:
            message = f'UserRepository::exists::with this query::"user":{watch_list_symbol.to_dict()}'
            Gladsheim.error(error=ex, message=message)
            raise ex
