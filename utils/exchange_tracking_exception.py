from utils.constants import Constants


class ExchangeTrackingException(Exception):

    def __init__(self, message: str, error: Exception):
        super().__init__(message)
        self.error = error


class DataScrapperException(ExchangeTrackingException):

    def __init__(self, exception: Exception):
        message = f"Unable to scrape data from {Constants.EURO_EXCHANGE_RATES_URL}."
        super().__init__(message, exception)
