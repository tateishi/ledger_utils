from dataclasses import dataclass


@dataclass
class Meta:
    name: str
    value: str | None
