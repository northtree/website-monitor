import os
from typing import Union

from kafka import KafkaProducer, KafkaConsumer
from kafka.errors import KafkaConnectionError, KafkaTimeoutError, KafkaError

# Adapted from Aiven Kafka Tutorial
# Credit: https://help.aiven.io/en/articles/489572-getting-started-with-aiven-for-apache-kafka


class Producer:
    def __init__(self, server: str=None, topic: str=None):
        self.server = server or os.environ.get('KAFKA_URI')
        self.topic = topic or os.environ.get('KAFKA_TOPIC')
        self.producer = None

        try:
            self.producer = KafkaProducer(
                bootstrap_servers=self.server,
                security_protocol='SSL',
                ssl_keyfile=os.environ.get('KAFKA_SSL_KEYFILE'),
                ssl_certfile=os.environ.get('KAFKA_SSL_CERTFILE'),
                ssl_cafile=os.environ.get('KAFKA_SSL_CAFILE'),
            )
        except (KafkaConnectionError, KafkaError) as e:
            print(f'Error to connect Kafka: {e}')
            raise e

    def __enter__(self):
        print('Enter Kafka Producer')
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print('Exit Kafka Producer')
        if self.producer:
            self.producer.close()

    def produce(self, message: bytes):
        """Send message to given Kafka topic.

        Args:
            message (bytes): message value in bytes
        """
        try:
            self.producer.send(self.topic, message)
            self.producer.flush()
        except KafkaTimeoutError as e:
            print(f'Cannot publish message: {e}')


class Consumer:
    def __init__(self, server: str=None, topic: str=None):
        self.server = server or os.environ.get('KAFKA_URI')
        self.topic = topic or os.environ.get('KAFKA_TOPIC')
        self.consumer = None

        try:
            self.consumer = KafkaConsumer(
                self.topic,
                auto_offset_reset='earliest',
                client_id='demo-client-1',
                group_id='demo-group',
                bootstrap_servers=self.server,
                security_protocol='SSL',
                ssl_keyfile=os.environ.get('KAFKA_SSL_KEYFILE'),
                ssl_certfile=os.environ.get('KAFKA_SSL_CERTFILE'),
                ssl_cafile=os.environ.get('KAFKA_SSL_CAFILE'),
            )
        except (KafkaConnectionError, KafkaError) as e:
            print(f'Error to connect Kafka: {e}')
            raise e

    def __enter__(self):
        print('Enter Kafka Consumer')
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print('Exit Kafka Consumer')
        if self.consumer:
            self.consumer.close()

    def consume(self) -> Union[bytes, None]:
        """Consume one message from given Kafka topic.

        Returns:
            bytes: message value
        """
        try:
            msg_pack = self.consumer.poll(timeout_ms=10000, max_records=1)
            # print(msg_pack)
            message = None
            for _, records in msg_pack.items():
                if records is None:
                    return None
                message = records[0].value
            self.consumer.commit()
            return message
        except KafkaError as e:
            print(f'Cannot poll message from Kafka topic: {e}')
            return None

    def subscript(self):
        # TODO
        pass
