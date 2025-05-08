import json
import logging
from kafka import KafkaProducer
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from app.core.config import settings

logger = logging.getLogger(__name__)

producer = KafkaProducer(
    bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS,
    value_serializer=lambda v : json.dumps(v).encode('utf-8')
)

async def send_message_to_kafka(topic:str, message:dict):
    """
    produce message
    """
    try:
        future = producer.send(topic,message)
        result = future.get(timeout=10)
        logger.debug(f"Message sent to {topic}: {result}")
        return True
    except Exception as e:
        logger.error(f"Error sending message to Kafka: {e}")
        return False