import asyncio
from app.kafka.consumer import start_kafka_consumer

if __name__ == "__main__":
    asyncio.run(start_kafka_consumer())