import threading
from flask import Flask
from flask_restful import Api
from flasgger import Swagger

from config.rootPath import getRootPath
from config.simulationConfig.simulationManager import SimulationManager
from data.dataManagers.realization.txtManager import TxtManager
from log.logger import Logger
from src.facade.api.utils import createResponse
from src.resources.messageResource import MessageResource, MessagesResource
from src.resources.metaDataResource import GamesResource, GameResource
from src.resources.thoughtsResource import ThoughtResource, ThoughtsResource
from src.simulation.baseSimulation import BaseSimulation
import traceback

app = Flask(__name__)
api = Api(app)

swaggerPath = str(getRootPath().joinpath("src/facade/api/swagger.yaml"))
swagger = Swagger(app, template_file=swaggerPath)

scriptThread: threading.Thread = None
stopEvent = threading.Event()
lock = threading.Lock()
logger = Logger()

def runSimulation():
    try:
        logger.info("Simulation started")
        #simulationManager = SimulationManager("6playersNoReason")
        simulationManager = SimulationManager("table_discussion")
        simulationLogger = TxtManager(filename="SimulationProtocol", folderpath="discussions")
        baseSimulation = BaseSimulation(simulationManager, simulationLogger)
        baseSimulation.run()
    except Exception as e:
        logger.error(f"Error in script: {e}")
        logger.error(f"Traceback: {traceback.format_exc()}")
    finally:
        with lock:
            global scriptThread
            scriptThread = None
        logger.info("Script shut down gracefully")


@app.route("/")
def hello():
    return "hello world!"

@app.route("/start")
def startSimulation():
    with lock:
        global scriptThread
        if scriptThread is not None and scriptThread.is_alive():
            return createResponse({"message": "Script already running."}, 400)
        stopEvent.clear()
        scriptThread = threading.Thread(target=runSimulation)
        scriptThread.start()
        return createResponse({"message": "Script started"}, 200)


api.add_resource(MessageResource, "/api/v1/message")
api.add_resource(MessagesResource, "/api/v1/messages")
api.add_resource(GameResource, "/api/v1/game")
api.add_resource(GamesResource, "/api/v1/games")
api.add_resource(ThoughtResource, "/api/v1/thought")
api.add_resource(ThoughtsResource, "/api/v1/thoughts")