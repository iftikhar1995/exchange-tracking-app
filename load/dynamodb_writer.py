from datetime import date

import boto3

from utils.constants import Constants
from utils.exchange_rate import ExchangeRate
from utils.exchange_tracking_exception import DynamoDBWriterException


class DynamoDBWriter:

    def __init__(self, exchange_rates: list[ExchangeRate]):

        self.__dynamodb = boto3.resource(Constants.DYNAMODB)
        self.__table = self.__dynamodb .Table(Constants.DESTINATION_TABLE)
        self.__exchange_rates = exchange_rates

    def __batch_writer(self):

        with self.__table.batch_writer() as batch:

            for exchange_rate in self.__exchange_rates:
                batch.put_item(Item=exchange_rate.to_dict())

    def write(self):

        try:

            self.__batch_writer()

        except Exception as error:

            raise DynamoDBWriterException(error)
