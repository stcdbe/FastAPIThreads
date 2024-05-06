from dataclasses import asdict, dataclass, field
from typing import Any
from uuid import UUID, uuid4


@dataclass
class AbstractEntity:
    guid: UUID = field(default_factory=uuid4, kw_only=True)

    def dump_to_dict(self) -> dict[str, Any]:
        return asdict(self)
