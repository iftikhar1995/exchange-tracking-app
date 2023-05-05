from datetime import date

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

            rates = {
                Constants.RATE: columns[Constants.ExchangeRate.CURRENCY_CODE].text.strip(),
                Constants.CURRENCY_NAME: columns[Constants.ExchangeRate.CURRENCY_NAME].text.strip(),
                Constants.CURRENCY_CODE: columns[Constants.ExchangeRate.RATE].text.strip()
            }

            exchange_rates.append(rates)

        return ExchangeRate(rates=exchange_rates, date=date.today().strftime(Constants.DATE_FORMAT))

    def get_exchange_rates(self):

        try:

            return self.__parse_forex_data()

        except Exception as error:

            raise DataScrapperException(error)


if __name__ == "__main__":
    print(DataScrapper().get_exchange_rates())
