import requests
from bs4 import BeautifulSoup

def get_third_href_link(stock_symbol, class_name):
    stock_url = f'https://finance.yahoo.com/quote/{stock_symbol}'

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
    }

    try:
        response = requests.get(stock_url, headers=headers)
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx and 5xx)

        soup = BeautifulSoup(response.text, 'html.parser')
        # Find the div with the specified class name
        div_element = soup.find('div', class_=class_name)
        if div_element:
            links = div_element.find_all('a', href=True)
            if len(links) >= 3:
                return links[2]['href']
            else:
                return {'error': 'Less than 3 href links found.'}
        else:
            return {'error': f'No element found with class name: {class_name}'}
    except requests.exceptions.RequestException as e:
        return {'error': f'Failed to retrieve data. Error: {str(e)}'}
    except AttributeError:
        return {'error': 'Failed to parse data. The structure of the Yahoo Finance page may have changed.'}

# Test the function
if __name__ == "__main__":
    stock_symbol = "TSLA"
    class_name = "yf-kznos4"
    third_href_link = get_third_href_link(stock_symbol, class_name)
    if 'error' not in third_href_link:
        print("Third href link:", third_href_link)
    else:
        print(third_href_link['error'])
