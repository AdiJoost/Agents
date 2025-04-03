from enum import Enum, StrEnum

class SimulationConfigFields(StrEnum):
    AGENTS = "agents"
    AGENT_NAME = "agentName"
    AGENT_ROLE = "agentRole"
    AGENT_ROLE_DESCRIPTION = "agentRoleDescription"
    GENERAL_MODEL_INSTRUCTIONS = "generalModelInstructions"
    MODEL = "model"
    INITIAL_PROMPT = "initialPrompt"
    QUESTION = "question"
    NUMBER_OF_FASCISTS = "numberOfFacists"
