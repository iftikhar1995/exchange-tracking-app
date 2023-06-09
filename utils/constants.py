from enum import IntEnum


class Constants:
    EURO_EXCHANGE_RATES_URL = \
        "https://www.ecb.europa.eu/stats/policy_and_exchange_rates/euro_reference_exchange_rates/html/index.en.html"

    HTML_PARSER = "html.parser"
    TABLE = "table"
    CLASS = "class"
    FOREX_TABLE = "forextable"
    TD = "td"
    TR = "tr"
    ITEMS = "Items"

    class ExchangeRate(IntEnum):
        CURRENCY_CODE = 0
        CURRENCY_NAME = 1
        RATE = 2

    DATE = "date"
    CURRENCY_CODE = "currency_code"
    CURRENCY_NAME = "currency_name"
    RATES = "rates"
    RATE = "rate"
    PERCENT_CHANGE = "percent_change"
    COMPARE_PREVIOUS = "compare_previous"

    DATE_FORMAT = "%Y-%m-%d"

    DYNAMODB = "dynamodb"
    DYNAMO_DB_TABLE_NAME = "ExchangeRates"
