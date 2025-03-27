from enum import Enum

class StrEnum(str, Enum):  # Inherit from str and Enum
    def __str__(self):
        return self.value

class SimulationConfigFields(StrEnum):
    AGENTS = "agents"
    AGENT_NAME = "agentName"
    AGENT_ROLE = "agentRole"
    AGENT_ROLE_DESCRIPTION = "agentRoleDescription"
    GENERAL_MODEL_INSTRUCTIONS = "generalModelInstructions"
    MODEL = "model"
    INITIAL_PROMPT = "initialPrompt"
    QUESTION = "question"
