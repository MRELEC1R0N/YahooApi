from flask import Flask, request, jsonify
from utils.search import search_stock_name
from utils.stock_info import get_stock_info
from utils.historical_data import get_historical_data
from utils.quote_data import get_quote_data
from utils.compare import compare_companies

app = Flask(__name__)

@app.route('/search', methods=['GET'])
def search():
    company_name = request.args.get('company')
    if not company_name:
        return jsonify({'error': 'Company name is required'}), 400

    results = search_stock_name(company_name)
    return jsonify(results)

@app.route('/stock', methods=['GET'])
def stock_info():
    stock_symbol = request.args.get('symbol')
    if not stock_symbol:
        return jsonify({'error': 'Stock symbol is required'}), 400

    info = get_stock_info(stock_symbol)
    return jsonify(info)

@app.route('/historical', methods=['GET'])
def historical_data():
    stock_symbol = request.args.get('symbol')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    interval = request.args.get('interval', '1d')  # Default to 1 day if not provided

    if not stock_symbol or not start_date or not end_date:
        return jsonify({'error': 'Stock symbol, start date, and end date are required'}), 400

    data = get_historical_data(stock_symbol, start_date, end_date, interval)
    return jsonify(data)

@app.route('/quote', methods=['GET'])
def quote_data():
    stock_symbol = request.args.get('symbol')
    if not stock_symbol:
        return jsonify({'error': 'Stock symbol is required'}), 400

    data = get_quote_data(stock_symbol)
    return jsonify(data)

@app.route('/compare', methods=['GET'])
def compare():
    stock_symbol = request.args.get('symbol')
    num_companies = int(request.args.get('num_companies', 5))  # Default to 5 if not provided
    include_historical = request.args.get('include_historical', 'false').lower() == 'true'

    if not stock_symbol:
        return jsonify({'error': 'Stock symbol is required'}), 400

    data = compare_companies(stock_symbol, num_companies, include_historical)
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
