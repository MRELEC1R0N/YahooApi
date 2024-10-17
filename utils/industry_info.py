import requests
from bs4 import BeautifulSoup

def get_company_sector_and_industry(stock_symbol):
    stock_url = f'https://finance.yahoo.com/quote/{stock_symbol}/profile'

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
    }

    try:
        response = requests.get(stock_url, headers=headers)
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx and 5xx)

        soup = BeautifulSoup(response.text, 'html.parser')
        # Look for the sector and industry information in the profile page
        sector_element = soup.find('a', {'data-ylk': 'elm:itm;elmt:link;itc:0;sec:qsp-company-overview;subsec:profile;slk:Technology'})
        industry_element = soup.find('a', {'data-ylk': 'elm:itm;elmt:link;itc:0;sec:qsp-company-overview;subsec:profile;slk:Consumer%20Electronics'})

        if sector_element and industry_element:
            sector = sector_element.get_text(strip=True)
            sector_link = sector_element['href']
            industry = industry_element.get_text(strip=True)
            industry_link = industry_element['href']
            return {
                'sector': sector,
                'sector_link': sector_link,
                'industry': industry,
                'industry_link': industry_link
            }
        else:
            return {'error': 'Sector or industry information not found.'}
    except requests.exceptions.RequestException as e:
        return {'error': f'Failed to retrieve sector and industry data. Error: {str(e)}'}
    except AttributeError:
        return {'error': 'Failed to parse sector and industry data. The structure of the Yahoo Finance page may have changed.'}

# Test the function
if __name__ == "__main__":
    stock_symbol = "AAPL"
    sector_and_industry_data = get_company_sector_and_industry(stock_symbol)
    if 'error' not in sector_and_industry_data:
        print(f"Sector: {sector_and_industry_data['sector']}")
        print(f"Sector Link: {sector_and_industry_data['sector_link']}")
        print(f"Industry: {sector_and_industry_data['industry']}")
        print(f"Industry Link: {sector_and_industry_data['industry_link']}")
    else:
        print(sector_and_industry_data['error'])
