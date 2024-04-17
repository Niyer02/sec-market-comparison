from sec_api import QueryApi, ExtractorApi
import yfinance as yf
import pandas as pd
from bs4 import BeautifulSoup
import csv


def fetch_query_list(query_set):
    queryAPI = QueryApi(api_key="YOUR_API_KEY")


    if query_set == 1:
        query = {
            "query": {
                "query_string": {
                    "query": "ticker:(TSLA OR NVDA OR AAPL OR MSFT OR ORCL) AND filedAt:{2019-01-01 TO 2023-12-31} AND formType:\"10-Q\""
                }
            },
            "from": "0",
            "size": "100000"
        }
    else:
        query = {
            "query": {
                "query_string": {
                    "query": "ticker:(AMZN OR NFLX OR AMD OR ADBE OR META) AND filedAt:{2019-01-01 TO 2023-12-31} AND formType:\"10-Q\""
                }
            },
            "from": "0",
            "size": "100000"
        }

    response = queryAPI.get_filings(query)

    data_by_ticker = {}
    # Iterate over the filings
    for filing in response["filings"]:
        # Get the ticker for the filing
        ticker = filing["ticker"]
        # Get the link to HTML for the filing
        link_to_html = filing["linkToHtml"]
        # Get the filed date for the filing
        filed_at = filing["filedAt"]
        # Append the link to HTML and filed date to the list corresponding to the ticker
        data_by_ticker.setdefault(ticker, []).append({"link": link_to_html, "filed_at": filed_at})

    # Convert the dictionary to a list of lists
    data_by_ticker_list = [[ticker, data] for ticker, data in data_by_ticker.items()]

    return data_by_ticker_list


def fetch_mda(ticker_list, l_number):
    extractorApi = ExtractorApi("YOUR_API_KEY")
    all_filings1 = []

    # Iterate through each sublist in the data list
    for company_data in ticker_list:
        # Access the list of dictionaries containing links and filing dates
        filings = company_data[1]

        ticker = company_data[0]
        # Sort the list of dictionaries based on 'filed_at' in descending order
        sorted_filings = sorted(filings, key=lambda x: x['filed_at'], reverse=True)
        # Iterate through each filing link
        for filing in sorted_filings:
            # Extract the filing URL
            filing_url = filing['link']
            filing_date = filing['filed_at']
            # Use the extractorApi to get the section with the given parameters
            filing_content = extractorApi.get_section(filing_url, "part1item2", "html")
            # Append the filing content to the list
            all_filings1.append([ticker, filing_content, filing_date])

    csv_file_path = f"all_filings_{l_number}.csv"

    # Open the CSV file in write mode with newline='' to prevent extra blank lines
    with open(csv_file_path, 'w', newline='') as csvfile:
        # Create a CSV writer object
        writer = csv.writer(csvfile)

        # Write the header row
        writer.writerow(['Ticker', 'Filing Content', 'Filing Date'])

        # Iterate through each item in the all_filings1 list
        for item in all_filings1:
            # Write each item as a row in the CSV file
            writer.writerow(item)
    return csv_file_path


def rem_tables_to_text(csv_path, number):
    def remove_tables(html):
        soup = BeautifulSoup(html, 'html.parser')

        for table in soup.find_all('table'):
            table.decompose()
        return soup.get_text()

    data = pd.read_csv(csv_path)
    dfs = []

    for index, row in data.iterrows():
        processed_text = remove_tables(row['Filing Content'])

        processed_df = pd.DataFrame({
            'ticker': [row['Ticker']],
            'filing_date': [row['Filing Date']],
            'processed_filing_data': [processed_text]
        })

        # Append the DataFrame to the list
        dfs.append(processed_df)

    processed_data = pd.concat(dfs, ignore_index=True)

    processed_data.to_csv(f'raw_text_{number}.csv')

    return f'raw_text_{number}.csv'


if __name__ == '__main__':
    # Get list of links
    ticker_list_1 = fetch_query_list(1)
    ticker_list_2 = fetch_query_list(2)

    # Get MD&A sections
    file_path_1 = fetch_mda(ticker_list_1, '1')
    file_path_2 = fetch_mda(ticker_list_2, '2')

    # Clean the HTML to remove tables and return text
    raw_text_1 = rem_tables_to_text(file_path_1, '1')
    raw_text_2 = rem_tables_to_text(file_path_2, '2')

    # Concat the 2 CSV files into 1
    df1 = pd.read_csv(raw_text_1)
    df2 = pd.read_csv(raw_text_2)

    final_df = pd.concat([df1, df2], ignore_index=True)

    final_df = final_df.drop(columns=['Unnamed: 0'])

    final_df.to_csv('final_text_data.csv')




