from flask import request
from bson.objectid import ObjectId
from src.models.thoughtsModel import ThoughtsModel
from src.resources.baseResource import BaseResource


class ThoughtResource(BaseResource):

    def get(self):
        return self.handleGetResponse(ThoughtsModel)
    
class ThoughtsResource(BaseResource):

    def get(self):
        if (request.args.get("gameId")):
            query = {"gameId": ObjectId(request.args.get("gameId"))}
            return self.handleGetManyWithFilter(ThoughtsModel, query=query)
        return self.handleGetMany(ThoughtsModel)