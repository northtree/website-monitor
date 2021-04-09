from dataclasses import dataclass, astuple, asdict
import json


@dataclass
class URLStatus:
    url: str
    status: int # response HTTP Status
    start: int  # start request time (nanoseconds)
    end: int    # end response time (nanoseconds)

    def to_tuple(self):
        return astuple(self)

    def to_bytes(self):
        return json.dumps(asdict(self)).encode('utf-8')

    def to_msgpack(self):
        # TODO
        pass

