import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    APP_NAME: str = "LLM FastAPI kafka Application"
    API_V1_STR: str = "/app/v1"

    KAFKA_BOOTSTRAP_SERVERS: str = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
    KAFKA_CONSUMER_GROUP: str = os.getenv("KAFKA_CONSUMER_GROUP", "llm-fastapi-group")
    KAFKA_INPUT_TOPIC: str = os.getenv("KAFKA_INPUT_TOPIC", "llm-fastapi-input")
    KAFKA_OUTPUT_TOPIC: str = os.getenv("KAFKA_OUTPUT_TOPIC", "llm-fastapi-output")

    LLM_API_KEY: str = os.getenv("LLM_API_KEY", "your_llm_api_key")
    LLM_MODEL: str = os.getenv("LLM_MODEL", "gpt-3.5-turbo")

    HOST: str = os.getenv("HOST","0.0.0.0")
    PORT: int = os.getenv("PORT", 8000)

    SENTRY_DSN: str = os.getenv("SENTRY_DSN", "https://a9af8782b993b18dd886de71330ed674@o4509286698319872.ingest.us.sentry.io/4509286700023808")
    SENTRY_ENVIRONMENT: str = os.getenv("SENTRY_ENVIRONMENT", "development")
    SENTRY_TRACES_SAMPLE_RATE: float = os.getenv("SENTRY_TRACES_SAMPLE_RATE", 1.0)

settings = Settings()

