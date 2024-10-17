import requests
from bs4 import BeautifulSoup

def search_stock_name(stock_name):
    search_url = f'https://finance.yahoo.com/lookup?s={stock_name}'

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
    }

    try:
        response = requests.get(search_url, headers=headers)
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx and 5xx)

        soup = BeautifulSoup(response.text, 'html.parser')
        stock_table = soup.find('table', {'class': 'W(100%)'})
        if stock_table:
            rows = stock_table.find_all('tr')[1:11]
            stocks = []
            for i, row in enumerate(rows, 1):
                columns = row.find_all('td')
                if len(columns) >= 2:
                    symbol = columns[0].get_text()
                    name = columns[1].get_text()
                    stocks.append({'symbol': symbol, 'name': name})
            return stocks
        else:
            return {'error': 'No stocks found with that name.'}
    except requests.exceptions.RequestException as e:
        return {'error': f'Failed to retrieve search results. Error: {str(e)}'}
