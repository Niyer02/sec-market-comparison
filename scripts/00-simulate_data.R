#### Preamble ####
# Purpose: Simulates 10Q files and corresponding financial data differences
# Author: Nikhil Iyer
# Date: 17 April 2024
# Contact: Nik.iyer@mail.utoronto.ca
# License: MIT
# Pre-requisites: R
# Python is needed to fetch data


#### Workspace setup ####
library(tidyverse)
library(dplyr)

#### Simulate data ####
set.seed(777)


# Generate simulated data
simulated_data <- data.frame(
  Ticker = rep(c("AAPL", "GOOGL", "MSFT", "AMZN", "NVDA"), each = 10), # Simulate 5 tickers
  MdA_section = rep(c("MD&A TEXT"), each = 50), # The text does not really matter so we use filler text
  OneWeek = runif(50, min = -0.1, max = 0.1) * 100, # 1 week percentage gain/loss in price
  OneMonth = runif(50, min = -0.15, max = 0.2) * 100, # 1 month percentage gain/loss in price
  ThreeMonth = runif(50, min = -0.2, max = 0.3) * 100, # 3 week percentage gain/loss in price
  SixMonth = runif(50, min = -0.25, max = 0.4) * 100 # 6 week percentage gain/loss in price
)

# Sort data by Ticker
simulated_data <- arrange(simulated_data, Ticker, MdA_section)

# Display first couple of rows of the generated data
head(simulated_data)