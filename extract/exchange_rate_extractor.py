from datetime import date, datetime

import requests
import boto3
from decimal import Decimal
from bs4 import BeautifulSoup

from utils.constants import Constants
from utils.exchange_rate import ExchangeRate
from utils.exchange_tracking_exception import DataScrapperException, DataNotFoundException


class ExchangeRateExtractor:
    """
    Class will be responsible for extracting the forex information.
    """

    def __init__(self):
        self.url = Constants.EURO_EXCHANGE_RATES_URL
        self.__dynamo_db = boto3.client(Constants.DYNAMODB)

    def __scrape_forex_table(self) -> dict:
        f"""
        A helper function that will scrap the data from {Constants.EURO_EXCHANGE_RATES_URL}.
        
        :return: A dictionary containing forex information. 
        """

        # Parse the HTML content of the response using BeautifulSoup
        response = requests.get(self.url)
        soup = BeautifulSoup(response.content, Constants.HTML_PARSER)

        # Find the table on the page containing the exchange rates
        exchange_rates_table = soup.find(Constants.TABLE, {Constants.CLASS: Constants.FOREX_TABLE})

        return exchange_rates_table

    def __get_exchange_data_from_website(self) -> ExchangeRate:
        """
        A helper function that will apply a structure to forex data and returns it.

        :return: Exchange Rates from the website.
        """

        # Extract the exchange rates from the table
        exchange_rates = dict()

        raw_forex_table = self.__scrape_forex_table()

        for row in raw_forex_table.find_all(Constants.TR)[1:]:
            columns = row.find_all(Constants.TD)

            currency_code = columns[Constants.ExchangeRate.CURRENCY_CODE].text.strip()
            currency_name = columns[Constants.ExchangeRate.CURRENCY_NAME].text.strip()
            rate = columns[Constants.ExchangeRate.RATE].text.strip()

            exchange_rates[currency_code] = {Constants.RATE: rate, Constants.CURRENCY_NAME: currency_name}

        return ExchangeRate(rates=exchange_rates, date=date.today().strftime(Constants.DATE_FORMAT))

    def __get_date_specific_exchange_rate_from_db(self, _date: str) -> dict:
        f"""
        A helper function to get exchange rate of specific date stored in the database.
        
        :param _date: A string representation of date in {Constants.DATE_FORMAT} format. 
        
        :return: The exchange rate data.
        """

        query_params = {
            'TableName': Constants.DYNAMO_DB_TABLE_NAME,
            'KeyConditionExpression': f'{Constants.DATE} = :d',
            'ExpressionAttributeValues': {
                ':d': {'S': _date}
            }
        }

        # Query the table and get the item
        response = self.__dynamo_db.query(**query_params)

        if response.get(Constants.ITEMS, False):
            # Get the rates from the item
            return response['Items'][0]

        raise DataNotFoundException(_date)

    def __get_rates(self, _date: str, compare_with_previous_day: bool) -> list:
        """
        Returns the exchange rate.

        :param _date: (Optional) If specified then fetch the data for the date otherwise latest data will be fetched
                      from website.
        :param compare_with_previous_day: (Optional) If true then previous day comparison will be made.

        :return: the exchange rates information.
        """

        rates = self.__get_exchange_data_from_website() \
            if not _date else self.__get_date_specific_exchange_rate_from_db(_date)

        if compare_with_previous_day:
            exchange_rates_date = _date
            if not exchange_rates_date:
                exchange_rates_date = date.today().strftime(Constants.DATE_FORMAT)

            previous_day_date = (
                    datetime.datetime.strptime(exchange_rates_date, Constants.DATE_FORMAT)
                    - datetime.timedelta(days=1)
            ).strftime(Constants.DATE_FORMAT)

            previous_day_rates = self.__get_date_specific_exchange_rate_from_db(previous_day_date)\
                .get(Constants.RATES, dict())

            # Compare exchange rates and calculate percentage change
            for currency_code, rate in rates[Constants.RATES].items():
                if previous_day_rates:
                    previous_rate = Decimal(previous_day_rates.get(currency_code, dict()).get(Constants.RATE, 0.0))
                    percent_change = ((Decimal(rate[Constants.RATE]) - previous_rate) / previous_rate) * 100
                    rates[Constants.RATES][currency_code][Constants.PERCENT_CHANGE] = percent_change

        return rates

    def get_exchange_rates(self, _date=None, compare_with_previous_day=False):
        """
        Function visible for other classes to get the exchange rates data.

        :param _date: (Optional) If specified then fetch the data for the date otherwise latest data will be fetched
                      from website.
        :param compare_with_previous_day: (Optional) If true then previous day comparison will be made.

        :return: the exchange rates information.
        """

        try:

            return self.__get_rates(_date, compare_with_previous_day)

        except DataNotFoundException as no_data_exception:

            raise no_data_exception

        except Exception as error:

            raise DataScrapperException(error)


if __name__ == "__main__":
    print(ExchangeRateExtractor().get_exchange_rates())
