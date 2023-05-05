from dataclasses import dataclass, asdict
from datetime import date


@dataclass
class ExchangeRate:
    """Class for holding exchange rates data."""
    currency_code: str
    currency_name: str
    rate: float
    date: str = date.today().isoformat()

    def to_dict(self):
        return {k: str(v) for k, v in asdict(self).items()}
