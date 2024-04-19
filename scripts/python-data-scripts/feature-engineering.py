import pandas as pd
import nltk
import numpy as np
from nltk.sentiment import vader
nltk.download('vader_lexicon')

sid = vader.SentimentIntensityAnalyzer()

# Get the set of positive words
positive_words = set(sid.lexicon.keys())
negative_words = set(word for word, score in sid.lexicon.items() if score < 0)

raw_data = pd.read_csv("../../data/raw_data/Final_raw_data.csv")

# Group the DataFrame by the 'ticker' column
grouped = raw_data.groupby('ticker')

# Create a dictionary to store DataFrames for each ticker
ticker_dfs = {}

for ticker, group_df in grouped:
    ticker_dfs[ticker] = group_df

# Calculate the average number of words in the 'filing_data-Preprocessed' column for each DataFrame
average_word_counts = {}
for ticker, df in ticker_dfs.items():
    # Split the text into words and calculate the word count for each row
    word_counts = df['processed_filing_data'].str.split().apply(len)
    # Calculate the average word count for the entire column
    avg_word_count = word_counts.mean()
    average_word_counts[ticker] = avg_word_count

# Print the average word counts
for ticker, avg_count in average_word_counts.items():
    print(f"Average number of words in 'filing_data-Preprocessed' column for {ticker}: {avg_count}")

# Calculate the average number of positive words in the 'filing_data-Preprocessed' column for each DataFrame

average_sentiment_word_counts = {}
for ticker, df in ticker_dfs.items():
    # Count positive and negative words for each row
    positive_counts = df['processed_filing_data'].apply(lambda x: sum(1 for word in nltk.word_tokenize(x.lower()) if word in positive_words))
    negative_counts = df['processed_filing_data'].apply(lambda x: sum(1 for word in nltk.word_tokenize(x.lower()) if word in negative_words))
    # Calculate the average positive and negative word counts
    avg_positive_count = positive_counts.mean()
    avg_negative_count = negative_counts.mean()
    average_sentiment_word_counts[ticker] = {'positive': avg_positive_count, 'negative': avg_negative_count}

# Print the average positive and negative word counts
for ticker, counts in average_sentiment_word_counts.items():
    print(f"Average number of positive words in 'filing_data-Preprocessed' column for {ticker}: {counts['positive']}")
    print(f"Average number of negative words in 'filing_data-Preprocessed' column for {ticker}: {counts['negative']}")

positive_word_counts_array = np.array([counts['positive'] for counts in average_sentiment_word_counts.values()])
mean_positive_word_count = np.mean(positive_word_counts_array)
std_positive_word_count = np.std(positive_word_counts_array)

# Calculate the mean and standard deviation of negative word counts across all rows
negative_word_counts_array = np.array([counts['negative'] for counts in average_sentiment_word_counts.values()])
mean_negative_word_count = np.mean(negative_word_counts_array)
std_negative_word_count = np.std(negative_word_counts_array)

# Calculate the mean and standard deviation of average word counts across all rows
average_word_counts_array = np.array(list(average_word_counts.values()))
mean_avg_word_count = np.mean(average_word_counts_array)
std_avg_word_count = np.std(average_word_counts_array)

# Add z-scores columns to the DataFrame
for ticker, df in ticker_dfs.items():
    # Calculate z-scores for each row
    df['z_score_positive'] = (df['processed_filing_data'].apply(lambda x: sum(1 for word in nltk.word_tokenize(x.lower()) if word in positive_words)) - mean_positive_word_count) / std_positive_word_count
    df['z_score_negative'] = (df['processed_filing_data'].apply(lambda x: sum(1 for word in nltk.word_tokenize(x.lower()) if word in negative_words)) - mean_negative_word_count) / std_negative_word_count
    df['z_score_avg_word_count'] = (df['processed_filing_data'].str.split().apply(len) - mean_avg_word_count) / std_avg_word_count

concatenated_df = pd.concat(ticker_dfs.values(), keys=ticker_dfs.keys())

# Reset index to make the keys (tickers) into columns
concatenated_df.reset_index(inplace=True)

concatenated_df.to_csv('../../data/raw_data/raw_features.csv')
# Set financial features to be 0 or 1

# Model the outcome


