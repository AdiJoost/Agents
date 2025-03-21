from bson import ObjectId
from pymongo import MongoClient

class MongoDBAdapter():

    def __init__(self, uri="mongodb://localhost:27017/") -> None:    #uri anpassen
        #Verbindung zu MongoDB
        self.client = MongoClient(uri)

    def get_document(self, object_id: ObjectId, database_name: str, collection_name: str) -> dict | None:
        #Create a client connection and then get the document with the objectId from the database and collection given. (Maybe in the future, we want to create bulk insertion, but not for now)
        collection = self._get_collection(database_name, collection_name)
        return collection.find_one({"_id": object_id})
    
    def get_document_by_game(self, game_id: int, database_name: str, collection_name: str):
        collection = self._get_collection(database_name, collection_name)
        return list(collection.find({"game_id": game_id}, {"_id": 0}))
    
    def get_document_by_round(self, game_id: int, round: int, database_name: str, collection_name: str):
        collection = self._get_collection(database_name, collection_name)
        return list(collection.find({"game_id": game_id, "round": round}, {"_id": 0}))
    
    def get_all_documents(self, database_name: str, collection_name: str):
        collection = self._get_collection(database_name, collection_name)
        return list(collection.find({}, {"_id": 0}))

    def _getClient(self) -> None:
        pass

    def _get_collection(self, database_name: str, collection_name: str):
        #Holt eine Sammlung aus der Datenbank
        db = self.client[database_name]
        return db[collection_name]

    def insert_document(self, document: dict, database_name: str, collection_name: str) -> ObjectId:  
        collection = self._get_collection(database_name, collection_name)
        result = collection.insert_one(document)
        return result.inserted_id