# %% [markdown]
# # Introduction
# ## Statement of Purpose
# The purpose of this analysis is to apply the full Exploratory Data Analysis (EDA) workflow to a real-world dataset of airline performance metrics. Our goal is to apply this workflow in order to answer meaningful question driven inquiries on U.S. airline performance metrics. Our aim is to develop a deep understanding of operational patterns, reliability factors, and delay drivers across, airlines, airports, and time periods.
# 
# ## Source Data
# * **United States Department of Transportation - U.S. Buerau of Transportation Statistics (Airlines, Airport, and Aviation)**
#     
#     URL: https://transtats.bts.gov/Fields.asp?gnoyr_VQ=FGJ
# 
# * **Federal Aviation Administration Aircraft Registration Database**
#     
#     URL: https://www.faa.gov/licenses_certificates/aircraft_certification/aircraft_registry/releasable_aircraft_download

# %% [markdown]
# # Step 0: Initial Questions To Answer
# 
# **1. What do we want to know about airline on-time performance?**
# * **How does on-time performance vary across carrier, airports, time, day, maybe aircraft?**
#   
#     - What's the overall distribution of any flight delays? 
#     -  What airline has the best and worst on-time performance? 
#     -  How do routes (short/long) correlate with performance? 
#     -  What departure time windows have the least amount of delays? Most amount of delays? 
#     -  What is the average delay per airport? per airline? per airport & airline? 
#     - What percentage of flights leave on-time? Delayed? 
#     -  What time ranges have the highest/lowest delays? 
#         - How many flights per day? 
#         - By airport? By carrier? 
#     - What is the average aircraft turnaround time by carrier? (I'd think we'd have to subtract any weather, security, or NAS delays because those are not impacted their ability to get the aircraft ready for the next flight) 
# 
# * **What delay propagation patterns can we draw?**
#   - Is there recovery or do they compound / propagate? 
#     - Are some airlines better at recovering than others? 
#   - What information can we draw from taxi times? Thinking about traffic jams at the runways due to built up delays
#   - What percent of flights are delayed 15, 30, 60+ minutes? 
#   - What is the % chance that a late arrival will cause the next flight to also be late 
#   - What is the average total time per day in delays a carrier has? 
#   - What correlations are there between delays and cancelations (mainly downstream, think about how a major storm could cause mass cancellations in a short period of time)? 
# 
# * **What factors have the greatest effect on on-time performance**
#   - Weather 
#     - What is the average number of delays per day due to weather?
#     - What percentage of days are due to weather?
#     - Which airports have the highest/most frequent weather delays?
#     - How much time is the average weather delay?
#   - Secuirty 
#     - What percentage of delays are due to security issues?
#     - How much time is the average security delay? 
#   - Carrier 
#     - Which carriers have the highest delays?
#     - How much time is the average carrier delay
#   - National Aviation System (Delay within control of ATC, not airline) 
#     - Which airports have the most/highest delays due to NAS?
#     - How much time is the average NAS delau
#     - What is the total number 
# 
# * **What is the impact to customers?**
#   - Which airports should customers expect delays
#   - What percent of flights are delayed 15, 30, 60+ minutes?
# 
# * **Ambitious Questions**
#   - What is the overall cost of delays?**
#     - Fuel, labor, etc.
# 
# 2. How will the answers be useful in decision making?
# 
# 
# ## Brandon Analysis Questions
#     -  How do routes correlate with performance? 
#     - What are the max, min, and average flight times? Is there a relationships to flight length and delays
#     -  What departure time windows have the least amount of delays? Most amount of delays? 
#     -  What time ranges have the highest/lowest delays? 
#     -How many flights per day? 
#         - By airport? By carrier? 
#     - How resilient is each carrier to delay shocks?
#         - What % of flights recover to on-time after a delay?
#     - What is the % chance that a late arrival will cause the next flight to also be late T
#     - What is the average total time per day in delays a carrier has? 
#     - Weather 
#         - What is the average number of delays per day due to weather?
#         - What percentage of days are due to weather?
#         - Which airports have the highest/most frequent weather delays?
#         - How much time is the average weather delay?
#     - Secuirty 
#         - What percentage of delays are due to security issues?
#         - How much time is the average security delay? 
#     - Are taxi times leading indicators of airport congestion?
#         - What is the relationship between taxi out times and departure delays (Wheels off)
#     
# ## Trace Analysis Questions
#     -  What's the overall distribution of any flight delays? 
#     - What airports have the highest delays?
#     -  What airline has the best and worst on-time performance? 
#     -  What is the average delay:
#         - Per airport? 
#         - Per airline? 
#         - Per airport & airline? 
#             -Can't really answer this one because some major airports are hubs for specific airlines, so the combnation of airline and airport would be obvious, skewed, and rather irrrelevant
#     - What percentage of flights leave on-time? Delayed? 
#     -What is the average aircraft turnaround time by carrier? (I'd think we'd have to subtract any weather, security, or NAS delays because those are not impacted their ability to get the aircraft ready for the next flight) 
#     - What percent of flights are delayed 15, 30, 60+ minutes? 
#     - What is the % chance that a late arrival will cause the next flight to also be late 
#     - What correlations are there between delays and cancelations (mainly downstream, think about how a major storm could cause mass cancellations in a short period of time)? 
#     - Carrier 
#         - Which carriers have the highest delays?
#         - How much time is the average carrier delay
#     - National Aviation System (Delay within control of ATC, not airline) 
#         - Which airports have the most/highest delays due to NAS?
#         - How much time is the average NAS delay?
#     - What is the likelyhood of a delay based on airline, airport, and time of day?
#     - What aircraft have the highest carrier delays?
#     - What day of the week has the highest delays?
# 
# 
# # Key Features Needed
#   1. Date
#   2. Time of Day
#   3. Carrier
#   4. Airport (Departure)
#   5. Airport (Arrival) / Destination
#   6. Flight Delay Code
#   7. Tail Number
#   8. Elapsed Time
#   9. State
#   10. Wheels Up
#   11. Wheel Down
#   12. Taxi Time 
# 
# 
# 

# %% [markdown]
# # 1. Initial Load & Reconniassance 
# ## Questions to Answer
# 1. Tidy or not?
# 2. Entities, Attributes, Observations?
# 3. Variable Types?
# 4. Shape & scale?
# 5. Any obvious problems?
# 
# ### Hypothessis
# - Relationships worth exploring
#     - Numeric
#     - Categorical
#     - Numeric vs Categorical
#     - Numeric vs Numeric 
#     -  on-time performance vs. time of day
#     -  on-time performance vs carrier
#     -  on-time performance vs airport
#     -  Carrier vs % of flights delayed
#     -  Carrier vs departure / arrival delays
# 

# %% [markdown]
# ## Importing Libraries

# %%
import pandas as pd
import numpy as np
from pathlib import Path
import zipfile
import seaborn as sns
import matplotlib.pyplot as plt
import statsmodels.api as sm

# %% [markdown]
# ## Reading In All The Source Data

# %%
df = pd.read_parquet("../data/bts_all.parquet") #initital load of parquet file containing main DF data from Beaurue of Transportation Stats
df_aircraft = pd.read_csv("../data/Aircraft.csv") #csv file of aircraft tail numbers and their makes and models
df_airports = pd.read_csv("../data/Airports.csv") #csv file of airport codes and their country
df_airline = pd.read_csv("../data/Airline.csv") #csv file of airline codes and they're full names

# %% [markdown]
# ## Data Preview

# %%
df.info()

# %% [markdown]
# * Expected:
#   - FlightDate to be datetime
#   - CRSDepTime & CRSArrTime to be datetime
#   - DepTime & ArrTime to be datatime
#   - WheelsOff & WheelsOn to be datetime
# 
# * Fixes:
#   - Update all expected datetime objects to their appropriate datetime 

# %%
df.describe()

# %%
df.shape

# %%
df.head()

# %% [markdown]
# ## Missing Data

# %%
df.columns[df.isna().any()].tolist()

# %% [markdown]
# ## Missing Data

# %% [markdown]
# * Missing:
#   - Tail Numbers
#     - Not super critical to fix since this would really only be used to track delays by aircraft. If we don't plan to do that, then we can just drop the column entirely. We COULD, however, clean the data frame up a little bit to show only the flights associated with large carrier airlines and remove private flights
#   - Departure Time
#     - Similar to Tail Numbers, we could remove private flights to see how this changes. We'll have to assess if removing a percentage of the data for each 
#   - Departure Delay
#   - Taxi Out
#   - Wheels Off
#   - Wheels On
#   - 
# 
# * Notes:
#   - We'll have to assess what rows we want to eliminate whether that's private flights or flights with no record of departure or arrival times
#   
# 

# %% [markdown]
# # 2. Data Quality

# %% [markdown]
# - What is broken, missing, or suspicious?
# - Are the dtypes correct for each variable?
# - Do the values make sense?
# - Where is data missing and how much?
# - Are there duplicates or outliers?
# - Is the data trustworthy as is?

# %%
#Displaying dataframe of missing values for each feature
#num_flights = len(df)
att_missing = df.isna().sum().sort_values(ascending=False)
pct_missing = df.isna().mean().sort_values(ascending=False)
# missing = pd.DataFrame({
#       'missing_count': df.isna().sum(),
#       'percent_missing': (df.isna().sum()/len(df))*100
# # })
missing = pd.DataFrame({
      'missing_count': att_missing,
      'percent_missing': (pct_missing*100).round(1)
})
missing

# %% [markdown]
# ## Checking to make sure dates of last and first flights are within the proper date range for which data was collected

# %%
#Checking that earliest date of dataset to be January 1, 2020
earliest_flight = df['FlightDate'].min()
latest_flight = df['FlightDate'].max()
print("Earliest Flight Date:", earliest_flight.date())
print("Latest Flight Date:", latest_flight.date())

# %% [markdown]
# # 3. Cleaning Decisions

# %% [markdown]
# - Motivation
#     - How do I fix problems without corrupting the truth?
# - Questions
#     - Drop or fix? What's the impact on the analysis?
#     - What the missingness mechanism (MCAR / MAR / MNAR)
#     - Are outliers legit or are they errors?
#     - What assumptions am I making?
# - Hypothesis & Iteration
#     - What biases might my cleaning decisions introduce
#     - What sensitivity analyses should I run?
# - Iteration Signals
#     - Cleaning reveals new issues --> back to phase 2
#     - Decisions feel arbitrary --> need domain expertise  

# %% [markdown]
# For the cleaning decisions section the goal is to correct structural issues within the dataframe while avoiding unintended transformations that may distort the true data. We will drop rows, and coluns with missing data or data that is not applicable to our analyses. All the decisions made will ideally reflect best knoweldge of the airline operations domain

# %% [markdown]
# ## Converting To Proper Dtypes & Time Fields

# %%
df['FlightDate'] = pd.to_datetime(df['FlightDate'], errors="coerce") #Displaying only date for Flight Date

# Turn departure time into a datetime object for better analysis
# This require combining the time information with flight date

# Prep a series of strings to comibe with flight dates
crs_str = (
    df["CRSDepTime"]
    .astype(str)
    .str.zfill(4)     # "0730", "1745"
)

# Combine FL_DATE + hh:mm into a true datetime
df["CRSDepDateTime"] = pd.to_datetime(
    df["FlightDate"].dt.strftime("%Y-%m-%d") + " " +
    crs_str.str.slice(0, 2) + ":" + crs_str.str.slice(2, 4),
    format="%Y-%m-%d %H:%M",
    errors="coerce"
)

# Drop any rows where we still failed to build a datetime
df = df[df["CRSDepDateTime"].notna()].copy()
df

# df = df["CRSDepDateTime"].unique()
# df

#df['FlightDate'] = pd.to_datetime(df['FlightDate'], errors="coerce") #Displaying only date for Flight Date
# #df['FlightDate'] = df['FlightDate'].dt.strftime("%d/%m/%Y") #Formatting date to be in dd/mm/yyyy format

# df['CRSDepTime'] = df['CRSDepTime'].astype(str).str.zfill(4) #Converting int64 to 4 digit string
# df['CRSArrTime'] = df['CRSArrTime'].astype(str).str.zfill(4) #Converting int64 to 4 digit string
# df['CRSDepTime'] = pd.to_datetime(df['CRSDepTime'], format="%H%M", errors='coerce') #Converting string to datetime with format proper hours and minutes format. Any invalid values will become NaT
# df['CRSArrTime'] = pd.to_datetime(df['CRSArrTime'], format="%H%M", errors='coerce') #Converting string to datetime with format proper hours and minutes format. Any invalid values will become NaT
# df.info()
# #df

# %% [markdown]
# ## Handling Missing Values

# %%
#Merging with Aircraft.csv
df['Tail_Number'] = df['Tail_Number'].str.lstrip('N') #Removing leading "N" from Tail Number (this is to be able to properly match the tail number with the correct make and model aircraft from the Aircraft.csv



# %% [markdown]
# ## Additional cleaning and consoladating of main DataFrame

# %%
#Merging with Aircraft.csv
df['Tail_Number'] = df['Tail_Number'].str.lstrip('N') #Removing leading "N" from Tail Number (this is to be able to properly match the tail number with the correct make and model aircraft from the Aircraft.csv

df_aircraft = df_aircraft.drop(columns='MFR MDL CODE') #Dropping column, 'MFR MDL CODE' in aircraft DF

df_aircraft = df_aircraft.rename(columns= { #Changing feature names for Aircraft.csv
    'N-NUMBER': 'Tail_Number',
    'MFR': 'Manufacturer',
    'NO-SEATS': 'Number_of_Seats'
})
df = df.merge(df_aircraft, on='Tail_Number', how='left') #Merging Aircraft DF

#Merging with Airport.csv
dep_airports = df_airports.copy()
dep_airports = dep_airports.rename(columns={'lid': 'DepAirport_code',
                                          'country': 'dep_country'})
df = df.merge(dep_airports[['DepAirport_code', 'dep_country']], left_on='Origin', right_on='DepAirport_code', how='left')

dest_airports = df_airports.copy()
dest_airports = dest_airports.rename(columns={'lid': 'DestAirport_code',
                                          'country': 'dest_country'})
df = df.merge(dest_airports[['DestAirport_code', 'dest_country']], left_on='Dest', right_on='DestAirport_code', how='left')

mask = (df['dep_country'] != 'US') | (df['dest_country'] != 'US')
df.loc[mask, 'international'] = 'International'
df.loc[~mask, 'international'] = 'Domestic'
df = df.drop(columns=['DepAirport_code', 'dep_country', 'DestAirport_code', 'dest_country'])

#Merging with Airline.csv
df_airline = df_airline.rename(columns= {'OP_UNIQUE_CARRIER': 'Reporting_Airline'})
df = df.merge(df_airline, on='Reporting_Airline', how='left')
df = df.rename(columns= { 'international': 'flight_type',
                          'Description': 'Airline'})
df['Airline'] = df['Airline'].replace({
    'American Airlines Inc.': 'American Airlines',
    'Alaska Airlines Inc.': 'Alaska Airlines',
    'Delta Air Lines Inc.': 'Delta Airlines',
    'Frontier Airlines Inc.': 'Frontier Airlines',
    'Hawaiian Airlines Inc.': 'Hawaiian Airlines',
    'PSA Airlines Inc.': 'PSA Airlines',
    'Skywest Airlines Inc.': 'Skywest Airlines',
    'United Air Lines Inc.': 'United Airlines',
    'Southwest Airlines Co.': 'Southwest Airlines',
})        
df = df.drop(columns=['Reporting_Airline'])

air_unique = df['Airline'].unique().tolist() #Show number of unique airlines in the main DF
air_counts = df['Airline'].value_counts(dropna=False) #Count # of occurrences for each unique airline, including rows with NaN values. We will drop rows with NaN later
#air_show = df[df['Airline'].isna()].head(5) #Show first 5 rows of observations with NaN for airline
df = df.dropna(subset=['Airline']) #Drop rows with no company airline. These are likely private carriers we want to exclude. Only looking to capture major airlines
# df = df[df['DepDelay'].isna()].head(5)
df.head()


# %%
#Displaying number of domestic flights vs. international
inter = df['flight_type'].value_counts()
inter

# %% [markdown]
# Things to note:
# 1. Some departure and/or arrival delays are noted but are not given is a designation as a reaosn to why
# 2. All rows for each delay category are listed as NaN is there was no report of a dealy specifically cause by one of the categories
# 3. Some flight records do not have a tail number recorded. This could make tracking based on routes skewed as well as show no make or model for that aircraft
#     - For our purposes, for filtering by aircraft, we will only consider records that have aircraft make and model listed
#  
# 

# %% [markdown]
# #### Checking to make sure the last and first flights of dataset are within the proper date which for which they were collected for

# %%
#Checking that earliest date of dataset to be January 1, 2020
earliest_flight = df['FlightDate'].min()
latest_flight = df['FlightDate'].max()
print("Earliest Flight Date:", earliest_flight.date())
print("Latest Flight Date:", latest_flight.date())

# %% [markdown]
# ### Summary Statistics

# %%
df.columns

# %%
df.info()
df.describe
df.shape


# %%
#Displaying dataframe of missing values for each feature
num_flights = len(df)
missing = pd.DataFrame({
    'missing_count': df.isna().sum(),
    'percent_missing': (df.isna().sum()/len(df))*100
})
missing

# %%
#Displaying number of non-NaN rows for each column feature
num_flights = len(df)
confirm = pd.DataFrame({
    'missing_count': df.notna().sum(),
    'percent_missing': (df.notna().sum()/len(df))*100
})
confirm

# %% [markdown]
# # 4. Statistical EDA

# %% [markdown]
# - Motivation
#   - What patterns, relationships stories exist in the data?
# - Driving Questions
#   - What's "typical" for each variable?
#   - How do variables relate to each other?
#   - Do patterns hold across subgroups?
#   - What surprises emerge?

# %% [markdown]
# In this Exploratory Data Analysis (EDA) is to explore and quantify key patterns, relationships, and operational behaviors within the Beaueru of Transportation Statistics On-TIme Performance dataset. In this phase, we will seek to move beyond structuure and quaity checking and begin to analyze how flight delays vary across airlines, airports, and time periods. By applying the techniques learned in class, our aim is to identify tendencies, distributions, correlations, and group level difference that reveal how and why delays occur. In addition we hope to provide some general stats that give individual reviews a sense of scale or magnitude at which the airline industry operates at. 

# %% [markdown]
# # What is the distributions of departure delays?

# %%
df = df.copy()
df = df.dropna(subset=['DepTime']) 
df
#df['DepDelay'].plot(kind='hist', bins=10, figsize=(10,4))


# %% [markdown]
# # What percent of reported delays were NOT given a specific delay code?

# %% [markdown]
# # What percent of flights leave on time/delayed?

# %%
#Make copy of main dataframe & drop rows with NaN in the DepTime column
df = df.copy()
df = df.dropna(subset=['DepTime']) 

#Counting total number of applicable flights
dep_count = len(df) 

#Calculating percent of flights that are late
dep_late = (df['DepDelay'] > 0).mean()

#Calculating percent of flights that are on-time
on_time = (df['DepDelay'] == 0).mean() 

#Calculating percent of flights that are early
dep_early = (df['DepDelay'] < 0).mean() 

#Printing results
print(f"Percent of Departures That Are Late: {dep_late:.1%}")
print(f"\nPercent of Departures That Are On-Time: {on_time:.1%}")
print(f"\nPercent of Departures That Are Early: {dep_early:.1%}")


# %% [markdown]
# ### How does this vary month by month or year by year?

# %%
#Make copy of main dataframe & check dtypes
df = df.copy()
df,info()

# %% [markdown]
# FlightDate dtype is already a datetime object

# %%
#Drop rows with NaN in the DepTime column
df = df.dropna(subset=['DepTime']) 

#Add column 'Year'
df['Year'] = df['FlightDate'].dt.year

#Counting total number of applicable flights
dep_count = len(df) 

#Calculating percent of flights that are late
dep_late = (df['DepDelay'] > 0).mean()

#Calculating percent of flights that are on-time
on_time = (df['DepDelay'] == 0).mean() 

#Calculating percent of flights that are early
dep_early = (df['DepDelay'] < 0).mean() 

#Printing results
print(f"Percent of Departures That Are Late: {dep_late:.1%}")
print(f"\nPercent of Departures That Are On-Time: {on_time:.1%}")
print(f"\nPercent of Departures That Are Early: {dep_early:.1%}")

# %% [markdown]
# ## What is the % chance that a late arrival will cause the next flight to also be late?

# %% [markdown]
# Check and make sure dytpes are correct

# %%
df = df.copy()
df.info()

# %%
df = df.sort_values(['Tail_Number', 'FlightDate', 'DepTime'])
df['next_delay'] = df.groupby('Tail_Number')['DepDelay'].shift(-1)
df['late_arr'] = df['ArrDelay'] > 0
df['next_dep_delay'] = df['next_delay'] > 0
late_arr = df[df['late_arr'] == True]
probability = late_arr['next_dep_delay'].mean()
print(f"\nLikelyhood a late arrival causes next flight to be late: {probability: .2%}")

# %% [markdown]
# ## What percent of flights are delayed 15, 30, 60 minutes?

# %%
df = df.copy()
df = 

# %%
df = df['15_mins'].astype(float)
df['15_mins'] = df['DepDelay'] <= 15
fifteen_mins = df['15_mins'].sum()
fifteen_mins
# df['30_mins'] = df['DepDelay'] <= 30
# df['60_mins'] = df['DepDelay'] <= 60

# delay_mins = df.groupby([15])

# %% [markdown]
# ### What is the likelyhood of a delay by airline?

# %% [markdown]
# First we will start the exploration by finding the number of flights for each airline

# %%

#Counting the number of flights for each airline
airline_flights = df_delay.groupby('Airline').size().reset_index(name='No. of Flights').sort_values('No. of Flights', ascending=False)

#Cleaning DF to only show specified column features as well as only show rows that have departure or arrival delays greater than 0
df_clean = df[['FlightDate', 'DepDelay', 'ArrDelay', 'Airline']]
df_delays = df_clean[(df_clean['DepDelay'] > 0) | (df_clean['ArrDelay'] > 0)]

#Grouping by Airline, showing the number of delays for departure and arrivals respectively
airline_dep_delay = (df_delays[df_delays['DepDelay']>0].groupby('Airline').size().reset_index(name='Departure_Delays'))
airline_arr_delay = (df_delays[df_delays['ArrDelay']>0].groupby('Airline').size().reset_index(name='Arrival_Delays'))
delays = airline_dep_delay.merge(airline_arr_delay, on='Airline', how='outer')
delays['Total_Delays'] = delays['Departure_Delays'] + delays['Arrival_Delays']

#Percent chance a flight is delayed by airline for either a departure or an arrival
delays['chance_of_dep_delay'] = ((delays['Departure_Delays'] / airline_flights['No. of Flights'])*100).round(1)
delays['chance_of_arr_delay'] = ((delays['Arrival_Delays'] / airline_flights['No. of Flights'])*100).round(1)
delays



# %%
airline_delay = df.groupby('Airline')

# %% [markdown]
# ### How does this vary by airline?

# %% [markdown]
# ### How does this cary by airport?

# %% [markdown]
# # What airports have the highest/worst delays?
# 
# We will measure this in two ways:
# 
#     1. Departure Delays
#     2. Arrival Delays
#     3. Total Delays 
# 
# Note: Some delays are recorded but are not designated as carrier, weather, NAS, or late aircraft related

# %%
#Airports with worst departure and arrival delays
airports_origin = df['Origin'].unique().tolist()
airports_dest = df['Dest'].unique().tolist()
worst_dep = df.groupby('Origin')['DepDelay'].sum().sort_values(ascending=False).reset_index()
worst_arr = df.groupby('Dest')['ArrDelay'].sum().sort_values(ascending=False).reset_index()

# %%
fig, axes = plt.subplots(2, 1, figsize=(12, 10))

# --- Plot 1: Departure delays ---
sns.barplot(
    data=worst_dep.head(15),
    x='Origin', 
    y='DepDelay',
    palette='Reds_r',
    ax=axes[0]
)
axes[0].set_title("Airports with Highest Departure Delays")
axes[0].set_xlabel("")
axes[0].set_ylabel("Departure Delay (min)")
axes[0].tick_params(axis='x', rotation=45)

# --- Plot 2: Arrival delays ---
sns.barplot(
    data=worst_arr.head(15),
    x='Dest', 
    y='ArrDelay',
    palette='Blues_r',
    ax=axes[1]
)
axes[1].set_title("Airports with Highest Arrival Delays")
axes[1].set_xlabel("Airport")
axes[1].set_ylabel("Arrival Delay (min)")
axes[1].tick_params(axis='x', rotation=45)

plt.tight_layout()
plt.show()

# %% [markdown]
# What if we investigated by month or year for each

# %%
df = df.copy()
df['Year'] = df['FlightDate'].dt.year #extracting year
df['Month'] = df['FlightDate'].dt.month #extracting month

#Departures
worst_dep_yr = df.groupby(['Year', 'Origin']).agg( #groupby year and origin airport to aggegrate sum, mean and median of depdelays per year and sort them in ascending order by total delays
    total_dep_delays=('DepDelay', 'sum'),
    avg_dep_delay=('DepDelay', 'mean'),
    median_dep_delay=('DepDelay', 'median')
).sort_values(['Year', 'total_dep_delays'], ascending=[True,False]).groupby('Year').head(5)

worst_dep_mo = df.groupby(['Month', 'Origin']).agg( #groupby month and origin airport to aggegrate sum, mean and median of depdelays per month and sort them in ascending order by total delays
    total_dep_delays=('DepDelay', 'sum'),
    avg_dep_delay=('DepDelay', 'mean'),
    median_dep_delay=('DepDelay', 'median')
).sort_values(['Month', 'total_dep_delays'], ascending=[True,False]).groupby('Month').head(5)

#Arrivals
worst_dest_yr = df.groupby(['Year', 'Dest']).agg( #groupby year and origin airport to aggegrate sum, mean and median of depdelays per year and sort them in ascending order by total delays
    total_arr_delays=('ArrDelay', 'sum'),
    avg_arr_delay=('ArrDelay', 'mean'),
    median_arr_delay=('ArrDelay', 'median')
).sort_values(['Year', 'total_arr_delays'], ascending=[True,False]).groupby('Year').head(5)

worst_dest_mo = df.groupby(['Month', 'Dest']).agg( #groupby month and origin airport to aggegrate sum, mean and median of depdelays per month and sort them in ascending order by total delays
    total_arr_delays=('ArrDelay', 'sum'),
    avg_arr_delay=('ArrDelay', 'mean'),
    median_arr_delay=('ArrDelay', 'median')
).sort_values(['Month', 'total_arr_delays'], ascending=[True,False]).groupby('Month').head(5)

worst_dest_mo

# %% [markdown]
# Now we plot 

# %%
# Reset index to make columns available
plot_dep = worst_dep_yr.reset_index()
plot_arr = worst_dest_yr.reset_index()

years = sorted(plot_dep['Year'].unique())

for yr in years:
    # Filter data for the given year
    dep_data = plot_dep[plot_dep['Year'] == yr]
    arr_data = plot_arr[plot_arr['Year'] == yr]

    # Create figure with 2 side-by-side subplots
    fig, axes = plt.subplots(1, 2, figsize=(16, 6))

    # ----- LEFT: Departure Delays -----
    sns.barplot(
        data=dep_data,
        x='Origin',
        y='total_dep_delays',
        ax=axes[0],
        palette='Reds'
    )
    axes[0].set_title(f"Top 5 Worst Departure Delay Airports in {yr}", fontsize=14)
    axes[0].set_xlabel("Origin Airport")
    axes[0].set_ylabel("Total Departure Delay (minutes)")
    axes[0].tick_params(axis='x', rotation=45)

    # ----- RIGHT: Arrival Delays -----
    sns.barplot(
        data=arr_data,
        x='Dest',
        y='total_arr_delays',
        ax=axes[1],
        palette='Blues'
    )
    axes[1].set_title(f"Top 5 Worst Arrival Delay Airports in {yr}", fontsize=14)
    axes[1].set_xlabel("Destination Airport")
    axes[1].set_ylabel("Total Arrival Delay (minutes)")
    axes[1].tick_params(axis='x', rotation=45)

    plt.tight_layout()
    plt.show()

# %%
# Reset index to make Month and Origin real columns
plot_mo = worst_dep_mo.reset_index()

months = sorted(plot_mo['Month'].unique())
num_months = len(months)

# Always create a grid of subplots (4 rows x 3 columns for 12 months)
rows = 4
cols = 3
fig, axes = plt.subplots(rows, cols, figsize=(20, 16), squeeze=False)
axes = axes.flatten()

# Plot each month in its own subplot
for i, mo in enumerate(months):
    ax = axes[i]
    data = plot_mo[plot_mo['Month'] == mo]

    sns.barplot(
        data=data,
        x='Origin',
        y='total_dep_delays',
        ax=ax,
        palette='Blues'
    )

    ax.set_title(f"Top 5 Worst Airports in Month {mo}", fontsize=12)
    ax.set_xlabel("Origin Airport")
    ax.set_ylabel("Total Departure Delay (minutes)")
    ax.tick_params(axis='x', rotation=45)

# Turn off unused subplots (e.g., if dataset has fewer than 12 months)
for j in range(i+1, len(axes)):
    axes[j].axis("off")

plt.tight_layout()
plt.show()


# %%
# Reset indices
plot_dep_mo = worst_dep_mo.reset_index()
plot_arr_mo = worst_dest_mo.reset_index()

months = sorted(plot_dep_mo['Month'].unique())

# Optional month name mapping (prettier charts)
month_labels = {
    1:"Jan", 2:"Feb", 3:"Mar", 4:"Apr",
    5:"May", 6:"Jun", 7:"Jul", 8:"Aug",
    9:"Sep", 10:"Oct", 11:"Nov", 12:"Dec"
}

for mo in months:
    dep_data = plot_dep_mo[plot_dep_mo['Month'] == mo]
    arr_data = plot_arr_mo[plot_arr_mo['Month'] == mo]

    fig, axes = plt.subplots(1, 2, figsize=(16, 6))

    # ----- LEFT: Departure Delays -----
    sns.barplot(
        data=dep_data,
        x="Origin",
        y="total_dep_delays",
        ax=axes[0],
        palette="Reds"
    )
    axes[0].set_title(f"Top 5 Worst Departure Airports in {month_labels[mo]}", fontsize=14)
    axes[0].set_xlabel("Origin Airport")
    axes[0].set_ylabel("Total Departure Delay (minutes)")
    axes[0].tick_params(axis='x', rotation=45)

    # ----- RIGHT: Arrival Delays -----
    sns.barplot(
        data=arr_data,
        x="Dest",
        y="total_arr_delays",
        ax=axes[1],
        palette="Blues"
    )
    axes[1].set_title(f"Top 5 Worst Arrival Airports in {month_labels[mo]}", fontsize=14)
    axes[1].set_xlabel("Destination Airport")
    axes[1].set_ylabel("Total Arrival Delay (minutes)")
    axes[1].tick_params(axis='x', rotation=45)

    plt.tight_layout()
    plt.show()

# %% [markdown]
# We can confirm that consistenly, Dallas Fort-Worth International Airport has the worst departure flight delays of any airport in the U.S.

# %% [markdown]
# ### Question: What airlines have the best/worst on-time performance?
# 
# We will look at this mainly from a departure standpoint 

# %%
df = df.copy()

worst_airline = df.groupby(['Airline']).agg( #groupby year and origin airport to aggegrate sum, mean and median of depdelays per year and sort them in ascending order by total delays
    total_dep_delays=('DepDelay', 'sum'),
    avg_dep_delay=('DepDelay', 'mean'),
    median_dep_delay=('DepDelay', 'median')
).sort_values(['total_dep_delays'], ascending=[False]).groupby('Airline').head(5)
worst_airline


# %% [markdown]
# Here we can see that Skywest and American Airline round out the top two worst airlines for departure delays and Alaska and Republic Airlines round out the best for departure delays
# Note: A key consideration is that Skywest, PSA, Republic, and Envoy are all subsidiaries of either American, Delta, or United which could add or reduce each airlines performance

# %% [markdown]
# # What day of the week has the worst delays?

# %%
df = df.copy()
df['day_of_week'] = df['FlightDate'].dt.day_name()
df
day_wk_delay= df.groupby('day_of_week').agg( #groupby month and origin airport to aggegrate sum, mean and median of depdelays per month and sort them in ascending order by total delays
    flights_wk=('FlightDate', 'size'),
    total_day_delays=('DepDelay', 'sum'),
    avg_day_delay=('DepDelay', 'mean'),
    median_day_delay=('DepDelay', 'median')
).sort_values('total_day_delays', ascending=False)
day_wk_delay


# %%
day_wk_delay['total_day_delays'].plot(
    kind='bar',
    figsize=(10,5),
    title='Total Departure Delay Minutes by Day of Week',
    ylabel='Total Delay (minutes)'
)

# %%
day_wk_delay['avg_day_delay'].plot(
    kind='bar',
    figsize=(10,5),
    title='Average Departure Delay by Day of Week',
    ylabel='Average Delay (minutes)'
)

# %% [markdown]
# This would make sense as Thursday and Friday are typically when people will fly out to go on a vacation

# %%
day_wk_delay['flights_wk'].plot(
    kind='bar',
    figsize=(10,5),
    title='Number of Flights by Day of Week',
    ylabel='Number of Flights'
)

# %% [markdown]
# ### What day of the week has the worst delays across airlines?

# %%
df = df.copy()
df['day_of_week'] = df['FlightDate'].dt.day_name()
air_delay_wk = df.groupby(['Airline', 'day_of_week']).agg(
     flights_wk=('FlightDate', 'size'),
    total_day_delays=('DepDelay', 'sum'),
    avg_day_delay=('DepDelay', 'mean'),
    median_day_delay=('DepDelay', 'median')
).sort_values('Airline', ascending=[False])
air_delay_wk



# worst_dep_mo = df.groupby(['Month', 'Origin']).agg( #groupby month and origin airport to aggegrate sum, mean and median of depdelays per month and sort them in ascending order by total delays
#     total_dep_delays=('DepDelay', 'sum'),
#     avg_dep_delay=('DepDelay', 'mean'),
#     median_dep_delay=('DepDelay', 'median')
# ).sort_values(['Month', 'total_dep_delays'], ascending=[True,False]).groupby('Month').head(5)

# %% [markdown]
# # What is the likelyhood of a delay based on airline?

# %%
#Counting the number of flights for each airline 
df = df.copy()
airline_flights = df_delay.groupby('Airline').size().reset_index(name='number_of_flights').sort_values('number_of_flights', ascending=False) 

#Cleaning DF to only show specified column features as well as only show rows that have departure or arrival delays greater than 0 
df_clean = df[['FlightDate', 'DepDelay', 'ArrDelay', 'Airline']] 
df_delays = df_clean[(df_clean['DepDelay'] > 0) | (df_clean['ArrDelay'] > 0)] 

#Grouping by Airline, showing the number of delays for departure and arrivals respectively 
airline_dep_delay = (df_delays[df_delays['DepDelay']>0].groupby('Airline').size().reset_index(name='Departure_Delays')) 
airline_arr_delay = (df_delays[df_delays['ArrDelay']>0].groupby('Airline').size().reset_index(name='Arrival_Delays')) 
delays = airline_dep_delay.merge(airline_arr_delay, on='Airline', how='outer') 
delays['Total_Delays'] = delays['Departure_Delays'] + delays['Arrival_Delays'] 

#Merging airline_flight DF with delays DF
delays = delays.merge(airline_flights[['Airline', 'number_of_flights']], on='Airline', how='left')

#Percent chance a flight is delayed by airline for either a departure or an arrival 
delays['chance_of_dep_delay'] = ((delays['Departure_Delays'] / airline_flights['number_of_flights'])*100).round(1) 
delays['chance_of_arr_delay'] = ((delays['Arrival_Delays'] / airline_flights['number_of_flights'])*100).round(1)
delays

# %%
delays.sort_values('Total_Delays', ascending=False).plot(
    x='Airline', y='Total_Delays', kind='bar', figsize=(10,5), title='Total Delays by Airline'
)
plt.ylabel("Total Delays")
plt.show()

# %%
delays.plot(
    x='Airline',
    y=['Departure_Delays', 'Arrival_Delays'],
    kind='bar',
    figsize=(12,6),
    title='Departure vs Arrival Delays by Airline'
)
plt.ylabel("Number of Delays")
plt.show()

# %%
delays.sort_values('chance_of_dep_delay').plot(
    x='Airline',
    y='chance_of_dep_delay',
    kind='barh',
    figsize=(8,6),
    title='Percentage Chance of Departure Delay by Airline'
)
plt.xlabel("Percent (%)")
plt.show()

# %%
plt.figure(figsize=(8,6))
plt.scatter(delays['number_of_flights'], delays['Total_Delays'])
plt.xlabel("Number of Flights")
plt.ylabel("Total Delays")
plt.title("Flights vs Total Delays")
plt.show()

# %% [markdown]
# # Brandon Inputs

# %%
df.tail()

# %%
# I DONT THINK WE NEED THIS ANYMORE

# df_aircraft = pd.read_csv("../data/Raw/Aircraft.csv")
# df_aircraft

# %%
# I DON'T THINK WE NEED THIS ANYMORE


# #Changing feature names for aircraft DF
# mod_aircraft = df_aircraft.rename(columns= {
#     'N-NUMBER': 'Tail_Number',
#     'MFR': 'Manufacturer',
#     'NO-SEATS': 'Number_of_Seats'
# })
# mod_aircraft

# df_merged = df.merge(mod_aircraft, on='Tail_Number', how='left')
# df_merged

# %% [markdown]
# ### How do routes correlate with delays?
# We're looking to assess how delays vary by route. In this context, we'll define a route as a departure/arrival airport pair.  We are interested in identifying the routes with the highest average delay per flight. 

# %%
#create a route column from origin and destination columns
df["route"] = df["Origin"] + "_" + df["Dest"]

#build a dataframe of flight delay information for each route
route_delay = (
    df.groupby("route")
      .agg(total_arr_delay=("ArrDelay", "sum"),
           n_flights=("ArrDelay", "count"))
      .sort_values("n_flights", ascending=False)
)

# %%
route_delay['avg_delay_per_flight'] = route_delay['total_arr_delay'] / route_delay['n_flights']
route_delay.head()

# %% [markdown]
# #### Establish a minimum number of flights
# To avoid the results being skewed by routes with very few flights, we'll establish a minimum threshold of number of flights in order for a route to be considered in the analysis. To do this, we'll start with a cutoff that includes 80% of all flights and adjust as necessary.

# %%
# Compute the cumulative percentage of total flights as routes are sorted by descending flight count
route_delay["cumulative_share"] = route_delay["n_flights"].cumsum() / route_delay["n_flights"].sum()
route_delay

# %%
#Establish 80% cutoff mark
cutoff_row = route_delay[route_delay["cumulative_share"] >= 0.80].iloc[0]
cutoff_value = cutoff_row["n_flights"]
cutoff_value


# %%
plt.figure(figsize=(14,6))
sns.barplot(
    data=route_delay.sort_values("n_flights", ascending=False),
    x=route_delay.sort_values("n_flights", ascending=False).index,
    y="n_flights",
    color="steelblue"
)
plt.title("Number of Flights per Route (Sorted)")
plt.xlabel("Route (sorted by flight volume)")
plt.ylabel("Number of Flights")
plt.xticks([], [])   #hide x-axis labels
plt.show()

# %%
sns.histplot(route_delay["n_flights"], bins=100)
plt.title("Distribution of Route Flight Counts")
plt.xlabel("Number of Flights")
plt.ylabel("Number of Routes")
plt.show()


# %% [markdown]
# Given the above histogram and bar char, there is a long tail of lower-volume routes that might be of interest.  Let's up the threshold to 95% of flights.

# %%
#Establish 95% cutoff mark
cutoff_row = route_delay[route_delay["cumulative_share"] >= 0.95].iloc[0]
cutoff_value = cutoff_row["n_flights"]
cutoff_value

# %% [markdown]
# A minimum threshold of 1623 flights for a route covers 95% of all flights. Now, we'll find the average delay time per flight for all routes with 1623 flights or more.

# %%
min_flights = 1623


filtered_routes = route_delay[route_delay["n_flights"] >= min_flights]

# Sort by highest avg delay per flight
filtered_routes = filtered_routes.sort_values(
    "avg_delay_per_flight",
    ascending=False
)
filtered_routes.drop(columns=["cumulative_share"], inplace=True) # cumulative share doesn't make sense in this context



# %%
worst_routes = filtered_routes.head()
worst_routes

# %%
best_routes = filtered_routes.tail()
best_routes

# %% [markdown]
# Based on this analysis, there is no standout commonality among the best and worst routes for delays or early arrivals.  Let's explore volume per day at the airports in the top 5 and bottom 5 in the delay data to see if there is a signal there.

# %%
top_worst_airports = ["BDL", "SJU", "DCA", "ASE", "DFW", "MDT", "EYW", "PHL"]
top_best_airports  = ["BTM", "SLC", "KOA", "OAK", "RHI", "MSP", "TYS", "DTW", "LIH", "DEN"]

airport_daily_volume = (
    df.melt(
        id_vars=["FlightDate"],
        value_vars=["Origin", "Dest"],
        var_name="type",
        value_name="airport"
    )
    .groupby(["airport", "FlightDate"])
    .size()
    .reset_index(name="flights_per_day")
)


# %%
# Average volume / day at the airports in the worst routes
worst_filtered = (
    airport_daily_volume[airport_daily_volume["airport"].isin(top_worst_airports)]
)
worst_filtered_avg = worst_filtered.groupby("airport")["flights_per_day"].mean()

# %%
# Average volume / day at the airports in the best routes
best_filtered = (
    airport_daily_volume[airport_daily_volume["airport"].isin(top_best_airports)]
)
best_filtered_avg = best_filtered.groupby("airport")["flights_per_day"].mean()

# %%
def create_route_volume_df(route_df,filtered_avg):
    """
    Given a dataframe of routes and a series of averages,
    create a dataframe of routes with volume totals and differences
    """
    rows = []
    for route in route_df.index:
        origin,dest = route.split("_")
        volume_diff = filtered_avg[origin] - filtered_avg[dest]
        total_volume = filtered_avg[origin] + filtered_avg[dest]
        rows.append({
            "route": route,
            "origin": origin,
            "dest": dest,
            "volume_diff": volume_diff,
            "total_volume": total_volume
        })
    
    return pd.DataFrame(rows).set_index("route")


    
    

# %%
best_route_volumes_df = create_route_volume_df(best_routes,best_filtered_avg)
best_route_volumes_df

# %%
worst_route_volumes_df = create_route_volume_df(worst_routes,worst_filtered_avg)
worst_route_volumes_df

# %%
#Best vs Worst Average Total Volumes
print("Best Route Total Volume:",best_route_volumes_df['total_volume'].mean())
print("Worst Route Total Volume:",worst_route_volumes_df['total_volume'].mean())

# %%
#Best vs Worst Average Volume Difference
print("Best Route Volume Diff:",best_route_volumes_df['volume_diff'].mean())
print("Worst Route Volume Diff:",worst_route_volumes_df['volume_diff'].mean())

# %% [markdown]
# There is signal in both the difference and totals in volumes between an origin and destination for more exploration. Next, we'll do a regression of these two variables on the entire set.

# %%
avg_daily_volume = airport_daily_volume.groupby("airport")["flights_per_day"].mean()
route_volume_df = create_route_volume_df(route_delay,avg_daily_volume)

# %%
merged_route_volumes = route_volume_df.merge(route_delay,on="route")

# %%
merged_route_volumes = merged_route_volumes[merged_route_volumes["n_flights"] >= min_flights]
merged_route_volumes.head()

# %%
#Single Variate Regression for volume difference
X = merged_route_volumes[["volume_diff"]] #predictor
y = merged_route_volumes["avg_delay_per_flight"] #predictand

X = sm.add_constant(X) #Intercept

# Fit model
model = sm.OLS(y, X).fit()

print(model.summary())


# %%
#Plot Avg Delay per FLight vs Volume Difference

x = merged_route_volumes["volume_diff"]
y = merged_route_volumes["avg_delay_per_flight"]

# Fit linear trend
m, b = np.polyfit(x, y, 1)

plt.figure(figsize=(8,5))
plt.scatter(x, y, alpha=0.4, label="Data")
plt.plot(x, m*x + b, color="red", label="Trend Line")

plt.xlabel("Volume Difference (Origin - Destination)")
plt.ylabel("Average Delay per Flight (min)")
plt.title("Avg Delay per Flight vs Volume Difference")
plt.legend()
plt.grid(True)
plt.show()


# %%
#Single Variate Regression for total volume
X = merged_route_volumes[["total_volume"]] #predictor
y = merged_route_volumes["avg_delay_per_flight"] #predictand

X = sm.add_constant(X) #Intercept

# Fit model
model = sm.OLS(y, X).fit()

print(model.summary())

# %%
#Plot Avg Delay per FLight vs Total Volume

x = merged_route_volumes["total_volume"]
y = merged_route_volumes["avg_delay_per_flight"]

# Fit linear trend
m, b = np.polyfit(x, y, 1)

plt.figure(figsize=(8,5))
plt.scatter(x, y, alpha=0.4, label="Data")
plt.plot(x, m*x + b, color="red", label="Trend Line")

plt.xlabel("Total Volume (Origin + Destination)")
plt.ylabel("Average Delay per Flight (min)")
plt.title("Avg Delay per Flight vs Total Volume")
plt.legend()
plt.grid(True)
plt.show()


# %% [markdown]
# The total volume of both origin and destination is slightly better predictor of average delay (1.8% contribution to variance based on R-squared) than the volume difference (~0.3% contribution) but both are tiny.  Next, we'll explore the relationship between flight distance and average delay.

# %%
# Initial Histogram of distances
plt.figure(figsize=(10,4))
sns.histplot(df["Distance"], bins=50)
plt.title("Distribution of Flight Distance")
plt.xlabel("Distance (miles)")
plt.show()

# %%
#Random sampling of flight distances vs delays
plt.figure(figsize=(8,5))
sns.scatterplot(
    data=df.sample(50000, random_state=42),  
    x="Distance",
    y="ArrDelay",
    alpha=0.25
)
plt.title("Flight Distance vs Arrival Delay")
plt.xlabel("Distance (miles)")
plt.ylabel("Arrival Delay (min)")
plt.grid(True)
plt.show()


# %%
corr = df["Distance"].corr(df["ArrDelay"])
corr

# %% [markdown]
# Correlation (R-squared) is near 0.  As expected, there is almost no relationship between flight delay and length, at least as a predictor.  

# %%
dep = df.copy()

# Convert the FlightDate columnn to datetime
dep["FlightDate"] = pd.to_datetime(dep["FlightDate"], errors="coerce")
dep

# %%
# Turn departure time into a datetime object for better analysis
# This require combining the time information with flight date

# Prep a series of strings to comibe with flight dates
crs_str = (
    dep["CRSDepTime"]
    .astype(str)
    .str.zfill(4)     # "0730", "1745"
)

# Combine FL_DATE + hh:mm into a true datetime
dep["CRSDepDateTime"] = pd.to_datetime(
    dep["FlightDate"].dt.strftime("%Y-%m-%d") + " " +
    crs_str.str.slice(0, 2) + ":" + crs_str.str.slice(2, 4),
    format="%Y-%m-%d %H:%M",
    errors="coerce"
)

# Drop any rows where we still failed to build a datetime
dep = dep[dep["CRSDepDateTime"].notna()].copy()

# %%
#Check to see how many rows we lost in the operation
rows_lost = len(df.index) - len(dep.index)
rows_lost

# %% [markdown]
# We'll first examine the hours of day with the highest and lowest average delay to check for a signal worth exploring.

# %%
#  Create Hourly Delay Stats

dep["dep_hour"] = dep["CRSDepDateTime"].dt.hour  # 0–23

hourly_dep_delay = (
    dep.groupby("dep_hour")["DepDelay"]
      .agg(
          n_flights="size",
          avg_dep_delay="mean",
          median_dep_delay="median",
          pct_delayed_15=lambda s: (s >= 15).mean(),
          pct_on_time_or_early=lambda s: (s <= 0).mean()
      )
      .reset_index()
      .sort_values("dep_hour")
)

hourly_dep_delay



# %%
# Hours with the lowest average departure delay
least_delay_hours = (
    hourly_dep_delay
    .sort_values("avg_dep_delay")
    .head(5)
)

# Hours with the highest average departure delay
most_delay_hours = (
    hourly_dep_delay
    .sort_values("avg_dep_delay", ascending=False)
    .head(5)
)

print("Departure hours with lowest average delay:")
display(least_delay_hours)

print("Departure hours with highest average delay:")
display(most_delay_hours)


# %%
bins = [0, 6, 10, 14, 18, 22, 24]
labels = [
    "Late Night (00–05)",
    "Morning (06–09)",
    "Late Morning (10–13)",
    "Afternoon (14–17)",
    "Evening (18–21)",
    "Late Evening (22–23)",
]

dep["dep_hour"] = dep["CRSDepDateTime"].dt.hour
dep["dep_window"] = pd.cut(dep["dep_hour"], bins=bins, labels=labels, right=False)

window_delay = (
    dep.groupby("dep_window")["DepDelay"]
      .agg(
          n_flights="size",
          avg_dep_delay="mean",
          median_dep_delay="median",
          pct_delayed_15=lambda s: (s >= 15).mean(),
          pct_on_time_or_early=lambda s: (s <= 0).mean()
      )
      .sort_values("avg_dep_delay")
)

window_delay


# %%
plt.figure(figsize=(10, 5))
sns.barplot(
    data=window_delay,
    x="dep_window",
    y="avg_dep_delay"
)
plt.xticks(rotation=30, ha="right")
plt.xlabel("Departure Time Window")
plt.ylabel("Average Departure Delay (minutes)")
plt.title("Average Departure Delay by Departure Time Window")
plt.tight_layout()
plt.show()

# %% [markdown]
# #### Conclusion
# It's clear that morning flights (6 to 9am) are the best in terms of delays, while afternoon flights are more delay prone.

# %% [markdown]
# ### Weather Effects on Delays
# We'll examine how weather causes delays.  We'll start the exploration with exploring the distribution of delay times throughout the year as well as geographically. 

# %%
dep["month"] = dep["FlightDate"].dt.month_name()
dep["month_num"] = dep["FlightDate"].dt.month 

monthly_delay_stats = (
    dep.groupby(["month_num", "month"])["ArrDelay"]
      .agg(
          n_flights="size",
          mean_delay="mean",
          median_delay="median",
          p90_delay=lambda s: s.quantile(0.90),
          total_delay="sum"
      )
      .sort_index()   
)

monthly_delay_stats


# %%
plt.figure(figsize=(12,5))
sns.barplot(
    data=monthly_delay_stats.reset_index(),
    x="month",
    y="mean_delay",
    order=monthly_delay_stats.reset_index()["month"]
)
plt.xticks(rotation=45)
plt.ylabel("Average Total Delay (mins)")
plt.title("Average Departures Delay per Flight by Month")
plt.tight_layout()
plt.show()


# %%
#Plotting Flights per month to control for effect of volume on delays
flights_per_month = (
    dep.groupby(["month_num", "month"])
      .size()
      .reset_index(name="n_flights")
      .sort_values("month_num")
)

flights_per_month


# %%
plt.figure(figsize=(12,5))
sns.barplot(
    data=flights_per_month,
    x="month",
    y="n_flights",
    order=flights_per_month["month"]
)

plt.xticks(rotation=45)
plt.xlabel("Month")
plt.ylabel("Number of Flights")
plt.title("Total Number of Flights per Month")
plt.tight_layout()
plt.show()


# %% [markdown]
# The relatively uniform distribution of flights tells us we can neglect volume as a factor in monthly delays.  This aligns to our earlier finding that total volume and volume difference contribute very little to delays.

# %%
#For averaging purposes, count the number of years each month appears in the record
month_year_count_dict = (
    dep.groupby(dep["FlightDate"].dt.month_name())["FlightDate"]
      .apply(lambda s: s.dt.year.nunique())
      .to_dict()
)
month_year_count_df = (
    pd.DataFrame.from_dict(month_year_count, orient="index", columns=["month_count"])
)
month_year_count_df

# %%
wx_delay_totals_by_month = dep.groupby("month")["WeatherDelay"].sum()
monthly_avg_wx_delay = wx_delay_totals_by_month / month_year_count_df["month_count"]
monthly_avg_wx_delay
monthly_avg_wx_delay_df = monthly_avg_wx_delay.reset_index()
monthly_avg_wx_delay_df.columns = ["month", "avg_minutes"]

# %%
plt.figure(figsize=(12,5))
sns.barplot(
    data=monthly_avg_wx_delay_df,
    x="month",
    y="avg_minutes",
    order=wx_by_month["month"]
)

plt.xticks(rotation=45)
plt.xlabel("Month")
plt.ylabel("Average Weather Delay (minutes)")
plt.title("Average Weather Delay Minutes per Month")
plt.tight_layout()
plt.show()


# %% [markdown]
# It's apparent the average weather delay per month follows a similar pattern to avereage dealy per flight per month.  Now, we'll examine the percentage of flights with any delay that also had a weather delay on a monthly basis.

# %%
#Create a binary column that indicates whether a delay of any type occurred.
#Logic is if either arrival or departure delay is positive, set to 1, otherwise 0
dep["AnyDelay"] = ((dep["DepDelay"] > 0) | (dep["ArrDelay"] > 0)).astype(int)
dep["AnyDelay"]

# %%
monthly_weather_pct = (
    dep.groupby(["month_num", "month"])
      .apply(lambda g: (
          ((g["AnyDelay"] == 1) & (g["WeatherDelay"] > 0)).sum() /
          (g["AnyDelay"] == 1).sum()
      ))
      .reset_index(name="pct_anydelay_with_weather")
      .sort_values("month_num")
)

monthly_weather_pct["pct_anydelay_with_weather"] *= 100
monthly_weather_pct


# %%
plt.figure(figsize=(12,5))
sns.barplot(
    data=monthly_weather_pct,
    x="month",
    y="pct_anydelay_with_weather",
    order=monthly_weather_pct["month"]
)

plt.xticks(rotation=45)
plt.ylabel("% of Delayed Flights with Weather Delay")
plt.title("Share of Delayed Flights Attributable to Weather (Monthly)")
plt.tight_layout()
plt.show()


# %% [markdown]
# It's clear the weather shares a similar pattern to the overall delays by month, but the low percentages indicate weather isn't generally a major contributor to overall delays. To get a sense of where weather is most likely to be an issue, let's examine the weather delays at the top 100 airports by volume.

# %%
#Create a dataframe of airports with total volume
airport_volume = (
    df.melt(
        id_vars=["FlightDate"],
        value_vars=["Origin", "Dest"],
        var_name="role",
        value_name="airport"
    )
    .groupby("airport")
    .size()
    .reset_index(name="flight_volume")
)
airport_volume

# %%
top100_airports = (
    airport_volume
    .sort_values("flight_volume", ascending=False)
    .head(100)["airport"]
    .tolist()
)


# %%
df["WeatherDelay"] = df["WeatherDelay"].fillna(0)

airport_weather = (
    df.melt(
        id_vars=["WeatherDelay"],
        value_vars=["Origin", "Dest"],
        var_name="role",
        value_name="airport"
    )
    .query("airport in @top100_airports")   # keep only top 100
    .groupby("airport")["WeatherDelay"]
    .sum()
    .reset_index(name="total_weather_delay")
    .sort_values("total_weather_delay", ascending=False)
)

# %%
#Normalize by volume

top100_volume = airport_volume[airport_volume["airport"].isin(top100_airports)]

airport_weather_rate = (
    airport_weather
    .merge(top100_volume, on="airport", how="left")
)

#minnutes per flight
airport_weather_rate["minutes_per_flight"] = (
    airport_weather_rate["total_weather_delay"] /
    airport_weather_rate["flight_volume"]
)

#sort to improve the plot
airport_weather_rate = airport_weather_rate.sort_values(
    "minutes_per_flight",
    ascending=False
)

# %%
plt.figure(figsize=(14,12))

sns.barplot(
    data=airport_weather_rate,
    y="airport",
    x="minutes_per_flight",
    palette="magma"
)

plt.title("Weather Delay Minutes per Flight for Top 100 Airports")
plt.xlabel("Weather Delay Minutes per Flight")
plt.ylabel("Airport")
plt.tight_layout()
plt.show()

# %%
airport_weather_rate.head()

# %% [markdown]
# Note the 3 of the top 5 airports for weather delay rate are small regional airports with high volumes.  This indicates that the smaller airports are less equipped to deal with weather impacts and slightly more prone to weather delays. 

# %% [markdown]
# #### Weather Delay Conclusions
# Based on our analysis, it appears weather delays are overall a minor contributor to the probability of flight delay. There are seasonal variations, but, generally, making flight decisions based on weather factors is not advised, especially if flying through major hubs. 
# 

# %% [markdown]
# ### Driving questions
#     - What percentage of delays are due to security issues?
#     - How much time is the average security delay? 
# 

# %% [markdown]
# ### Phase 1: Load and Initial Reconnaissance

# %%
df.info()

# %%
df.shape

# %%
# Initial Look at security delay
df["SecurityDelay"].describe()


# %% [markdown]
# Given the zeroes in the IQR and the very low mean, we can assume security delays are rare.  Given this, we'll focus on non-zero sercurity delays to analyze their characteristics when they do occur. 

# %%
print("Unique origin airports:", df["Origin"].nunique())
print("Unique destination airports:", df["Dest"].nunique())

# %% [markdown]
# ### Phase 2: Data Quality

# %%
#Ensure security delays are positive values
negative_security = df[df["SecurityDelay"] < 0]
print("Negative SECURITY_DELAY rows:", len(negative_security))

# %%
#Check for NaN
na_counts = df.isna().sum().sort_values(ascending=False)
na_counts

# %% [markdown]
# Key columns (FlightDate, Des, Origin,etc.) have no missing values. Missing values are expected in other columns as they are not always reported.

# %%
#Check for outliers, but only evaluate non-zero security delays
sec_pos = df.loc[df["SecurityDelay"] > 0, "SecurityDelay"]

Q1 = sec_pos.quantile(0.25)
Q3 = sec_pos.quantile(0.75)
IQR = Q3 - Q1
upper_bound = Q3 + 1.5 * IQR

print("IQR:")
print(Q1, Q3, IQR, upper_bound)
outliers = len(df[df["SecurityDelay"] > upper_bound]["SecurityDelay"])
print("Outliers",outliers)
print("Outlier Percent:",outliers/len(sec_pos)*100)


# %% [markdown]
# Outlier conlusion:  Only 8% of the sercurity delays are outside the upper bound. Outliers are not a concern for this analysis. 

# %% [markdown]
# ### Phase 3:  Cleaning Decisions & Implementation

# %%
#Turn flight date into a datetime
df["FlightDate"] = pd.to_datetime(df["FlightDate"], errors="coerce")
df["FlightDate"].head()


# %% [markdown]
# ### Phase 4:  Statistical EDA

# %%
#Frequency of Sercurity Delays
any_sec_delay = df["SecurityDelay"] > 0

avg_sec_delay_all = df["SecurityDelay"].mean()
avg_sec_delay_pos = df.loc[any_sec_delay, "SecurityDelay"].mean()

print(f"Fraction of flights with any security delay: {sec_delay_rate:.4%}")
print(f"Average security delay given SECURITY_DELAY > 0: {avg_sec_delay_pos:.2f} minutes")


# %%
plt.figure(figsize=(8, 6))
sample = df.loc[any_sec_delay, ["ArrDelay", "SecurityDelay"]].sample(
    min(5000, any_sec_delay.sum()),
    random_state=42
)

sns.scatterplot(data=sample, x="SecurityDelay", y="ArrDelay", alpha=0.3)
plt.title("Arrival Delay vs Security Delay (Sample of Flights with SECURITY_DELAY > 0)")
plt.xlabel("Security Delay (minutes)")
plt.ylabel("Arrival Delay (minutes)")
plt.show()


# %% [markdown]
# The above scatter plot reveals an expected pattern:
# - No total delays below the security delay time (total delay must be >= any contributor)
# - With increasing security delay times, the total delay is more likely to be equal to security delay.

# %% [markdown]
# Which airlines have the highest rate of security delay?

# %%
carrier_sec = df.groupby("Reporting_Airline").agg(
    flights=("FlightDate", "count"),
    sec_delay_count=("SecurityDelay", lambda x: (x > 0).sum()),
    avg_sec_delay_positive=("SecurityDelay", lambda x: x[x > 0].mean())
).assign(
    pct_flights_with_sec=lambda x: x["sec_delay_count"] / x["flights"]
).sort_values("pct_flights_with_sec", ascending=False)

carrier_sec.head(10)


# %%
plt.figure(figsize=(12, 6))
sns.barplot(
    data=carrier_sec.reset_index(),
    x="Reporting_Airline",
    y="pct_flights_with_sec"
)
plt.xticks(rotation=45)
plt.title("Security Delay Frequency by Carrier")
plt.ylabel("Pct Flights with Security Delay")
plt.show()


# %% [markdown]
# Spirit Airlines has the highhest delay, but the overall percentage values are very low (<1%).  We can conclude that security delays are not a significant factor in choosing an airline.
# 
# However, the average security delay time of 27 minutes begs the question:  Hoe does this length of time compare to other delay types? 

# %%
delay_cols = [
    "CarrierDelay",
    "WeatherDelay",
    "NASDelay",
    "SecurityDelay",
    "LateAircraftDelay"
]

df_delay = df[delay_cols]


# %%
pos_delay_stats = df_delay[df_delay > 0].describe()
pos_delay_stats


# %% [markdown]
# Overall, when security delays do happen, they are shorter on average that other delay types, with the exception of NAS delays.

# %% [markdown]
# ### Phase 5 Feature Engineering

# %% [markdown]
# N/A For this question

# %% [markdown]
# ### Phase 6: Save and Document
# Overall, security-related days were a minimal contributor to overall delays.
# 

# %% [markdown]
# # Taxi Time

# %% [markdown]
# ### Phase 1: Load and Initial Reconniassance

# %%
# Load your preprocessed parquet or pickle
df = pd.read_parquet("../data/bts_all.parquet")  # or pd.read_pickle("flights.pkl")

df.head()

# %%
df[["TaxiOut", "DepDelay"]].describe()


# %% [markdown]
# ### Phase 2: Data Quality Assessment

# %%
taxi_percent_missing = len(df["TaxiOut"]) / df["TaxiOut"].isna().sum()

taxi_percent_missing

# %% [markdown]
# Almost half of the te taxi out column is missing.  Is that due airport reporting abilities/  Let's examine the distribution of missing values across airports.

# %%
# Number of missing values per airport
missing_taxis_by_airport = (
    df.groupby("Origin")
      .agg(
          total_flights=("TaxiOut", "size"),
          missing_taxiout=("TaxiOut", lambda x: x.isna().sum())
      )
      .assign(pct_missing=lambda x: x["missing_taxiout"] / x["total_flights"]*100)
      .sort_values("pct_missing", ascending=False)
)

missing_taxis_by_airport


# %%
plt.figure(figsize=(10,6))
sns.scatterplot(
    data=missing_taxis_by_airport,
    x="total_flights",
    y="pct_missing"
)

plt.title("Missing TaxiOut % vs Total Flights by Origin Airport")
plt.show()

# %% [markdown]
# Lower volume airports have a slightly higher percentage of missing taxi times, but even the high-volume airports have percentages in 0 to 5% range.  We will just neglect missing values in this analysis.
# 
# Now, we'll validate the TaxiOut data using domain logic.

# %%
# Assume Taxi Times less than 0 and greater than 24 hours are erroneous
invalid_taxi = df[(df["TaxiOut"] < 0) | (df["TaxiOut"] > 1440)]


invalid_taxi.shape


# %%
Q1 = df["TaxiOut"].quantile(0.25)
Q3 = df["TaxiOut"].quantile(0.75)
IQR = Q3 - Q1

taxi_outliers = df[(df["TaxiOut"] < Q1 - 1.5*IQR) | (df["TaxiOut"] > Q3 + 1.5*IQR)]
outlier_pct = len(taxi_outliers)/len(df["TaxiOut"])*100
outlier_pct

# %% [markdown]
# Only 4% of the taxi times are considered outliers. 

# %% [markdown]
# ### Phase 4:  Cleaning Decisions
# N/A for this dataset

# %% [markdown]
# ### Phase 5:  Statistical EDA

# %%
#Distribution of TaxiOut and Departure delays
fig, ax = plt.subplots(1, 2, figsize=(14,5))
sns.histplot(df["TaxiOut"], bins=50, ax=ax[0])
ax[0].set_title("Distribution of TaxiOut Times")

sns.histplot(df["DepDelay"], bins=50, ax=ax[1])
ax[1].set_title("Distribution of Departure Delays")

plt.show()


# %%
plt.figure(figsize=(10,6))
sns.scatterplot(x="TaxiOut", y="DepDelay", data=df, alpha=0.3)
plt.title("TaxiOut vs. Departure Delay")
plt.show()

# %%
airport_stats = (
    df.groupby("Origin")
        .agg(avg_taxi=("TaxiOut","mean"),
             avg_dep_delay=("DepDelay","mean"),
             flights=("Origin","count"))
        .query("flights > 500")   # avoid small-sample noise
)

airport_stats.head()


# %%
plt.figure(figsize=(10,6))
sns.regplot(data=airport_stats, x="avg_taxi", y="avg_dep_delay")
plt.title("Average Airport Taxi Times and Departure Delays")
plt.show()


# %% [markdown]
# We only detect a weak linear relationship between airport average taxi time and average departure delays.

# %% [markdown]
# ### Phase 5: Transformation
# 

# %% [markdown]
# N/A for this question

# %% [markdown]
# ### Phase 6:  Save and Document

# %% [markdown]
# **Conclusion**
# 
# Average taxi times are only slightly positively related with average departure delays, indicating taxi times aren't a great contributor to departure delays.  This is probably the result of the fact that departure times already factor taxi times into the predicted departure time. 

# %% [markdown]
# # Delay Shocks

# %% [markdown]
# ### Phase 1: Load and Initial Reconniassance

# %%
#Random sample to keep the memory down... temporary measure
df = df.sample(n=100000, random_state=42)

# %%
df.info()

# %%
df_airline

# %%
# Remove the summary row
df_airline = df_airline[df_airline["OP_UNIQUE_CARRIER"] != "All Rows"]

df = df.merge(
    df_airline[["OP_UNIQUE_CARRIER", "Description"]],
    left_on="Reporting_Airline",
    right_on="OP_UNIQUE_CARRIER",
    how="left"
).rename(columns={"Description": "Airline"})
df

# %%
df["FlightDate"] = pd.to_datetime(df["FlightDate"])


# %%

df["CRSDepTime"] = df["CRSDepTime"].astype(str).str.zfill(4)


df["CRSDepDateTime"] = (
    pd.to_datetime(df["FlightDate"])
    + pd.to_timedelta(df["CRSDepTime"].str[:2].astype(int), unit="h")
    + pd.to_timedelta(df["CRSDepTime"].str[2:].astype(int), unit="m")
)

# %% [markdown]
# ### Phase 2: Data Quality Assessment

# %%
# Delay distributions
df[["DepDelay", "ArrDelay"]].describe(percentiles=[0.5, 0.9, 0.95, 0.99])


# %%
df["Tail_Number"].nunique()


# %% [markdown]
# ### Phase 3: Cleaning Decisions

# %% [markdown]
# ### Phase 4: Statistical EDA

# %%
# Overall arrival delay distribution
df["ArrDelay"].hist(bins=100, figsize=(8, 4))
plt.title("Arrival Delay Distribution (Minutes)")
plt.xlabel("Arrival delay (minutes)")
plt.ylabel("Count")
plt.show()


# %%
# Percentage of late arrivals by carrier (using 15-minute threshold)
LATE_THRESHOLD = 15
df["arr_late"] = df["ArrDelay"] > LATE_THRESHOLD

carrier_delay_rates = (
    df.groupby("Airline")["arr_late"]
      .mean()
      .sort_values(ascending=False)
)

carrier_delay_rates.plot.bar(figsize=(10, 4))
plt.title("Percent of Flights Arriving Late (>15 minutes) by Carrier")
plt.ylabel("Late arrival rate")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.show()

carrier_delay_rates


# %% [markdown]
# ### Phase 5: Transformation

# %% [markdown]
# We are interested in how each carrier resists cascading delays.  We'll need to do some feature transformation to help us with this analysis.

# %%
#Create an hour column
df["DepHour"] = df["CRSDepDateTime"].dt.hour


# %%
avg_delay_by_hour = (
    df.groupby(["Airline", "DepHour"])["DepDelay"]
      .mean()
      .reset_index()
)
avg_delay_by_hour

# %%
plt.figure(figsize=(14, 7))

sns.lineplot(
    data=avg_delay_by_hour,
    x="DepHour",
    y="DepDelay",
    hue="Airline",
    marker="o"
)

plt.title("Average Departure Delay by Hour of Day for Each Airline", fontsize=16)
plt.xlabel("Hour of Day (0–23)")
plt.ylabel("Average Departure Delay (minutes)")
plt.grid(True, alpha=0.3)
plt.xticks(range(0, 24))

plt.show()


# %% [markdown]
# It's clear in the chart above, the delays grow throughout the day for all airlines, but not at the same rate. Dispersion is smallest around 7am and grows to maximum spread at aroun 9pm. To further evaluate, we'll look at the difference in average flight delays between 7am and 9pm for each airline. **NOTE: This is  less noisy with more data**
# 
# 

# %%
subset = avg_delay_by_hour[avg_delay_by_hour["DepHour"].isin([7, 21])]

#Make 7 and 21 hours columns
pivot = subset.pivot(index="Airline", columns="DepHour", values="DepDelay")
pivot = pivot.rename(columns={7: "delay_7", 21: "delay_21"})
pivot["difference_21_minus_7"] = pivot["delay_21"] - pivot["delay_7"]
pivot

# %%
delay_diff = pivot.sort_values("difference_21_minus_7", ascending=False)
delay_diff.sort_values("difference_21_minus_7",ascending=False)


# %% [markdown]
# Digging further, we want to see how well each airline recovers, on average, from a delayed arrival flight by seeing the average delay of departure for the same aircraft. 

# %%
# Sort the rows by tail number first then scheduled departure time
df = df.sort_values(["Tail_Number", "CRSDepDateTime"])

# %%
#Previous Flight's Arrival delay
df["PrevArrDelay"] = df.groupby("Tail_Number")["ArrDelay"].shift(1)

# %%
#Boolean for whether the previous flight was late more than 15 minutes
df["PrevLate"] = df["PrevArrDelay"] > 15


# %%
#Dleay of the next flight
df["NextDepDelay"] = df["DepDelay"]


# %%
#Group recoveries by carrier
recovery_by_carrier = (
    df.groupby(["Airline", "PrevLate"])["NextDepDelay"]
      .mean()
      .unstack()
)
recovery_by_carrier.columns = [
    "avg_after_on_time",
    "avg_after_late"
]
recovery_by_carrier = recovery_by_carrier.sort_values(
    "avg_after_late", ascending=False
)
recovery_by_carrier

# %%
rc = recovery_by_carrier.copy()

x = np.arange(len(rc))
width = 0.35

fig, ax = plt.subplots(figsize=(14, 7))

ax.bar(x - width/2, rc["avg_after_on_time"], width, label="After On-Time Previous Flight")
ax.bar(x + width/2, rc["avg_after_late"], width, label="After Late Previous Flight")

ax.set_xticks(x)
ax.set_xticklabels(rc.index, rotation=45, ha="right")
ax.set_ylabel("Average Departure Delay (minutes)")
ax.set_title("Delay Recovery Analysis by Airline")
ax.grid(axis="y", alpha=0.3)
ax.legend()

plt.tight_layout()
plt.show()

# %% [markdown]
# We can conclude from this analysis that time of day and choice of carrier play a meaningful role in likelihood of delay.  Mornings flights with reputable air carriers like Southwest are your best bet.

# %% [markdown]
# # 5. Transform

# %% [markdown]
# # 6.  Save and Document


