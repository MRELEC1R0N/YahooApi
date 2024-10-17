import requests
from bs4 import BeautifulSoup
import json

def extract_stock_info(soup):
    stock_info = {}

    # Extract stock exchange and currency
    exchange_info = soup.find('span', class_='exchange yf-wk4yba')
    if exchange_info:
        exchange_text = exchange_info.get_text(strip=True)
        stock_info['Exchange Info'] = exchange_text

    # Extract stock name and symbol
    stock_name = soup.find('h1', class_='yf-xxbei9')
    if stock_name:
        stock_name_text = stock_name.get_text(strip=True)
        stock_info['Stock Name'] = stock_name_text

    # Extract current price
    current_price = soup.find('fin-streamer', {'data-field': 'regularMarketPrice'})
    if current_price:
        current_price_text = current_price.get_text(strip=True)
        stock_info['Current Price'] = current_price_text

    # Extract price change
    price_change = soup.find('fin-streamer', {'data-field': 'regularMarketChange'})
    if price_change:
        price_change_text = price_change.get_text(strip=True)
        stock_info['Price Change'] = price_change_text

    # Extract price change percentage
    price_change_percent = soup.find('fin-streamer', {'data-field': 'regularMarketChangePercent'})
    if price_change_percent:
        price_change_percent_text = price_change_percent.get_text(strip=True)
        stock_info['Price Change Percent'] = price_change_percent_text

    # Extract after hours price
    after_hours_price = soup.find('fin-streamer', {'data-field': 'postMarketPrice'})
    if after_hours_price:
        after_hours_price_text = after_hours_price.get_text(strip=True)
        stock_info['After Hours Price'] = after_hours_price_text

    # Extract after hours price change
    after_hours_price_change = soup.find('fin-streamer', {'data-field': 'postMarketChange'})
    if after_hours_price_change:
        after_hours_price_change_text = after_hours_price_change.get_text(strip=True)
        stock_info['After Hours Price Change'] = after_hours_price_change_text

    # Extract after hours price change percentage
    after_hours_price_change_percent = soup.find('fin-streamer', {'data-field': 'postMarketChangePercent'})
    if after_hours_price_change_percent:
        after_hours_price_change_percent_text = after_hours_price_change_percent.get_text(strip=True)
        stock_info['After Hours Price Change Percent'] = after_hours_price_change_percent_text

    # Extract additional information from the container div
    container_div = soup.find('div', class_='container yf-mrt107')
    if container_div:
        for item in container_div.find_all('li'):
            label = item.find('span', class_='label yf-mrt107').get_text(strip=True)
            value = item.find('span', class_='value yf-mrt107')
            if value.find('fin-streamer'):
                value_text = value.find('fin-streamer').get_text(strip=True)
            else:
                value_text = value.get_text(strip=True)
            stock_info[label] = value_text

    return stock_info

def get_stock_info(stock_symbol):
    url = f'https://finance.yahoo.com/quote/{stock_symbol}'

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx and 5xx)

        soup = BeautifulSoup(response.text, 'html.parser')
        stock_info = extract_stock_info(soup)

        return stock_info
    except requests.exceptions.RequestException as e:
        return {'error': f'Failed to retrieve stock information. Error: {str(e)}'}
    except AttributeError:
        return {'error': 'Failed to parse stock information. The structure of the Yahoo Finance page may have changed.'}
