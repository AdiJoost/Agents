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
    NUMBER_OF_LIBERAL_POLICIES = "numberOfLiberalPolicies"
    NUMBER_OF_FACIST_POLICIES = "numberOfFacistPolicies"
    USE_REFLECTION = "useReflection"
    USE_REASONING = "useReasoning"
    PROMPT_PATH = "promptPath"
    TEXT_PROMPT = "textPrompt"
    NUMBER_OF_PASSED_MESSAGES = "numberOfPassedMessages"
    NUMBER_OF_BAD_POLICIES_FOR_WIN = "numberOfBadPoliciesForWin"
    NUMBER_OF_GOOD_POLICIES_FOR_WIN = "numberOfGoodPoliciesForWin"

