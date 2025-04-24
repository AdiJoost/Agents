


from src.models.messageModel import MessageModel
from src.resources.baseResource import BaseResource


class MessageResource(BaseResource):

    def get(self):
        return self.handleGetResponse(MessageModel)
    
class MessagesResource(BaseResource):

    def get(self):
        return self.handleGetMany(MessageModel)