from flask import Flask, jsonify, request

from extract.exchange_rate_extractor import ExchangeRateExtractor
from load.dynamodb_writer import DynamoDBWriter
from utils.constants import Constants
from utils.exchange_rate import ExchangeRate
from utils.exchange_tracking_exception import ExchangeTrackingException
from validations.request_parameter_validations import RequestParameterValidations

app = Flask(__name__)


@app.route('/api/exchange-rates', methods=['GET'])
def get_exchange_rates():
    f"""
    API to get the exchange rates information.
    
    @:parameter date: The date for which the exchange rate information needed. It should be in {Constants.DATE_FORMAT} 
                      format. If not specified, then it will provide the latest information.
    @:type str
    @:parameter compare_previous: If specified, then it will show the information with the comparison of previous date.
    @:type str
    :returns: The forex exchange rate information. 
    """
    _date = request.args.get(Constants.DATE, None)
    compare_previous = request.args.get(Constants.COMPARE_PREVIOUS, None)
    print(_date)

    # Performing query parameters validation
    try:
        RequestParameterValidations.validate_date(_date)
        RequestParameterValidations.validate_compare_previous(compare_previous)
    except ExchangeTrackingException as validation_error:
        return jsonify(str(validation_error)), 422

    try:
        # Return the exchange rates as a JSON response
        return jsonify(ExchangeRateExtractor().get_exchange_rates(_date, bool(compare_previous))), 200
    except ExchangeTrackingException as error:
        return jsonify(str(error)), 500


@app.route('/api/exchange-rates', methods=['POST'])
def save_exchange_rates():
    """
    Save the exchange rates into DB.

    @:parameter date: The date of the exchange rates.
    @:type str
    @:parameter rates: The rate information
    @:type dict

    :return: confirmation that data saved successfully or not.
    """
    input_data = request.get_json()
    rates = input_data.get(Constants.RATES, dict())
    _date = input_data.get(Constants.DATE, None)

    # Performing query parameters validation
    try:
        RequestParameterValidations.validate_date(_date)
        RequestParameterValidations.validate_rates(rates)
    except ExchangeTrackingException as validation_error:
        return jsonify(str(validation_error)), 422

    # Saving exchange rates into DB
    try:

        exchange_rates = ExchangeRate(date=_date, rates=rates)
        DynamoDBWriter(exchange_rates).write()
        return jsonify({'message': 'Exchange rates saved successfully.'}), 200

    except ExchangeTrackingException as error:
        return jsonify(str(error)), 500


if __name__ == '__main__':
    app.run(debug=True)
