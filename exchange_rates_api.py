from flask import Flask, jsonify, request

from extract.data_scrapper import DataScrapper
from load.dynamodb_writer import DynamoDBWriter
from utils.constants import Constants
from utils.exchange_rate import ExchangeRate

app = Flask(__name__)


@app.route('/api/exchange-rates', methods=['GET'])
def get_exchange_rates():

    # Return the exchange rates as a JSON response
    return jsonify(DataScrapper().get_exchange_rates()), 200


@app.route('/api/save-exchange-rates', methods=['POST'])
def save_exchange_rates():

    input_data = request.get_json()
    rates = input_data[Constants.RATES]
    _date = input_data[Constants.DATE]
    exchange_rates = ExchangeRate(date=_date, rates=rates)

    DynamoDBWriter(exchange_rates).write()

    # Return the exchange rates as a JSON response
    return jsonify({'message': 'Exchange rates saved successfully.'}), 200


if __name__ == '__main__':
    app.run(debug=True)
