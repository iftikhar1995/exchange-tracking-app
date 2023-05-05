from datetime import date

import boto3

from utils.constants import Constants
from utils.exchange_rate import ExchangeRate
from utils.exchange_tracking_exception import DynamoDBWriterException


class DynamoDBWriter:

    def __init__(self, exchange_rates: ExchangeRate):

        self.__dynamodb = boto3.resource(Constants.DYNAMODB)
        self.__table = self.__dynamodb.Table(Constants.DESTINATION_TABLE)
        self.__exchange_rates = exchange_rates.to_dict()

    def __put_item(self):

        self.__dynamodb.put_item(
            TableName=Constants.DESTINATION_TABLE,
            Item=self.__exchange_rates
        )

    def write(self):

        try:

            self.__put_item()

        except Exception as error:

            raise DynamoDBWriterException(error)
