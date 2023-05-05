import boto3

from utils.constants import Constants
from utils.exchange_rate import ExchangeRate
from utils.exchange_tracking_exception import DynamoDBWriterException


class DynamoDBWriter:

    def __init__(self, exchange_rates: list[ExchangeRate]):

        self.__dynamodb = boto3.resource('dynamodb')
        self.__table = self.__dynamodb .Table('')
        self.__exchange_rates = exchange_rates

    def __batch_writer(self):

        with self.__table.batch_writer() as batch:

            for exchange_rate in self.__exchange_rates:

                item = {
                    Constants.CURRENCY_CODE: exchange_rate.currency_code,
                    Constants.CURRENCY_NAME: exchange_rate.currency_name,
                    Constants.RATE: exchange_rate.rate
                }

                batch.put_item(Item=item)

    def write(self):

        try:

            self.__batch_writer()

        except Exception as error:

            raise DynamoDBWriterException(error)
