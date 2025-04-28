from src.models.metaDataModel import MetaDataModel
from src.resources.baseResource import BaseResource


class GameResource(BaseResource):

    def get(self):
        return self.handleGetResponse(MetaDataModel)
    
class GamesResource(BaseResource):

    def get(self):
        return self.handleGetMany(MetaDataModel)