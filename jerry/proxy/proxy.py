from functools import partial

import yaml
import attr
from yaml.dumper import SafeDumper
from yaml.representer import SafeRepresenter


@attr.s
class Proxy(object):
    url: str = attr.ib()
    pos: int = attr.ib(default=0)
    neg: int = attr.ib(default=0)


class ProxyRepresenter(SafeRepresenter):
    def represent_proxy(self, proxy_obj):
        data = attr.asdict(proxy_obj)
        return self.represent_mapping('tag:yaml.org,2002:map', data)


ProxyRepresenter.add_representer(Proxy, ProxyRepresenter.represent_proxy)


class ProxyDumper(SafeDumper, ProxyRepresenter):
    pass


proxy_dump = partial(yaml.dump, default_flow_style=False, Dumper=ProxyDumper)
