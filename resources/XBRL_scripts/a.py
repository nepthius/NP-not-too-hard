import os
import json
import csv

json_dir = 'dow_jones_sample'
output_csv = 'dow_jones_financial_data.csv'

key_labels = [
    'SalesRevenueNet', 'RevenueFromContractWithCustomer', 'NetIncomeLoss', 
    'CostOfGoodsAndServicesSold', 'OperatingExpenses', 'Assets', 'AssetsCurrent', 
    'Liabilities', 'LiabilitiesCurrent', 'StockholdersEquity', 'CashAndCashEquivalentsAtCarryingValue',
    'NetCashProvidedByUsedInOperatingActivities', 'EarningsPerShareBasic', 'EarningsPerShareDiluted', 
    'Dividends', 'DividendsDeclaredPerShare', 'TotalDebtToEquityRatio', 'CapitalExpendituresIncurredButNotYetPaid',
    'CommonStockSharesOutstanding'
]


cik_to_ticker = {
    66740: 'MMM', 4962: 'AXP', 318154: 'AMGN', 320193: 'AAPL', 12927: 'BA',
    18230: 'CAT', 93410: 'CVX', 858877: 'CSCO', 21344: 'KO', 1751788: 'DOW',
    886982: 'GS', 354950: 'HD', 773840: 'HON', 51143: 'IBM', 50863: 'INTC',
    200406: 'JNJ', 19617: 'JPM', 63908: 'MCD', 310158: 'MRK', 789019: 'MSFT',
    320187: 'NKE', 80424: 'PG', 1108524: 'CRM', 86312: 'TRV', 731766: 'UNH',
    732712: 'VZ', 1403161: 'V', 1618921: 'WBA', 104169: 'WMT', 1001039: 'DIS'
}

def extract_data(json_data, key_labels):
    extracted_data = []
    for section, content in json_data.get('facts', {}).items():
        for label, details in content.items():
            if label in key_labels:
                values = details.get('units', {}).get('USD', [])
                for item in values:
                    extracted_data.append({
                        'Label': label,
                        'Value': item.get('val'),
                        'Date': item.get('end'),
                    })
    return extracted_data
with open(output_csv, mode='w', newline='') as csvfile:
    fieldnames = ['Ticker', 'CIK', 'Label', 'Value', 'Date']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    for filename in os.listdir(json_dir):
        if filename.endswith('.json'):
            cik = filename.replace('CIK', '').replace('.json', '')  
            cik_int = int(cik)
            
            if cik_int in cik_to_ticker:
                ticker = cik_to_ticker[cik_int]

                with open(os.path.join(json_dir, filename), 'r') as f:
                    data = json.load(f)
                    extracted_data = extract_data(data, key_labels)

                    for item in extracted_data:
                        writer.writerow({
                            'Ticker': ticker,
                            'CIK': cik,
                            'Label': item['Label'],
                            'Value': item['Value'],
                            'Date': item['Date']
                        })

print(f"Data extraction completed. Saved to {output_csv}")
