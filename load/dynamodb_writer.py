import boto3

from utils.constants import Constants
from utils.exchange_rate import ExchangeRate
from utils.exchange_tracking_exception import DynamoDBWriterException


class DynamoDBWriter:
    """
    This class will be responsible for writing forex data in DynamoDB.
    """

    def __init__(self, exchange_rates: ExchangeRate):

        self.__dynamodb = boto3.resource(Constants.DYNAMODB)
        self.__table = self.__dynamodb.Table(Constants.DYNAMO_DB_TABLE_NAME)
        self.__exchange_rates = exchange_rates.to_dict()

    def __put_item(self) -> None:

        self.__dynamodb.put_item(
            TableName=Constants.DYNAMO_DB_TABLE_NAME,
            Item=self.__exchange_rates
        )

    def write(self) -> None:
        """
        This method will be visible to the outside classes and is responsible for writing the data into db.
        """

        try:

            self.__put_item()

        except Exception as error:

            raise DynamoDBWriterException(error)
