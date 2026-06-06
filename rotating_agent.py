from textarena.core import Agent
from textarena_utils import parse_model_response

class RotatingOpenAIAgent(Agent):
    def __init__(self, client):
        super().__init__()
        self.client = client

    def __call__(self, observation: str) -> dict[str, str]:
        raw_response = self.client.chat(user_message=observation) 
        parsed = parse_model_response(raw_response)

        return {
            "prompt": observation,
            "raw_response": raw_response,
            "reasoning_trace": "", 
            "action": parsed.action,
        }