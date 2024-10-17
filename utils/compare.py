import requests
from bs4 import BeautifulSoup
from .stock_info import get_stock_info
from .quote_data import get_quote_data
from .historical_data import get_historical_data
from .industry_info import get_company_sector_and_industry

def compare_companies(stock_symbol, num_companies=5, include_historical=False):
    sector_and_industry_data = get_company_sector_and_industry(stock_symbol)
    if not sector_and_industry_data or 'error' in sector_and_industry_data:
        return {'error': 'Failed to retrieve sector and industry data for the given company.'}

    industry_link = sector_and_industry_data['industry_link']
    search_url = f'https://finance.yahoo.com{industry_link}'

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
    }

    try:
        response = requests.get(search_url, headers=headers)
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx and 5xx)

        soup = BeautifulSoup(response.text, 'html.parser')
        table_container = soup.find('div', class_='table-container yf-1y4urt9')
        if table_container:
            rows = table_container.find_all('tr')[1:num_companies+1]  # Skip the header row and limit to num_companies
            companies = []
            for row in rows:
                columns = row.find_all('td')
                if len(columns) >= 2:
                    symbol = columns[0].find('span', class_='symbol').get_text(strip=True)
                    name = columns[0].find('span', class_='longName').get_text(strip=True)
                    companies.append({'symbol': symbol, 'name': name})

            comparison_data = []
            for company in companies:
                company_data = {}
                stock_info = get_stock_info(company['symbol'])
                if 'error' not in stock_info:
                    company_data['stock_info'] = stock_info

                quote_data = get_quote_data(company['symbol'])
                if 'error' not in quote_data:
                    company_data['quote_data'] = quote_data

                if include_historical:
                    historical_data = get_historical_data(company['symbol'], '2023-01-01', '2023-12-31')
                    if 'error' not in historical_data:
                        company_data['historical_data'] = historical_data

                company_data['symbol'] = company['symbol']
                comparison_data.append(company_data)

            return comparison_data
        else:
            return {'error': 'No companies found in the same industry.'}
    except requests.exceptions.RequestException as e:
        return {'error': f'Failed to retrieve companies data. Error: {str(e)}'}
