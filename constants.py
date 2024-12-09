#-----------#
# Constants #
#-----------#
COMPANY_INFO_COLUMNS = {
    "longName": "VARCHAR(255)",
    "country": "VARCHAR(100)",
    "industry": "VARCHAR(150)",
    "sector": "VARCHAR(150)",
    "fullTimeEmployees": "INT",
    "longBusinessSummary": "TEXT"
}

STOCK_FUNDAMENTALS_COLUMNS = {
    "profitMargins": "FLOAT",
    "operatingMargins": "FLOAT",
    "returnOnAssets": "FLOAT",
    "returnOnEquity": "FLOAT",
    "currentRatio": "FLOAT",
    "quickRatio": "FLOAT",
    "debtToEquity": "FLOAT",
    "trailingPE": "FLOAT",
    "trailingEps": "FLOAT",
    "priceToBook": "FLOAT",
    "priceToSalesTrailing12Months": "FLOAT"
}

STOCK_RECOMMENDATIONS_COLUMNS = {
    "recommendationKey": "VARCHAR(50)",
    "currentPrice": "FLOAT",
    "targetMedianPrice": "FLOAT",
    "targetMeanPrice": "FLOAT",
    "targetLowPrice": "FLOAT",
    "targetHighPrice": "FLOAT"
}

PRICE_HISTORY_COLUMNS = {
    "Symbol": "VARCHAR(10)",  # Assuming stock ticker symbols
    "Open": "FLOAT",
    "High": "FLOAT",
    "Low": "FLOAT",
    "Close": "FLOAT",
    "Volume": "BIGINT"  # Volume is usually large, so BIGINT is appropriate
}