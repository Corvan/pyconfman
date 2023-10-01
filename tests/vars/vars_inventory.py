import dataclasses
from dataclasses import dataclass, field
import ipaddress
from typing import Union, Optional

from pyconfman.models.inventory import Group, Host


@dataclass(init=True)
class TestHost(Host):

    ip_interface: Optional[
        Union[ipaddress.IPv4Interface, ipaddress.IPv6Interface]
    ] = field(default=None, kw_only=True)

    def __hash__(self):
        return super().__hash__()


host1 = TestHost(
    name="host1.example.com", ip_interface=ipaddress.ip_interface("0.0.0.0/32")
)
host2 = TestHost(
    name="host2.example.com", ip_interface=ipaddress.ip_interface("fd01:0:0:1::1/64")
)
group1 = Group("group1", {host1, host2})
group2 = Group("group2", {group1, host1})
host3 = TestHost("Test")
