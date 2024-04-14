from dataclasses import dataclass, field, asdict
from datetime import datetime


@dataclass
class OfferDTO:
    category: str
    shop: str
    bank: str
    bonus: int
    updated_at: datetime
    is_beneficial: bool = field(default=False)
    conditions: list[str] = field(default_factory=list)

    def dict(self) -> dict:
        return {k: str(v) if isinstance(v, datetime) else v for k, v in asdict(self).items()}
