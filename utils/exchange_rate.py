from dataclasses import dataclass, asdict


@dataclass
class ExchangeRate:
    """Class for holding exchange rates data."""

    rates: dict()
    date: str

    def to_dict(self):
        return asdict(self)

