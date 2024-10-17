import requests
import time
import datetime

def date_to_unix_timestamp(date_str):
    dt = datetime.datetime.strptime(date_str, "%Y-%m-%d")
    return int(time.mktime(dt.timetuple()))

def get_historical_data(stock_symbol, start_date, end_date, interval='1d'):
    period1 = date_to_unix_timestamp(start_date)
    period2 = date_to_unix_timestamp(end_date)
    historical_url = f'https://query2.finance.yahoo.com/v8/finance/chart/{stock_symbol}?period1={period1}&period2={period2}&interval={interval}&includePrePost=true&events=div%7Csplit%7Cearn&lang=en-US&region=US'

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
    }

    try:
        response = requests.get(historical_url, headers=headers)
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx and 5xx)

        data = response.json()
        chart_data = data['chart']['result'][0]
        timestamps = chart_data.get('timestamp', [])
        indicators = chart_data['indicators']['quote'][0]

        if not timestamps or not indicators:
            return {'error': 'No historical data available for the given range.'}

        historical_data = []
        for i in range(len(timestamps)):
            historical_data.append({
                'date': timestamps[i],
                'open': indicators['open'][i],
                'close': indicators['close'][i],
                'high': indicators['high'][i],
                'low': indicators['low'][i],
                'volume': indicators['volume'][i]
            })

        return historical_data
    except requests.exceptions.RequestException as e:
        return {'error': f'Failed to retrieve historical data. Error: {str(e)}'}
    except KeyError as e:
        return {'error': f'Missing expected data in the response. Error: {str(e)}'}
