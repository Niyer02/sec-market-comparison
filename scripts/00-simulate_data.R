#### Preamble ####
# Purpose: Simulates 10Q files and corresponding financial data differences
# Author: Nikhil Iyer
# Date: 17 April 2024
# Contact: Nik.iyer@mail.utoronto.ca
# License: MIT
# Pre-requisites: R, LaTeX
# Python is needed to fetch data


#### Workspace setup ####
library(tidyverse)
library(dplyr)

#### Simulate data ####
set.seed(777)


# Generate sample data
simulated_data <- data.frame(
  Ticker = rep(c("AAPL", "GOOGL", "MSFT", "AMZN", "NVDA"), each = 10),
  MdA_section = rep(c("MD&A TEXT"), each = 50),
  OneWeek = runif(50, min = -0.1, max = 0.1) * 100,
  OneMonth = runif(50, min = -0.15, max = 0.2) * 100,
  ThreeMonth = runif(50, min = -0.2, max = 0.3) * 100,
  SixMonth = runif(50, min = -0.25, max = 0.4) * 100
)

# Sort data by Ticker and MdA_section
simulated_data <- arrange(simulated_data, Ticker, MdA_section)

# Display first few rows of the generated data
head(simulated_data)