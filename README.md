# Airline On-Time Performance Analysis - FInal Project

**Auburn Univertisy * INSY6500 * FALL 2025**
BY: Trace Warriner & Brandon Chambers

## Project Overview
This project seeks to examine airline on-time performance metric from the U.S. Department of Transportation. The analysis question-driven following the class requirements that are set by the EDA worflow. Analysis is question driven, iterative and ground in domain knowledge and data quality.

## Data Source
U.S. Department of Transportation Statistics
  * Contains flight-level record data includeing attributes such as flight date, departure/arrival times, airports, airlines, origin/destination

Federal Aviation Administration
  * Contains data on tail numbers, aircraft make and model

## EDA Workflow
Our work follows the six phases of EDA workflow:

### 1. Load & Initial Reconnaissance
  * Load multiple raw data files (CSVs & ZIPs)
  * Identfy entities, attributes, and observations
  * Assessed variable types, shapes, and missing data

### 2. Data Quality Assessment
  * Checked for dtype mismatches
  * Identified missing data and the number of missing values

### 3. Cleaning Decisions
  * Converted dtypes and removed/imputed missing data
  * Converted dates and times to datetime objects
  * Joined aircraft, airline, and airport reference data using merge

### 4. Statistical EDA
  * Univariate, Bivariate, and multivariate analysis
    * Delay distributions
    * Flight volume
    * Delay vs. distance
    * Delay Drivers (airlines, airports)
    * Trends by hour, day, month

### 5. Transformations 

### 6. Save & Document
  * Cleaned and saved data as CSV, pickle, parquet 
  * Tracked progress and decision through Github commits

**This README serves as the top-level documentation for this project**

## Key Questions to Answer
  * Which airports or airlines have the highest delays? Which have the highest average delays?
  * Are delays impacted by route?
  * How do delays vary by time of day? Day of week? Vary by Month?
  * If a flight is late, what's the likelihood the next flight will be late?


## Streamlit Dashboard
The streamlit dashboard is an interactive tool that allows users to play with the source data through plotting and changing of variables

## Limitations
  * BTS datasets can have missing data or can be inconsistent with their entries
  * Weather, seurity, carrier, and NAS delay specific analysis is limited due to the missing data because of limited publicly available data

        





Repo for Auburn INSY 6500 class project by Trace Warriner and Brandon Chambers. 