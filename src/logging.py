import sys
import json

from .kafka import Consumer
from .postgres import PGClient
from .model import URLStatus


if __name__ == '__main__':
    try:
        kafka_consumer = Consumer()
        pg_client = PGClient()

        # TODO: change to subscript
        # TODO: try https://github.com/aio-libs/aiokafka
        while True:
            msg = kafka_consumer.consume()
            if msg:
                print(msg.decode('utf-8'))
                url_status = URLStatus(**json.loads(msg.decode('utf-8')))
                # print(url_status)
                pg_client.insert(url_status)


    except KeyboardInterrupt:
        print('Ctrl+C to exit...')
        sys.exit()
