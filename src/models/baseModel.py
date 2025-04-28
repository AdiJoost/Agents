from typing import Union
from bson import ObjectId

from config.configFiles import ConfigFiles
from config.configManager import getConfig
from config.mongoDBConfig.mongoDbConfigFields import MongoDBConfigFields
from src.database.database_utils import deleteDocument, getDocumentById, getDocuments, getDocumentsWithFilter, saveDocument

class BaseModel():

    DATABASE_NAME = getConfig(MongoDBConfigFields.DATABASE_NAME.value, ConfigFiles.MONGO_DB_CONFIG)
    COLLECTION_NAME = None

    def __init__(self, _id: Union[str, ObjectId]=None):
        self._id = self._castToObjectId(_id)

    def getId(self) -> ObjectId:
        return self._id
    
    def setId(self, _id: ObjectId) -> None:
        self._id = _id

    def addIdToJson(self, values: dict) -> dict:
        if self._id is not None:
            values["_id"] = str(self._id)
        return values

    def save(self) -> None:
        upserResult: ObjectId = saveDocument(self.toJson(), databaseName=self.DATABASE_NAME, collectionName=self.COLLECTION_NAME)
        if upserResult is not None:
            self._id = upserResult

    def _castToObjectId(self, _id: Union[str, ObjectId]) -> ObjectId:
        if _id is None:
            return None
        if isinstance(_id, ObjectId):
            return _id
        return ObjectId(_id)
    
    @classmethod
    def get(cls, objectId: ObjectId):
        result: dict = getDocumentById(objectId, databaseName=cls.DATABASE_NAME, collectionName=cls.COLLECTION_NAME)
        if result is None:
            return None
        result["_id"] = objectId
        return cls(**result)
    
    @classmethod
    def getMany(cls, limit: int, offset: int) -> list:
        result: list = getDocuments(limit, offset, databaseName=cls.DATABASE_NAME, collectionName=cls.COLLECTION_NAME)
        if result is None:
            return None
        return [cls(**item) for item in result]
    
    @classmethod
    def getManyWithCondition(cls, limit: int, offset: int, filterDict: dict) -> list:
        result: list = getDocumentsWithFilter(limit, offset, databaseName=cls.DATABASE_NAME, collectionName=cls.COLLECTION_NAME, filterDict=filterDict)
        if result is None:
            return None
        return [cls(**item) for item in result]
    
    @classmethod
    def delete(cls, objectId: ObjectId):
        deleteDocument(objectId, databaseName=cls.DATABASE_NAME, collectionName=cls.COLLECTION_NAME)