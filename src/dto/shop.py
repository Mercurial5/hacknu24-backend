from dataclasses import dataclass, asdict


@dataclass
class ShopDTO:
    id: str
    name: str

    def dict(self) -> dict:
        return asdict(self)
