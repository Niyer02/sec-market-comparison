#### Preamble ####
# Purpose: Cleans the raw data fetched by the Python scripts
# Author: Nikhil Iyer
# Date: 17 April 2024
# Contact: Nik.iyer@mail.utoronto.ca
# License: MIT
# Pre-requisites: R
# Python is needed to fetch data

#### Workspace setup ####
library(tidyverse)
library(dplyr)


#### Clean data ####
set.seed(777)
data <- read_csv("data/raw_data/raw_features.csv")

# Drop unnecessary columns that were made in the data fetching process
data <- select(data, -contains("...1"))
data <- select(data, -contains("level_0"))
data <- select(data, -contains("level_1"))
data <- select(data, -contains("Unnamed: 0"))

# We also do not need the text data anymore so we can remove it
data <- select(data, -contains("processed_filing_data"))

# Clean up the quant data to have 4 decimal places
data[c("IG", "1-Month", "3-Month", "6-Month", "z_score_positive", "z_score_negative", "z_score_avg_word_count")] <- 
  lapply(data[c("IG", "1-Month", "3-Month", "6-Month", "z_score_positive", "z_score_negative", "z_score_avg_word_count")], round, 4)

# Now we have only numeric data
write.csv(data,"data/analysis_data/analysis_data.csv")