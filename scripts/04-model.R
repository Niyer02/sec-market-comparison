#### Preamble ####
# Purpose: Models... [...UPDATE THIS...]
# Author: Rohan Alexander [...UPDATE THIS...]
# Date: 11 February 2023 [...UPDATE THIS...]
# Contact: rohan.alexander@utoronto.ca [...UPDATE THIS...]
# License: MIT
# Pre-requisites: [...UPDATE THIS...]
# Any other information needed? [...UPDATE THIS...]


#### Workspace setup ####
library(tidyverse)
library(rstanarm)
library(lme4)
library(dplyr)
library(randomForest)
library(xgboost)
library(e1071)
library(nnet)
library(survival)
library(readr)
library(brms)
library(ggplot2)


#### Read data ####
analysis_data <- read_csv("data/analysis_data/analysis_data.csv")


### Model data ####

# Gaussian model
model_1_month <- stan_glm(
  `1-Month` ~ z_score_positive + z_score_negative + z_score_avg_word_count,
  data = analysis_data,
  family = gaussian(),
  seed = 853
)

# Gaussian model summary
summary_model_1_month <- summary(model_1_month)
print(summary_model_1_month)

# Random Forest Model
rf_model <- randomForest(`1-Month` ~ z_score_positive + z_score_negative + z_score_avg_word_count, data = train_data)

# Random Forest evaluation
rf_preds <- predict(rf_model, newdata = test_data)
mae_rf <- mean(abs(rf_preds - test_data$`1-Month`))
rmse_rf <- sqrt(mean((rf_preds - test_data$`1-Month`)^2))
rsq_rf <- 1 - (sum((rf_preds - test_data$`1-Month`)^2) / sum((test_data$`1-Month` - mean(test_data$`1-Month`))^2))
cat("Random Forest:\n")
cat("MAE:", mae_rf, "\n")
cat("RMSE:", rmse_rf, "\n")
cat("R-squared:", rsq_rf, "\n\n")


# Linear model for plotting purposes
linear_model <- lm(z_score_avg_word_count ~ `6-Month`, data = analysis_data)

# Plot the data and the regression line
plot(analysis_data$`6-Month`, analysis_data$z_score_avg_word_count,
     xlab = "1-Month", ylab = "z_score_avg_word_count",
     main = "Scatter Plot of 1-Month vs. z_score_avg_word_count")
abline(linear_model, col = "red")

# Polynomial regression for plotting purposes
poly_model <- lm(z_score_avg_word_count ~ poly(`1-Month`, 2), data = analysis_data)

ggplot(analysis_data, aes(x = `1-Month`, y = z_score_avg_word_count)) +
  geom_point() +
  geom_smooth(method = "lm", formula = y ~ poly(x, 2), color = "red") +
  labs(x = "1-Month", y = "z_score_avg_word_count", 
       title = "Polynomial Regression Model (Degree 2) for 1-Month and z_score_avg_word_count") +
  theme_minimal()

# Save the RF model
saveRDS(
  rf_model,
  file = "models/random_forest_model.rds"
)


