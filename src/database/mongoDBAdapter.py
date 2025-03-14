from bson import ObjectId

class MongoDBAdapter():

    def __init__(self) -> None:
        pass

    def getDocument(self, objectId: ObjectId, databaseName: str, collectionName:str) -> any:
        #Create a client connection and then get the document with the objectId from the database and collection given. (Maybe in the future, we want to create bulk insertion, but not for now)
        pass

    def _getClient(self) -> None:
        pass

    def _getCollection(self) -> None:
        pass