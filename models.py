from dataclasses import dataclass
from typing import Optional


@dataclass
class Device:
    device_id: str
    name: Optional[str] = None
    model: Optional[str] = None
    android_version: Optional[str] = None
    battery: Optional[int] = None
    online: bool = False
    last_seen: Optional[str] = None
