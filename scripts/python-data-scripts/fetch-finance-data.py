import yfinance as yf
import pandas as pd
from datetime import timedelta


def fetch_finance_data(ticker_list, start_date, end_date):
    df = yf.download(ticker_list, start=start_date, end=end_date)
    return df


if __name__ =='__main__':
    raw_text = pd.read_csv('final_text_data.csv')
    raw_text['filing_date'] = raw_text['filing_date'].apply(lambda x: x.split('T', 1)[0])

    # WE WANT:
    # 1 week prior to MD&A AND 1 week after MD&A => INFORMATION GIVEN IN MD&A
    # 1 month after MD&A
    # 3 months after MD&A
    # 6 months after MF&A

    print("Computing Differences of 1 week")
    # 1 WEEK PRIOR AND AFTER MD&A
    raw_text['IG'] = None
    raw_text['filing_date'] = pd.to_datetime(raw_text['filing_date'])
    for index, row in raw_text.iterrows():
        filing_date = row['filing_date']
        ticker = row['ticker']

        prev_7 = filing_date - timedelta(days=7)
        post_7 = filing_date + timedelta(days=7)

        post_7_p = filing_date + timedelta(days=6)

        formatted_pre_7 = prev_7.strftime('%Y-%m-%d')
        formatted_post_7 = post_7.strftime('%Y-%m-%d')

        formatted_post_7_p = post_7_p.strftime('%Y-%m-%d')

        finance_data = fetch_finance_data([f'{ticker}'], formatted_pre_7, formatted_post_7)

        pre_7 = finance_data['Adj Close'].iloc[0]

        post_7 = finance_data['Adj Close'].iloc[-1]
        diff = (abs(post_7 - pre_7) / pre_7) * 100

        raw_text.at[index, 'IG'] = diff

    print("Computing Differences of 1 Month")
    # 1 Month after MD&A
    raw_text['1-Month'] = None
    for index, row in raw_text.iterrows():
        filing_date = row['filing_date']
        ticker = row['ticker']

        month_ahead = filing_date + timedelta(days=30)

        formatted_month_ahead = month_ahead.strftime('%Y-%m-%d')

        finance_data = fetch_finance_data([f'{ticker}'], filing_date, formatted_month_ahead)

        pre_month = finance_data['Adj Close'].iloc[0]

        post_month = finance_data['Adj Close'].iloc[-1]
        diff = (abs(post_month - pre_month) / pre_month) * 100

        raw_text.at[index, '1-Month'] = diff

    print("Computing Differences of 3 Month")
    # 1 Month after MD&A
    raw_text['3-Month'] = None
    for index, row in raw_text.iterrows():
        filing_date = row['filing_date']
        ticker = row['ticker']

        month_ahead = filing_date + timedelta(days=90)

        formatted_month_ahead = month_ahead.strftime('%Y-%m-%d')

        finance_data = fetch_finance_data([f'{ticker}'], filing_date, formatted_month_ahead)

        pre_month = finance_data['Adj Close'].iloc[0]

        post_month = finance_data['Adj Close'].iloc[-1]
        diff = (abs(post_month - pre_month) / pre_month) * 100

        raw_text.at[index, '3-Month'] = diff

    print("Computing Differences of 6 Month")
    # 1 Month after MD&A
    raw_text['6-Month'] = None
    for index, row in raw_text.iterrows():
        filing_date = row['filing_date']
        ticker = row['ticker']

        month_ahead = filing_date + timedelta(days=180)

        formatted_month_ahead = month_ahead.strftime('%Y-%m-%d')

        finance_data = fetch_finance_data([f'{ticker}'], filing_date, formatted_month_ahead)

        pre_month = finance_data['Adj Close'].iloc[0]

        post_month = finance_data['Adj Close'].iloc[-1]
        diff = (abs(post_month - pre_month) / pre_month) * 100

        raw_text.at[index, '6-Month'] = diff

    raw_text = raw_text.drop(columns=['Unnamed: 0'])
    raw_text.to_csv('Final_raw_data.csv')

