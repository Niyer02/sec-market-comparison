#### Preamble ####
# Purpose: Tests the data to ensure no Type errors or any other errors
# Author: Nikhil Iyer
# Date: 17 April 2024
# Contact: Nik.iyer@mail.utoronto.ca
# License: MIT
# Pre-requisites: R
# Python is needed to fetch data


#### Workspace setup ####
library(tidyverse)


#### Test data ####
analysis_data <- read_csv("data/analysis_data/analysis_data.csv")

# Test that quant columns are all numeric
quant_columns <- c("IG", "1-Month", "3-Month", "6-Month", "z_score_positive", "z_score_negative", "z_score_avg_word_count")

test_numeric <- function(col) {
  all(is.numeric(col))
}

test <- sapply(analysis_data[quant_columns], test_numeric)

if (all(test)) {
  print("PASS")
} else {
  failed <- names(test)[!test]
  print("FAIL for columns: ", paste(failed), collapse=", ")
}

# Test that the date column is in proper format: YYYY-MM-DD
filing_date <- analysis_data$filing_date

test_date <- function(date) {
  grepl("^\\d{4}-\\d{2}-\\d{2}$", date)
}

test_d <- sapply(filing_date, test_date)

if (all(test_d)) {
  print("PASS")
} else {
  print("FAIL")
}