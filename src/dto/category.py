from dataclasses import dataclass, asdict


@dataclass
class CategoryDTO:
    id: int
    name: str

    def dict(self) -> dict:
        return asdict(self)