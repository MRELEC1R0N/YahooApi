import requests
from bs4 import BeautifulSoup

def get_quote_data(stock_symbol):
    stock_url = f'https://finance.yahoo.com/quote/{stock_symbol}'

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
    }

    try:
        response = requests.get(stock_url, headers=headers)
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx and 5xx)

        soup = BeautifulSoup(response.text, 'html.parser')
        quote_data = {}

        # Extract quote information
        name_element = soup.find('h1', {'class': 'D(ib) Fz(18px)'})
        price_element = soup.find('fin-streamer', {'data-field': 'regularMarketPrice'})
        price_change_element = soup.find('fin-streamer', {'data-field': 'regularMarketChange'})
        price_change_percent_element = soup.find('fin-streamer', {'data-field': 'regularMarketChangePercent'})
        pre_market_price_element = soup.find('fin-streamer', {'data-field': 'preMarketPrice'})
        pre_market_change_element = soup.find('fin-streamer', {'data-field': 'preMarketChange'})
        pre_market_change_percent_element = soup.find('fin-streamer', {'data-field': 'preMarketChangePercent'})

        if name_element:
            quote_data['name'] = name_element.get_text()
        if price_element:
            quote_data['price'] = price_element.find('span').get_text()
        if price_change_element:
            quote_data['price_change'] = price_change_element.find('span').get_text()
        if price_change_percent_element:
            quote_data['price_change_percent'] = price_change_percent_element.find('span').get_text()
        if pre_market_price_element:
            quote_data['pre_market_price'] = pre_market_price_element.find('span').get_text()
        if pre_market_change_element:
            quote_data['pre_market_change'] = pre_market_change_element.find('span').get_text()
        if pre_market_change_percent_element:
            quote_data['pre_market_change_percent'] = pre_market_change_percent_element.find('span').get_text()

        return quote_data
    except requests.exceptions.RequestException as e:
        return {'error': f'Failed to retrieve quote data. Error: {str(e)}'}
    except AttributeError:
        return {'error': 'Failed to parse quote data. The structure of the Yahoo Finance page may have changed.'}
