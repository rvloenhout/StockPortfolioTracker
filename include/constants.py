#-----------#
# Constants #
#-----------#
from datetime import datetime, timedelta

HISTORY_START_DATE = datetime.now()
HISTORY_END_DATE = datetime.now() + timedelta(hours=1)

COMPANY_INFO_COLUMNS = {
    "ID": "VARCHAR(50)",
    "stock": "VARCHAR(10)",
    "date": "DATE",
    "longName": "VARCHAR(255)",
    "industry": "VARCHAR(150)",
    "sector": "VARCHAR(150)",
}

STOCK_FUNDAMENTALS_COLUMNS = {
    "ID": "VARCHAR(50) NOT NULL",
    "Symbol": "VARCHAR(10) NOT NULL",
    "Datetime": "DATE NOT NULL",
    "revenueGrowth": "FLOAT NULL",
    "profitMargins": "FLOAT NULL",
    "grossMargins": "FLOAT NULL",
    "operatingMargins": "FLOAT NULL",
    "returnOnEquity": "FLOAT NULL",
    "freeCashflow": "INT NULL",
    "debtToEquity": "FLOAT NULL",
    "currentRatio": "FLOAT NULL",
    "trailingEps": "FLOAT NULL",
    "trailingPE": "FLOAT NULL",
    "returnOnAssets": "FLOAT NULL",
    "operatingCashflow": "INT NULL"
}

# STOCK_RECOMMENDATIONS_COLUMNS = {
#     "recommendationKey": "VARCHAR(50)",
#     "currentPrice": "FLOAT",
#     "targetMedianPrice": "FLOAT",
#     "targetMeanPrice": "FLOAT",
#     "targetLowPrice": "FLOAT",
#     "targetHighPrice": "FLOAT"
# }

PRICE_HISTORY_COLUMNS = {
    "ID": "VARCHAR(50)",
    "Symbol": "VARCHAR(10)",
    "Open": "FLOAT",
    "High": "FLOAT",
    "Low": "FLOAT",
    "Close": "FLOAT",
    "Volume": "BIGINT",
    "Datetime": "DATETIME"
}

INCOMES_STATEMENT_COLUMNS = {
    "Datetime": "DATETIME",
    "TaxEffectOfUnusualItems": "FLOAT",
    "TaxRateForCalcs": "FLOAT",
    "NormalizedEBITDA": "FLOAT",
    "TotalUnusualItems": "FLOAT",
    #"TotalUnusualItemsExcludingGoodwill": "FLOAT",
    "NetIncomeFromContinuingOperationNetMinorityInterest": "FLOAT",
    "ReconciledDepreciation": "FLOAT",
    "ReconciledCostOfRevenue": "FLOAT",
    "EBITDA": "FLOAT",
    "EBIT": "FLOAT",
    "NetInterestIncome": "FLOAT",
    "InterestExpense": "FLOAT",
    "InterestIncome": "FLOAT",
    "NormalizedIncome": "FLOAT",
    "NetIncomeFromContinuingAndDiscontinuedOperation": "FLOAT",
    "TotalExpenses": "FLOAT",
    "TotalOperatingIncomeAsReported": "FLOAT",
    "DilutedAverageShares": "FLOAT",
    "BasicAverageShares": "FLOAT",
    "DilutedEPS": "FLOAT",
    "BasicEPS": "FLOAT",
    "DilutedNIAvailtoComStockholders": "FLOAT",
    "NetIncomeCommonStockholders": "FLOAT",
    "OtherunderPreferredStockDividend": "FLOAT",
    "NetIncome": "FLOAT",
    "NetIncomeIncludingNoncontrollingInterests": "FLOAT",
    "NetIncomeContinuousOperations": "FLOAT",
    "TaxProvision": "FLOAT",
    "PretaxIncome": "FLOAT",
    "SpecialIncomeCharges": "FLOAT",
    "OtherSpecialCharges": "FLOAT",
    "NetNonOperatingInterestIncomeExpense": "FLOAT",
    "TotalOtherFinanceCost": "FLOAT",
    "InterestExpenseNonOperating": "FLOAT",
    "InterestIncomeNonOperating": "FLOAT",
    "OperatingIncome": "FLOAT",
    "OperatingExpense": "FLOAT",
    "OtherOperatingExpenses": "FLOAT",
    "DepreciationAndAmortizationInIncomeStatement": "FLOAT",
    "Amortization": "FLOAT",
    "DepreciationIncomeStatement": "FLOAT",
    "SellingGeneralAndAdministration": "FLOAT",
    "SellingAndMarketingExpense": "FLOAT",
    "GeneralAndAdministrativeExpense": "FLOAT",
    "GrossProfit": "FLOAT",
    "CostOfRevenue": "FLOAT",
    "TotalRevenue": "FLOAT",
    "OperatingRevenue": "FLOAT",
    "Symbol": "VARCHAR(10)"
}
