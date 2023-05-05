from dataclasses import dataclass


@dataclass
class ExchangeRate:
    """Class for holding exchange rates data."""
    currency_code: str
    currency_name: str
    rate: float
