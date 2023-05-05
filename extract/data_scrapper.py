import requests
from bs4 import BeautifulSoup

from utils.constants import Constants
from utils.exchange_rate import ExchangeRate
from utils.exchange_tracking_exception import DataScrapperException


class DataScrapper:

    def __init__(self):
        self.url = Constants.EURO_EXCHANGE_RATES_URL
        self.__raw_forex_table = self.__get_raw_forex_table()

    def __get_raw_forex_table(self):

        # Parse the HTML content of the response using BeautifulSoup
        response = requests.get(self.url)
        soup = BeautifulSoup(response.content, Constants.HTML_PARSER)

        # Find the table on the page containing the exchange rates
        exchange_rates_table = soup.find(Constants.TABLE, {Constants.CLASS: Constants.FOREX_TABLE})

        return exchange_rates_table

    def __parse_forex_data(self):

        # Extract the exchange rates from the table
        exchange_rates = list()

        for row in self.__raw_forex_table.find_all(Constants.TR)[1:]:

            columns = row.find_all(Constants.TD)

            exchange_rate = ExchangeRate(
                currency_code=columns[Constants.ExchangeRate.CURRENCY_CODE].text.strip(),
                currency_name=columns[Constants.ExchangeRate.CURRENCY_NAME].text.strip(),
                rate=float(columns[Constants.ExchangeRate.RATE].text.strip())
            )

            exchange_rates.append(exchange_rate)

        return exchange_rates

    def get_exchange_rates(self):

        try:

            return self.__parse_forex_data()

        except Exception as error:

            raise DataScrapperException(error)


if __name__ == "__main__":
    print(DataScrapper().get_exchange_rates())
