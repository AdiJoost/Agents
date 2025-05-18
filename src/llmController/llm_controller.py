#import ollama
from ollama import Client, AsyncClient
import ollama

from config.applicationConfig.applicationConfigFields import ApplicationConfigFields
from config.configManager import getConfig
from log.logger import Logger
from src.actions.questions.question import Question
from src.enums.deploymentMode import DeploymentMode
from src.utils.serverConfig.serverConfig import ServerConfig
#import asyncio

class LLM_Controller():

    def __init__(self, model: str="mistral:7b",
                 role = None,
                 agent_prompt: str=None,
                 host = "http://ollama:11434") -> None: 

        self.model = model  # Modell für Ollama: https://ollama.com/library
        self.role = role    # Rolle: Liberal, Faschichst, Hitler
        self.agent_prompt = agent_prompt or f"Du agierst als Rolle {role} im Secret Hitler Spiel" # Persönlichkeit/Verhalten global steuern
        # Custom client: damit ich Ollama auf anderer Server (Docker) laufen lassen kann
        self.host = ServerConfig.getOllamaAddress()
        self.logger = Logger()
        self.logger.info(f"Ollama-Adress is {self.host}")
        self.client = Client(host=host)
        self.client.pull(model=model)
        # Async client: bessere Performance wenn viele Agenten parallel laufen
        self.async_client = AsyncClient(host=host)
        

    def toString(self) ->str:
        return f"Model: {self.model}, role: {self.role}, host: {self.host}"

    def generateOnMessage(self, messages: list) -> str:
        # LLM wird angesprochen, Antwort als string Rückgabe
        try:
            response = self.client.chat(        # ruft ollama synchron auf mit:
                model=self.model,               # - Modell &
                messages=messages               # - alle bisher gesammelten Nachrichten
            )
            answer = response['message']['content'].strip()     # strip entfernt unnötige Leerzeichen/Umbrüche/Tabs am Anfang/Ende
            return answer

        # falls ollama nicht antwortet oder Fehler auftritt
        except Exception as e:
            self.logger.error(e)
            self.logger.error(f"Call to LLM <{self.model}> failed. Controller: <{self.toString()}>")
            return ""
        
    def generateAnswere(self, messages: list, question: Question) -> Question:
         # LLM wird angesprochen, Antwort als string Rückgabe
        try:
            response = self.client.chat(        # ruft ollama synchron auf mit:
                model=self.model,               # - Modell &
                messages=messages,
                format=question.getAnswereSchema().model_json_schema(),               # - alle bisher gesammelten Nachrichten
            )
            question.setResult(response)     # strip entfernt unnötige Leerzeichen/Umbrüche/Tabs am Anfang/Ende
            return question

        # falls ollama nicht antwortet oder Fehler auftritt
        except Exception as e:
            self.logger.error(e)
            self.logger.error(f"Call to LLM <{self.model}> failed. Controller: <{self.toString()}>")
            return ""

    def generate(self, prompt: str) -> str:     # nimmt Prompt/Spielsituation entgegen
        # call the LLM on ollama and return the answer
        # https://github.com/ollama/ollama-python

        messages = []

        if self.agent_prompt:
            messages.append({"role": "user", "content": self.agent_prompt}) # Agenten-Prompt zur Nachricht hinzugefügt

        # eigentlicher Input des Agenten
        messages.append({"role": "user", "content": prompt})    # aktuelle Spielsituation zur Nachricht hinzugefügt

        # LLM wird angesprochen, Antwort als string Rückgabe
        try:
            response = self.client.chat(        # ruft ollama synchron auf mit:
                model=self.model,               # - Modell &
                messages=messages               # - alle bisher gesammelten Nachrichten
            )
            answer = response['message']['content'].strip()     # strip entfernt unnötige Leerzeichen/Umbrüche/Tabs am Anfang/Ende
            return answer

        # falls ollama nicht antwortet oder Fehler auftritt
        except Exception as e:
            print("Fehler der Kommunikation mit LLM: {e}")
            return ""

    # Streaming responses (LLM Antworten live empfangen -> Diskussionen realistischer)
    def generate_stream(self, prompt: str) -> str:
        messages = []

        if self.agent_prompt:
            messages.append({"role": "user", "content": self.agent_prompt})

        messages.append({"role": "user", "content": prompt})

        try:
            # startet ollama im Streaming-Modus -> Antworten kommen stückweise
            stream = self.client.chat(      # self.client anstatt ollama.chat für den custom host
                model=self.model,
                messages=messages,
                stream=True
            )
            response_content = ""       # gibt Antwort live aus, paralleler Zusammenbau des ganzen Texts
            for chunk in stream:
                print(chunk['message']['content'], end='', flush=True)
                response_content += chunk['message']['content']
            return response_content.strip()

        except Exception as e:
            print("Fehler der Kommunikation mit LLM: {e}")
            return ""

    # Async Client (-> paralleles & performantes Arbeiten mit mehreren Agenten)
    async def generate_async(self, prompt: str) -> str:
        messages = []

        if self.agent_prompt:
            messages.append({"role": "user", "content": self.agent_prompt})

        messages.append({"role": "user", "content": prompt})

        try:
            response_content = ""       # Anwort asychron holen -> effizienter, Antwort auch stückweise live
            response = await self.async_client.chat(model=self.model,
                                                    messages=messages,
                                                    stream=True)
            async for part in response:
                response_content += part['message']['content']
                print(part['message']['content'], end='', flush=True)
            return response_content.strip()

        except Exception as e:
            print("Fehler der Kommunikation mit LLM: {e}")
            return ""

