from flask import Flask
from flask_restful import Api
from flasgger import Swagger

from config.rootPath import getRootPath
from src.resources.messageResource import MessageResource, MessagesResource
from src.resources.metaDataResource import GamesResource, GameResource
from src.resources.thoughtsResource import ThoughtResource, ThoughtsResource

app = Flask(__name__)
api = Api(app)

swaggerPath = str(getRootPath().joinpath("src/facade/api/swagger.yaml"))
swagger = Swagger(app, template_file=swaggerPath)


@app.route("/")
def hello():
    return "hello world!"

api.add_resource(MessageResource, "/api/v1/message")
api.add_resource(MessagesResource, "/api/v1/messages")
api.add_resource(GameResource, "/api/v1/game")
api.add_resource(GamesResource, "/api/v1/games")
api.add_resource(ThoughtResource, "/api/v1/thought")
api.add_resource(ThoughtsResource, "/api/v1/thoughts")