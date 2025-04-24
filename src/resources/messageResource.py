from flask import request
from bson.objectid import ObjectId
from src.models.messageModel import MessageModel
from src.resources.baseResource import BaseResource


class MessageResource(BaseResource):

    def get(self):
        return self.handleGetResponse(MessageModel)
    
class MessagesResource(BaseResource):

    def get(self):
        if (request.args.get("gameId")):
            query = {"gameId": ObjectId(request.args.get("gameId"))}
            return self.handleGetManyWithFilter(MessageModel, query=query)
        return self.handleGetMany(MessageModel)