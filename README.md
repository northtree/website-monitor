# Website Monitor
> 👀 Simple website monitor via aiohttp + kafka + postgresql 



## Prerequisite
### Installation
> poetry install

### Environment Vars
```
export KAFKA_URI='***'
export KAFKA_SSL_KEYFILE='conf/service.key'
export KAFKA_SSL_CERTFILE='conf/service.cert'
export KAFKA_SSL_CAFILE='conf/ca.pem'
export KAFKA_TOPIC='website-monitor'

export PG_URI='***'
export PG_DATABASE='website-monitor'
export PG_TABLE='logs'
```

## Run
### monitor
Periodic requesting given URLs and produce URL Status into Kafka.

> python -m src.monitor

or 

> python -m src.monitor -l top.list -i 2 -c 1

> python -m src.monitor --help 
```
Usage: monitor.py [OPTIONS]

Options:
  -l, --urls TEXT         URLs file to monitor
  -i, --interval INTEGER  Periodic interval in seconds
  -c, --count INTEGER     Periodic counts in this run
  --help                  Show this message and exit.
```

### logging
Consuming Kafka message and save into PostgreSQL.

> python -m src.logging


#### table
```
 id  |               url                | status |     start_time      |      end_time       
-----+----------------------------------+--------+---------------------+---------------------
 383 | https://httpbin.org/delay/2      |    200 | 1618049751369818000 | 1618049754355952000
 382 | https://httpbin.org/delay/1      |    200 | 1618049751369370000 | 1618049753310107000
 381 | https://httpbin.org/status/500   |    500 | 1618049751368899000 | 1618049752363546000
 380 | https://httpbin.org/status/200   |    200 | 1618049751366424000 | 1618049752343412000
 379 | https://httpbin.org/status/300   |    300 | 1618049751367437000 | 1618049752323979000
 378 | https://httpbin.org/status/400   |    400 | 1618049751368099000 | 1618049752304502000
 377 | https://google.com               |    200 | 1618049751370261000 | 1618049751913038000
```

## Features

* Use [aiohttp](https://github.com/aio-libs/aiohttp) as asynchronous HTTP client 
* Package management by [poetry](https://github.com/python-poetry/poetry)
* Linting by [pylint](https://github.com/PyCQA/pylint)
* Unit Testing by [pytest](https://github.com/pytest-dev/pytest)
* CLI configuration by [click](https://github.com/pallets/click)
* CI via [GitHub Actions](https://github.com/northtree/website-monitor/actions)
* Use [psycopg2.sql](https://www.psycopg.org/docs/sql.html) module to generate SQL statements in safe way to avoid SQL injection 
* Define `URLStatus` structure using [dataclass](https://docs.python.org/3/library/dataclasses.html)
* Follow [PEP526](https://www.python.org/dev/peps/pep-0526/) for type annotation
* Mockup request status and delay from [httpbin.org](httpbin.org)
* Use `__enter__` and `__exit__` to [manage resources in Pythonic way](https://alysivji.github.io/managing-resources-with-context-managers-pythonic.html)


## TODOs
* Design `scheduler` before `monitor` to support different `interval`
* Plugin `parser` to extract content by regex
* Replace [kafka-python](https://github.com/dpkp/kafka-python) with [aiokafka](https://github.com/aio-libs/aiokafka)
* Replace [psycopg2](https://github.com/psycopg/psycopg2) with [asyncpg](https://github.com/MagicStack/asyncpg)
* More Unit Tests and coverage report
* Dockerized
