# Singapore Birth Rate and Fertility Analysis

GA Capstone Project – Lester



## Overview

This project examines historical fertility and birth data in Singapore to understand the scale, pattern, and structure of long-term decline in total fertility rate and resident live births.

The analysis follows a structured data analysis process, starting from data preparation and exploratory analysis, followed by feature engineering, predictive modelling, and model evaluation.

The purpose of this project is not causal inference, but predictive evaluation and trend understanding based on available historical data.

[Visual placeholder]



## Problem, Goals, and Audience

### Problem Statement

Singapore’s total fertility rate and resident live births have decline steadily over the past few decades.
This long-term trend raises concerns about population ageing, labour force sustainability, and overall economic stability.

This project examines historical fertility and birth data to understand how fertility has changed over time, whether the decline is gradual or abrupt, and how persistent the pattern is across years.

The focus is on understanding the data patterns before attempting prediction.

### Project Goals

This project aims to:

* Analyse long-term trends in total fertility rate and resident live births in Singapore
* Identify major patterns and structural shifts over time
* Build and evaluate at least one predictive model using historical data

The goals are limited to what the data can support, given the annual structure and limited number of observations.

### Intended Audience

This analysis is written for policymakers and planners involved in population policy, workforce development, and long-term socio-economic planning in Singapore.



## Data Sources and Preparation

### Why these datasets are used

This project uses data from official Singapore government statistics.
The data is downloaded in CSV format.

The main datasets used are:

* Total Fertility Rate by year
* Births and fertility rates

These datasets are chosen because they come from an official source, cover many years, and are directly related to fertility and birth patterns.

Yearly national data allows the analysis of long-term fertility changes rather than short-term fluctuation.

### Why the HDB Resale Price Index is included

The HDB Resale Price Index is included as a contextual economic indicator for extended modelling.

It is not used as a core fertility variable, but added to test whether an economic housing indicator improves short-term fertility prediction when combined with fertility history.

This dataset is included for comparison, not assumption of causality.

### Data Preparation

The datasets are originally stored in wide format.
They are reshaped into long format to support time-series analysis.

Before analysis, the datasets are inspected for structure, data types, missing values, duplicate values, and plausible value ranges.

No missing or duplicate values are found after reshaping, and the datasets are suitable for further analysis.

[Visual placeholder]



## Exploratory Data Analysis

### Why EDA is done before modelling

Exploratory data analysis is used to describe long-term trends before feature engineering or modelling.

This step ensures that modelling choices are informed by observed patterns rather than assumptions.

### What is examined

The analysis examines:

* Changes in total fertility rate over time
* The year fertility first fell below replacement level
* Long-term decline patterns in resident live births
* Shifts in birth counts by birth order

The results show a sustained decline rather than short-term volatility.

This confirms that fertility changes gradually over time, which informs later feature engineering decisions.

[Visual placeholder]



## Feature Engineering

### Why feature engineering is limited

Given the annual structure of the data and the limited number of observations, feature engineering is kept simple.

The focus is on capturing persistence and gradual change rather than adding many variables.

### Features created

The following variables are created:

* Lag variables representing prior-year fertility values
* A year-on-year change variable
* A time index representing long-term movement

Lag variables allow the model to incorporate fertility levels from previous years.
This reflects the gradual nature of fertility change observed in the EDA.

Observations affected by lag-related missing values are removed before modelling to maintain data consistency.

### Why not more lag variables

The number of lag variables is kept small because additional lags reduce the number of usable observations without improving model performance.

This decision balances model complexity with dataset size.



## Predictive Modelling

### Why linear regression is used

Linear regression is used because it is suitable for small datasets and allows clear comparison between baseline and extended models.

The objective is predictive evaluation rather than complex modelling.

### Models built

The following models are built:

* A baseline model using a single lag variable
* A lag regression model using multiple lag variables
* An extended model including the HDB Resale Price Index

A time-aware train and test split is used to preserve chronological order and avoid information leakage.



## Model Performance

### How performance is evaluated

Model performance is evaluated using mean absolute error and root mean squared error.

These metrics allow comparison across models using the same test data.

### What the results show

The lag regression model performs better than the baseline model.

The extended model including the HDB Resale Price Index does not show meaningful improvement in prediction accuracy.

This indicates that recent fertility history explains short-term fertility changes better than the housing price index in this model setup.

[Visual placeholder]



## Model Interpretation

Lag variables show strong influence on predicted fertility values.
This reflects persistence in fertility levels across consecutive years.

The strong correlation between the time index and the HDB Resale Price Index introduces multicollinearity in the extended model.

This limits coefficient interpretability and supports the decision not to rely on the extended model for conclusions.

The models are used for predictive evaluation rather than causal inference.



## Assumptions

The linear regression models assume:

* A linear relationship between predictors and fertility rate
* Independence of errors
* Constant error variance
* No severe multicollinearity

Some assumptions are affected by the small dataset and strong time correlation.



## Limitations

The dataset contains a limited number of yearly observations after feature engineering.
This restricts model complexity and statistical power.

Annual data may mask short-term changes.
Policy changes and immigration dynamics are not explicitly modelled.

The results should be interpreted as exploratory and predictive rather than causal.



## Conclusions and Next Steps

The analysis confirms a long-term decline in fertility in Singapore.

Lag-based models capture short-term fertility patterns better than models that include housing price data.

Future work could include:

* Additional demographic variables
* Alternative modelling approaches
* Higher frequency data if available

This project provides a structured foundation for further fertility trend analysis.
