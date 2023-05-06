from datetime import datetime

from utils.constants import Constants
from utils.exchange_tracking_exception import InvalidDateException, InvalidComparePreviousException, \
    InvalidRatesException


class RequestParameterValidations:

    @staticmethod
    def validate_date(date: str):
        if date:
            try:
                datetime.strptime(date, Constants.DATE_FORMAT)
                return True
            except ValueError:
                raise InvalidDateException(date)
        return True

    @staticmethod
    def validate_compare_previous(compare_previous: str):
        if compare_previous:
            if isinstance(compare_previous, str) and compare_previous.lower() in ["true", "false"]:
                return True
            else:
                raise InvalidComparePreviousException(compare_previous)
        return True

    @staticmethod
    def validate_rates(rates: dict):

        for currency_code, rate in rates.items():
            if isinstance(currency_code, str) and rate.get(Constants.RATE, False) and rate.get(Constants.CURRENCY_NAME, False):
                pass
            else:
                raise InvalidRatesException()

        return True
