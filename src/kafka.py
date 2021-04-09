import os
from typing import List

from kafka import KafkaProducer, KafkaConsumer
from kafka.errors import KafkaConnectionError, KafkaTimeoutError, KafkaError

# Adapted from Aiven Kafka Tutorial
# Credit: https://help.aiven.io/en/articles/489572-getting-started-with-aiven-for-apache-kafka

class Producer:
    def __init__(self, server: str=None, topic: str=None):
        self.server = server or os.environ.get('KAFKA_URI')
        self.topic = topic or os.environ.get('KAFKA_TOPIC')

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

    def __del__(self):
        print('Deleting Kafka Producer...')
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

    def __del__(self):
        print('Deleting Kafka Consumer...')
        self.consumer.close()

    def consume(self) -> bytes:
        """Consume one message from given Kafka topic.

        Returns:
            bytes: message value
        """
        try:
            msg_pack = self.consumer.poll(timeout_ms=10000, max_records=1)
            # print(msg_pack)
            message = None
            for tp, records in msg_pack.items():
                if records is None:
                    return
                message = records[0].value
            self.consumer.commit()
            return message
        except KafkaError as e:
            print(f'Cannot poll message from Kafka topic: {e}')

    def subscript(self):
        # TODO
        pass
