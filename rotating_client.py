from openai import OpenAI, OpenAIError
import itertools
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class RotatingOpenAIClient:
    def __init__(self, api_keys, base_url, model, system_prompt="You are a helpful assistant"):
        if not api_keys:
            raise ValueError("At least one API key is required")
        self.api_keys = list(api_keys)
        self.base_url = base_url
        self.model = model
        self.system_prompt = system_prompt
        self._key_cycle = itertools.cycle(self.api_keys)
        self._current_key = next(self._key_cycle)
        self._client = self._build_client(self._current_key)

    def _build_client(self, api_key):
        return OpenAI(api_key=api_key, base_url=self.base_url)

    def _rotate_key(self):
        self._current_key = next(self._key_cycle)
        self._client = self._build_client(self._current_key)
        logger.info(f"Rotated to key ending in ...{self._current_key[-4:]}")

    def chat(self, user_message, system_prompt=None, max_retries=None, **kwargs):
        """
        Send a chat message, rotating through keys on failure.
        Tries each key once by default before giving up.
        """
        max_retries = max_retries or len(self.api_keys)
        last_error = None

        for attempt in range(max_retries):
            try:
                response = self._client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": system_prompt or self.system_prompt},
                        {"role": "user", "content": user_message},
                    ],
                    **kwargs,
                )
                return response.choices[0].message.content
            except OpenAIError as e:
                last_error = e
                logger.warning(
                    f"Key ...{self._current_key[-4:]} failed (attempt {attempt + 1}/{max_retries}): {e}"
                )
                self._rotate_key()

        raise RuntimeError(f"All {max_retries} attempts failed. Last error: {last_error}")

