import logging
import uvicorn
import asyncio
from fastapi import FastAPI
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from app.api import endpoints
from app.core.config import settings    
from app.kafka_test.consumer import start_kafka_consumer
import sentry_sdk
from sentry_sdk.integrations.fastapi import FastApiIntegration
from sentry_sdk.integrations.asyncio import AsyncioIntegration

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

if settings.SENTRY_DSN:
    sentry_sdk.init(
        dsn = "https://a9af8782b993b18dd886de71330ed674@o4509286698319872.ingest.us.sentry.io/4509286700023808",
        environment = settings.SENTRY_ENVIRONMENT,
        traces_sample_rate = settings.SENTRY_TRACES_SAMPLE_RATE,
        integrations = [
            FastApiIntegration(),
            AsyncioIntegration()
        ],
        enable_tracing=True,
    )
    logger.info("Sentry initialized.")
else:
    logger.warning("Sentry DSN not provided. Sentry integration will be disabled.")
app = FastAPI(title=settings.APP_NAME, openapi_url=f"{settings.API_V1_STR}/openapi.json")

app.include_router(endpoints.router, prefix=settings.API_V1_STR)

@app.middleware('http')
async def add_correlation_id(request, call_next):
    """
    Middleware to add correlation ID
    """
    trace_id = request.headers.get("X-Trace-ID")
    if trace_id:
        with sentry_sdk.configure_scope() as scope:
            scope.set_tag("trace_id", trace_id)
    response = await call_next(request)

    return response
    

@app.on_event("startup")
async def startup_event():
    """
    Application Startup Event
    """
    logger.info("Starting Kafka Consumer...")
    await start_kafka_consumer()
    logger.info("Kafka Consumer started.")

@app.get("/")
async def read_root():
    """
    Root Endpoint
    """
    return {"message": "Welcome to the LLM API!"}

if __name__ == "__main__":
    """
    Main Entry Point
    """
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=True
    )