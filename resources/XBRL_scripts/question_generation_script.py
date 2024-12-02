import pandas as pd


def generate_questions_and_answers(ticker, cik, label, value, date):
    questions = [
        f"What is the US GAAP XBRL tag for {label} as reported by {ticker} for fiscal year {date[:4]}?",
        f"Provide the XBRL tag for {label} reported by {ticker} on {date}.",
        f"Which XBRL tag represents {label} in {ticker}'s {date[:4]} filing?",  
        f"What is the value of {label} as reported by {ticker} on {date}?",
        f"Which financial statement includes {label} for {ticker} in the {date[:4]} report?" 
    ]
    
    answers = [
        label, 
        label,  
        label,  
        value,  
        get_financial_statement(label)
    ]
    return questions, answers

def get_financial_statement(label):
    balance_sheet_items = ['Assets', 'AssetsCurrent', 'Liabilities', 'LiabilitiesCurrent', 'StockholdersEquity']
    income_statement_items = ['SalesRevenueNet', 'NetIncomeLoss', 'OperatingExpenses', 'EarningsPerShareBasic', 'EarningsPerShareDiluted']
    cash_flow_items = ['NetCashProvidedByUsedInOperatingActivities', 'CapitalExpendituresIncurredButNotYetPaid']

    if label in balance_sheet_items:
        return "Balance Sheet"
    elif label in income_statement_items:
        return "Income Statement"
    elif label in cash_flow_items:
        return "Cash Flow Statement"
    else:
        return "Unknown Statement" 

def generate_filing_questions_and_answers(ticker, company_name, form_type, filing_date, report_date, filing_url):
    filing_questions = [
        f"What is the {form_type} filing for {company_name} (Ticker: {ticker}) on {filing_date}?",
        f"Which {form_type} document was filed by {company_name} on {filing_date}?",
        f"Provide the link to the {form_type} filed by {ticker} on {filing_date}.",
        f"What is the reporting period for {ticker}'s {form_type} filed on {filing_date}?"
    ]
    filing_answers = [filing_url, filing_url, filing_url, report_date]
    return filing_questions, filing_answers

financial_data_df = pd.read_csv('dow_jones_financial_data.csv')
filings_df = pd.read_csv('dowjonesfilings.csv')
submission_data_df = pd.read_csv('dow_jones_submission_data.csv')

filings_info = filings_df[['Ticker', 'Form Type', 'Filing Date', 'Report Date', 'Filing URL']]
submission_info = submission_data_df[['ticker', 'company_name', 'filing_date', 'form_type', 'primary_document']]

questions = []
answers = []
for index, row in financial_data_df.iterrows():
    ticker = row['Ticker']
    cik = row['CIK']
    label = row['Label']
    value = row['Value']
    date = row['Date']
    
    q, a = generate_questions_and_answers(ticker, cik, label, value, date)
    questions.extend(q)
    answers.extend(a)

for index, row in filings_info.iterrows():
    ticker = row['Ticker']
    form_type = row['Form Type']
    filing_date = row['Filing Date']
    report_date = row['Report Date']
    filing_url = row['Filing URL']
    
    company_row = submission_info[submission_info['ticker'] == ticker]
    if not company_row.empty:
        company_name = company_row['company_name'].values[0]
        q, a = generate_filing_questions_and_answers(ticker, company_name, form_type, filing_date, report_date, filing_url)
        questions.extend(q)
        answers.extend(a)

output_df = pd.DataFrame({
    'Generated Questions': questions,
    'Generated Answers': answers
})
output_df.to_csv('generated_questions_and_answers_output_final.csv', index=False)

print("Questions and answers generated and saved to 'generated_questions_and_answers_output_final.csv'")
