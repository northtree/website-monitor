import os
import time
from src.postgres import PGClient
from src.model import URLStatus

def test_pg_connect_database():
    pg_client = PGClient()
    assert pg_client.database == pg_client.current_database()

def test_insert():
    pg_client = PGClient()
    url_status = URLStatus('foo', 200, time.time_ns(), time.time_ns())
    pg_client.insert(url_status)
