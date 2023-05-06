from utils.constants import Constants


class ExchangeTrackingException(Exception):

    def __init__(self, message: str, error: Exception):
        super().__init__(message)
        self.error = error


class DataScrapperException(ExchangeTrackingException):

    def __init__(self, exception: Exception):
        message = f"Unable to scrape data from {Constants.EURO_EXCHANGE_RATES_URL}."
        super().__init__(message, exception)


class DynamoDBWriterException(ExchangeTrackingException):

    def __init__(self, exception: Exception):
        message = f"Unable to load data into {Constants.TABLE}."
        super().__init__(message, exception)


class DataNotFoundException(ExchangeTrackingException):

    def __init__(self, date: str):
        message = f"Data not found for {date}. Please load the data first."
        super().__init__(message, None)


class InvalidDateException(ExchangeTrackingException):

    def __init__(self, date: str):
        message = \
            f"Invalid value of date. You have provided {date} but system is expecting date in {Constants.DATE_FORMAT}."
        super().__init__(message, None)


class InvalidComparePreviousException(ExchangeTrackingException):

    def __init__(self, compare_previous: str):
        message = f"""
            Invalid value of {Constants.COMPARE_PREVIOUS}.
            It can only be true or false instead you provided {compare_previous}."""

        super().__init__(message, None)


class InvalidRatesException(ExchangeTrackingException):

    def __init__(self):
        message = f"""
            Invalid value of {Constants.RATES}.
            Each object in it should have {Constants.RATE} and {Constants.CURRENCY_NAME} keys in it."""

        super().__init__(message, None)
