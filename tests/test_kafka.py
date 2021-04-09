import uuid
from src.kafka import Producer, Consumer


def test_kafka_message():
    """Verify message value between Producer and Consumer.
    """
    test_topic = 'test'
    send_msg = f'hello world {uuid.uuid4().hex}'
    print(f'{send_msg=}')
    kafka_producer = Producer(topic=test_topic)
    kafka_producer.produce(send_msg.encode('utf-8'))

    kafka_consumer = Consumer(topic=test_topic)
    consumer_msg = kafka_consumer.consume()
    if consumer_msg:
        recv_msg = consumer_msg.decode('utf-8')
        print(f'{recv_msg=}')
        assert send_msg == recv_msg
