from typing import Optional

def get_mac_address(
    interface: Optional[str] = None,
    ip: Optional[str] = None,
    ip6: Optional[str] = None,
    hostname: Optional[str] = None,
    network_request: bool = True,
) -> Optional[str]: ...
