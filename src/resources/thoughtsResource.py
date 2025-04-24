from src.models.messageModel import MessageModel
from src.models.thoughtsModel import ThoughtsModel
from src.resources.baseResource import BaseResource


class ThoughtResource(BaseResource):

    def get(self):
        return self.handleGetResponse(ThoughtsModel)
    
class ThoughtsResource(BaseResource):

    def get(self):
        return self.handleGetMany(ThoughtsModel)