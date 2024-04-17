#### Preamble ####
# Purpose: Cleans the raw data fetched by the Python scripts
# Author: Nikhil Iyer
# Date: 17 April 2024
# Contact: Nik.iyer@mail.utoronto.ca
# License: MIT
# Pre-requisites: R, LaTeX
# Python is needed to fetch data

#### Workspace setup ####
library(tidyverse)
library(tm)
library(SnowballC)

#### Clean data ####
set.seed(777)
data <- read_csv("data/raw_data/Final_raw_data.csv")

