import pandas as pd

# Function to generate financial-related questions and answers
def generate_questions_and_answers(ticker, cik, label, value, date):
    questions = [
        f"What is the US GAAP XBRL tag for {label} as reported by {ticker} for fiscal year {date[:4]}?",
        f"Provide the XBRL tag for {label} reported by {ticker} on {date}.",
        f"Which XBRL tag represents {label} in {ticker}'s {date[:4]} filing?",  # Use label as the answer here
        f"What is the value of {label} as reported by {ticker} on {date}?",
        f"Which financial statement includes {label} for {ticker} in the {date[:4]} report?"  # Provide a more meaningful answer
    ]
    
    # Use label for XBRL tag-related questions, value for value-related questions, and provide meaningful answers for financial statement
    answers = [
        label,  # XBRL tag itself
        label,  # XBRL tag itself
        label,  # XBRL tag itself
        value,  # Value of the label
        get_financial_statement(label)  # More meaningful financial statement answer
    ]
    return questions, answers

# Function to provide meaningful financial statement context
def get_financial_statement(label):
    # Example: Assigning different labels to specific financial statements
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
        return "Unknown Statement"  # Default answer if not sure

# Function to generate filing-related questions and answers
def generate_filing_questions_and_answers(ticker, company_name, form_type, filing_date, report_date, filing_url):
    filing_questions = [
        f"What is the {form_type} filing for {company_name} (Ticker: {ticker}) on {filing_date}?",
        f"Which {form_type} document was filed by {company_name} on {filing_date}?",
        f"Provide the link to the {form_type} filed by {ticker} on {filing_date}.",
        f"What is the reporting period for {ticker}'s {form_type} filed on {filing_date}?"
    ]
    # Use filing_url or report_date as answers
    filing_answers = [filing_url, filing_url, filing_url, report_date]
    return filing_questions, filing_answers

# Load the CSV files
financial_data_df = pd.read_csv('dow_jones_financial_data.csv')
filings_df = pd.read_csv('dowjonesfilings.csv')
submission_data_df = pd.read_csv('dow_jones_submission_data.csv')

# Extract filings info and submission info
filings_info = filings_df[['Ticker', 'Form Type', 'Filing Date', 'Report Date', 'Filing URL']]
submission_info = submission_data_df[['ticker', 'company_name', 'filing_date', 'form_type', 'primary_document']]

# Generate questions and answers for financial data
questions = []
answers = []
for index, row in financial_data_df.iterrows():
    ticker = row['Ticker']
    cik = row['CIK']
    label = row['Label']
    value = row['Value']
    date = row['Date']
    
    # Generate financial metric questions and answers
    q, a = generate_questions_and_answers(ticker, cik, label, value, date)
    questions.extend(q)
    answers.extend(a)

# Generate filing-related questions and answers
for index, row in filings_info.iterrows():
    ticker = row['Ticker']
    form_type = row['Form Type']
    filing_date = row['Filing Date']
    report_date = row['Report Date']
    filing_url = row['Filing URL']
    
    # Get company name from submission data, skip if ticker doesn't exist
    company_row = submission_info[submission_info['ticker'] == ticker]
    if not company_row.empty:
        company_name = company_row['company_name'].values[0]
        # Generate filing-specific questions and answers
        q, a = generate_filing_questions_and_answers(ticker, company_name, form_type, filing_date, report_date, filing_url)
        questions.extend(q)
        answers.extend(a)

# Save the generated questions and answers to a CSV file
output_df = pd.DataFrame({
    'Generated Questions': questions,
    'Generated Answers': answers
})
output_df.to_csv('generated_questions_and_answers_output_final.csv', index=False)

print("Questions and answers generated and saved to 'generated_questions_and_answers_output_final.csv'")
