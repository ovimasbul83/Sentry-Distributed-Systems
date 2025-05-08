import uuid
import logging
import sentry_sdk
from fastapi import APIRouter, HTTPException
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from app.core.config import settings
from app.core.llm_service import LLMService
from app.kafka_test.producer import send_message_to_kafka
from app.api.models import LLMRequest, LLMResponse, kafkaMessage, KafkaResponse

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/llm/direct", response_model=LLMResponse)
async def get_llm_response(request: LLMRequest):
    """
    Direct LLM API call
    """
    request_id = str(uuid.uuid4())
    with sentry_sdk.start_transaction(op="llm_direct", name="LLM Direct API Call") as transaction:
        transaction.set_tag("request_id", request_id)
        try:
            with sentry_sdk.start_span(op="llm_request", description="LLM Request") as span:    
                response = await LLMService.generate_response(request.prompt)
            return LLMResponse(response=response, request_id=request_id)
    
        except Exception as e:
            logger.error(f"Error in get_llm_response: {e}")
            sentry_sdk.capture_exception(e)
            raise HTTPException(status_code=500, detail= str(e))
    
@router.post("/llm/async", response_model=KafkaResponse)
async def submit_llm_request(request: LLMRequest):
    """
    Asynchronous LLM API call
    """
    request_id = str(uuid.uuid4())
    with sentry_sdk.start_transaction(op="llm_async", name="LLM Async API Call") as transaction:
        transaction.set_tag("request_id", request_id)
        try:
            message = {
                "prompt": request.prompt,
                "request_id": request_id,
                "trace_context": {
                    "trace_id": sentry_sdk.get_current_span().trace_id if sentry_sdk.get_current_span() else None,
                    "span_id": sentry_sdk.get_current_span().span_id if sentry_sdk.get_current_span() else None
                }
            }
            with sentry_sdk.start_span(op="kafka_produce", description="Kafka Produce") as span:
                success = await send_message_to_kafka(settings.KAFKA_INPUT_TOPIC, message)

            if success:
                return KafkaResponse(success=True, request_id=request_id, message="Message sent to Kafka")
            else:
                return KafkaResponse(success=False, request_id=request_id, message="Failed to send message to Kafka")
        except Exception as e:
            logger.error(f"Error in submit_llm_request: {e}")
            sentry_sdk.capture_exception(e)
            return KafkaResponse(success=False, request_id=request_id, message=f"Error:{str(e)}")

