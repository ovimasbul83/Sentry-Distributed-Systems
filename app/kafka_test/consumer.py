import json 
import logging
import asyncio
from kafka import KafkaConsumer
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from app.core.config import settings
from app.core.llm_service import LLMService
from app.kafka_test.producer import send_message_to_kafka
import sentry_sdk

logger = logging.getLogger(__name__)

async def process_message(message):
    """
    message processing
    """
    try:
        value = json.loads(message.value)
        prompt = value.get('prompt')
        request_id = value.get('request_id')
        trace_context = value.get('trace_context',{})


        if not prompt or not request_id:
            logger.warning(f"Invalid message format: {message.value}")
            return 
        with sentry_sdk.start_transaction(
            op="kafka_consumer",
            name=f"process_message-{request_id[:8]}",
            trace_id=trace_context.get('trace_id'),
            parent_span_id=trace_context.get('span_id'),) as transaction:
            transaction.set_tag("request_id", request_id)
            logger.info(f"Processing message: {message.value}")

            with sentry_sdk.start_span(op="llm_request", description=f"LLM request-{request_id[:8]}") as span:
                response = await LLMService.generate_response(prompt)

            output = {
                "request_id": request_id,
                "prompt": prompt,
                "response": response
            }
            with sentry_sdk.start_span(op="kafka_produce", description=f"Kafka produce-{request_id[:8]}") as span:
                await send_message_to_kafka(settings.KAFKA_OUTPUT_TOPIC, output)

            logger.info(f"Message processed and sent to {settings.KAFKA_OUTPUT_TOPIC}: {output}")
    except Exception as e:
        logger.error(f"Error processing message: {e}")
        sentry_sdk.capture_exception(e)

async def kafka_consumer_task():
    
    with sentry_sdk.start_transaction(
        op="kafka_consumer lifecycle",
        name="kafka_consumer_task",):
        consumer = KafkaConsumer(
            settings.KAFKA_INPUT_TOPIC,
            bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS,
            group_id=settings.KAFKA_CONSUMER_GROUP,
            auto_offset_reset='earliest',
            enable_auto_commit=True,
            value_deserializer=lambda x: x.decode('utf-8')
        )
        logger.info(f"Kafka consumer started for topic: {settings.KAFKA_INPUT_TOPIC}")

        while True:
            with sentry_sdk.start_span(op="kafka_poll", description="Kafka poll"):
                messages = consumer.poll(timeout_ms=1000)
            for tp, messages in messages.items():
                for message in messages:
                    asyncio.create_task(process_message(message))
            await asyncio.sleep(1)

async def start_kafka_consumer():

    asyncio.create_task(kafka_consumer_task())


