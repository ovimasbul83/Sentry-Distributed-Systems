from pydantic import BaseModel, Field
from typing import Dict, Any, Optional

class LLMRequest(BaseModel):
    """
    Request Model for LLM
    """
    prompt: str = Field(..., description="Prompt for the LLM")

class LLMResponse(BaseModel):
    """
    Response Model for LLM
    """
    response: str = Field(..., description="Response from the LLM")
    request_id: Optional[str] = Field(None, description="Request ID for tracking")

class kafkaMessage(BaseModel):
    """
    Kafka Message Model
    """
    prompt: str = Field(..., description="Prompt for the LLM")
    request_id: str = Field(..., description="Request ID for tracking")

class KafkaResponse(BaseModel):
    """
    Kafka Response Model
    """
    success: bool = Field(..., description="Success status of the operation")
    request_id: str = Field(..., description="Request ID for tracking")
    message: Optional[str] = Field(None, description="Message detailing the operation result")

