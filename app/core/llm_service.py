import logging
from openai import OpenAI
import sentry_sdk
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from app.core.config import settings

logger = logging.getLogger(__name__)


class LLMService:
    def __init__(self):
        self.client = OpenAI(api_key=settings.LLM_API_KEY)
        self.model = settings.LLM_MODEL
        logger.info(f"LLMService initialized with model: {self.model}")

    async def generate_response(self, prompt: str) -> str:
        """
        Response Generation
        """
        try:
            with sentry_sdk.start_span(
                op="openai_api_call", description=f"OpenAI API {self.model} call"
            ) as span:
                span.set_data("prompt_length", len(prompt))
                span.set_data("model", self.model)

                logger.debug(f"Generating response for prompt: {prompt}")
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=200,
                    temperature=0.7,
                )
                span.set_data(
                    "response_length", len(response.choices[0].message.content)
                )
                span.set_data(
                    "tokens_used",
                    (
                        response.usage.total_tokens
                        if hasattr(response.usage, "total_tokens")
                        else None
                    ),
                )

            return response.choices[0].message.content

        except Exception as e:
            logger.error(f"Error generating reponse: {e}")
            sentry_sdk.capture_exception(e)
            return f"Error generating response: {e}"


LLMService = LLMService()
