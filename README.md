# Stock Market Analysis API

## 📈 Introduction

The Stock Market Analysis API provides a set of endpoints to retrieve and compare financial data for various companies. This API allows users to search for stock names, get detailed stock information, retrieve historical data, get real-time quote data, and compare companies within the same industry.

## 🚀 Features

- Search for stock names by company name.
- Retrieve detailed stock information.
- Get historical stock data.
- Fetch real-time quote data.
- Compare companies within the same industry.

## 🛠️ Installation

1. **Clone the repository:**
   ```sh
   git clone https://github.com/yourusername/stock-market-analysis-api.git
   cd stock-market-analysis-api
   ```


2. **Create a virtual environment:**
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```
    
3. **Install the dependencies:**
    ```sh
    pip install -r requirements.txt
   ```
4. **Run the Flask application:**
    ```sh
    python app.py
   ```
📚 Usage
API Endpoints
1. **Search for a Company**
    - **Endpoint:** /search
    - **Method:** GET
    - **Parameters:**
        - company (required): The name of the company to search for.
    - **Example:**
        ```sh
        curl "http://127.0.0.1:5000/search?company=Microsoft"
         ```

2.  **Get Stock Information**
    - **Endpoint:** /stock
    - **Method:** GET
    - **Parameters:**
            symbol (required): The stock symbol of the company.
    - **Example:**
      ```sh
            curl "http://127.0.0.1:5000/stock?symbol=MSFT"
      ```

3. **Get Historical Data**
    - **Endpoint:** /historical
    - **Method:** GET
    - **Parameters:**
        - *symbol* (required): The stock symbol of the company.
        - *start_date* (required): The start date for the historical data (format: YYYY-MM-DD).
        - *end_date* (required): The end date for the historical data (format: YYYY-MM-DD).
        - *interval* (optional): The interval for the historical data (default: 1d).
        - **Example:**
          ```sh
                curl "http://127.0.0.1:5000/historical?symbol=MSFT&start_date=2023-01-01&end_date=2023-12-31&interval=1d"
          ```


4. **Get Quote Data**
    - **Endpoint:** /quote
    - **Method:** GET
    - **Parameters:**
        - *symbol* (required): The stock symbol of the company.
    - **Example:**
      ```sh
      curl "http://127.0.0.1:5000/quote?symbol=MSFT"
      ```
5. **Compare Companies**
    - **Endpoint:** /compare
    - **Method:** GET
    - **Parameters:**
        - *symbol* (required): The stock symbol of the company.
        - *num_co*mpanies (optional): The number of companies to compare (default: 5).
        - *includ*e_historical (optional): Whether to include historical data (default: false).
    - **Example:**
      ```sh
            curl "http://127.0.0.1:5000/compare?symbol=MSFT&num_companies=5&include_historical=true"
      ```
