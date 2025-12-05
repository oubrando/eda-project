#!/usr/bin/env python
# coding: utf-8

# # Introduction
# ## Help

# # Initial Questions
# 1. What do we want to know about airline on-time performance?
# 2. How will the answer be useful in decision making?
# 
# # Data Specific Questions
# **1. How does on-time performance vary across carrier, airports, time, day, maybe aircraft?**
#    
#     -  What's the overall distribution of any flight delays? 
#     -  What airline has the best and worst on-time performance? 
#     -  How do routes (short/long) correlate with performance? 
#     -  What departure time windows have the least amount of delays? Most amount of delays? 
#     -  What is the average delay per airport? per airline? per airport & airline? 
#     - What percentage of flights leave on-time? Delayed? 
#     -  What time ranges have the highest/lowest delays? 
#     -How many flights per day? 
#         - By airport? By carrier? 
#     -What is the average aircraft turnaround time by carrier? (I'd think we'd have to subtract any weather, security, or NAS delays because those are not impacted their ability to get the aircraft ready for the next flight) 
#     
# 
# **2. What delay propagation patterns can we draw?**
# 
#     - Is there recovery or do they compound / propagate? 
#             - Are some airlines better at recovering than others? 
#         - What information can we draw from taxi times? Thinking about traffic jams at the runways due to built up delays
#     - What percent of flights are delayed 15, 30, 60+ minutes? 
#     - What is the % chance that a late arrival will cause the next flight to also be late 
#     - What is the average total time per day in delays a carrier has? 
#     - What correlations are there between delays and cancelations (mainly downstream, think about how a major storm could cause mass cancellations in a short period of time)? 
# 
# **3. What factors have the greatest effect on on-time performance**
#    
#     - Weather 
#         - What is the average number of delays per day due to weather?
#         - What percentage of days are due to weather?
#         - Which airports have the highest/most frequent weather delays?
#         - How much time is the average weather delay?
#     - Secuirty 
#         - What percentage of delays are due to security issues?
#         - How much time is the average security delay? 
#     - Carrier 
#         - Which carriers have the highest delays?
#         - How much time is the average carrier delay
#     - National Aviation System (Delay within control of ATC, not airline) 
#         - Which airports have the most/highest delays due to NAS?
#         - How much time is the average NAS delau
#         - What is the total number 
# 
# 4. What is the overall cost of delays?
#     -Fuel, labor, etc. 
# 
# 6. What is the impact to customers?
#     - Which airports should customers expect delays
#     - What percent of flights are delayed 15, 30, 60+ minutes?
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
#     -  What is the average delay per airport? per airline? per airport & airline? 
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
# ## Amibtion
# - What is the cost to airlines due to delays? Per day? Per Year?
# - 
# 
# 
#         
# # Source Data
# United States Department of Transportation - U.S. Buerau of Transportation Statistics
# 
# # Features Needed
# ### 1. Date
# 
# ### 2. Time of Day
# 
# ### 3. Carrier
# - American
# - United
# - Delta
# - Southwest
# - Alaska
# - JetBlue
# - Spirit
# - Frontier
# 
# ### 5. Airport (Departure)
# - Dallas Fort-Worth (DFW) **1**
# - Atlanta (ATL)           **2**
# - Los Angeles (LAX)       **3**
# - New York                **6**
#   - JFK
# - Miami (MIA)             **8**
# - Chicago O'Hare (OHD)    **4**
# - Phoenix (PHX)           **7**
# - Denver (DEN)            **5**
# - San Franscisco (SFO)
# - Washington D.C.
#   - Dulles (IAD)
# 
# **I was thinking we could just narrow it down to 5-10 airports but since we have the airport IDs in the data, I don't entirely see the benefit of just picking 10 other than maybe lessening the complexity or size of the data. Maybe we could just do some groupings by U.S. region? Open to suggestions**
# 
# 
# ### 7. Airport (Arrival) / Destination
# 
# ### 8. Reason For Delay
# - Weather
# - Carrier
# - Security
# - Late Aircraft
# - National Aviation System (NAS)
# 
# **we can leave these split up into their own feature**
# 
# ### 9. Tail Number
# 
# ### 10. Elapsed Time
# 
# ### 11. State
# 
# ### 12. Wheels Up
# 
# ### 13. Wheel Down
# 
# ### 14. Taxi Time (We could create a column that sums up taxi out and taxi in. However, taxi out could be an important variable for assessing NAS delays)
# 
# 
# 

# # 1. Initial Load & Reconniassance 
# ## Questions to Answer
# 1. Tidy or not?
# 2. Entities, Attributes, Observations?
# 3. Variable Types?
# 4. Shape & scale?
# 5. Any obvious problems?
# 
# **I will add a table of feature names and a brief description for each so it's easy to follow the table**
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
# - 
# 

# #### Preprocessing Note
# Data are in individual CSV files within compressed directories separated by year and month.  Run `python ~/data/bts_preprocess.py` to generate the pickle file used in this notebook

# In[1]:


import pandas as pd
import numpy as np
from pathlib import Path
import zipfile
import seaborn as sns
import matplotlib.pyplot as plt
import statsmodels.api as sm


# In[90]:


df = pd.read_parquet("../data/bts_all.parquet")


# In[91]:


df.tail()


# In[5]:


df_aircraft = pd.read_csv("../data/Raw/Aircraft.csv")
df_aircraft


# In[6]:


#Changing feature names for aircraft DF
mod_aircraft = df_aircraft.rename(columns= {
    'N-NUMBER': 'Tail_Number',
    'MFR': 'Manufacturer',
    'NO-SEATS': 'Number_of_Seats'
})
mod_aircraft

df_merged = df.merge(mod_aircraft, on='Tail_Number', how='left')
df_merged


# In[100]:


df_merged.dtypes


# ### How do routes correlate with delays?
# We're looking to assess how delays vary by route. In this context, we'll define a route as a departure/arrival airport pair.  We are interested in identifying the routes with the highest average delay per flight. 

# In[15]:


#create a route column from origin and destination columns
df["route"] = df["Origin"] + "_" + df["Dest"]

#build a dataframe of flight delay information for each route
route_delay = (
    df.groupby("route")
      .agg(total_arr_delay=("ArrDelay", "sum"),
           n_flights=("ArrDelay", "count"))
      .sort_values("n_flights", ascending=False)
)


# In[16]:


route_delay['avg_delay_per_flight'] = route_delay['total_arr_delay'] / route_delay['n_flights']
route_delay.head()


# #### Establish a minimum number of flights
# To avoid the results being skewed by routes with very few flights, we'll establish a minimum threshold of number of flights in order for a route to be considered in the analysis. To do this, we'll start with a cutoff that includes 80% of all flights and adjust as necessary.

# In[17]:


# Compute the cumulative percentage of total flights as routes are sorted by descending flight count
route_delay["cumulative_share"] = route_delay["n_flights"].cumsum() / route_delay["n_flights"].sum()
route_delay


# In[18]:


#Establish 80% cutoff mark
cutoff_row = route_delay[route_delay["cumulative_share"] >= 0.80].iloc[0]
cutoff_value = cutoff_row["n_flights"]
cutoff_value


# In[19]:


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


# In[20]:


sns.histplot(route_delay["n_flights"], bins=100)
plt.title("Distribution of Route Flight Counts")
plt.xlabel("Number of Flights")
plt.ylabel("Number of Routes")
plt.show()


# Given the above histogram and bar char, there is a long tail of lower-volume routes that might be of interest.  Let's up the threshold to 95% of flights.

# In[21]:


#Establish 95% cutoff mark
cutoff_row = route_delay[route_delay["cumulative_share"] >= 0.95].iloc[0]
cutoff_value = cutoff_row["n_flights"]
cutoff_value


# A minimum threshold of 1623 flights for a route covers 95% of all flights. Now, we'll find the average delay time per flight for all routes with 1623 flights or more.

# In[36]:


min_flights = 1623


filtered_routes = route_delay[route_delay["n_flights"] >= min_flights]

# Sort by highest avg delay per flight
filtered_routes = filtered_routes.sort_values(
    "avg_delay_per_flight",
    ascending=False
)
filtered_routes.drop(columns=["cumulative_share"], inplace=True) # cumulative share doesn't make sense in this context



# In[37]:


worst_routes = filtered_routes.head()
worst_routes


# In[38]:


best_routes = filtered_routes.tail()
best_routes


# Based on this analysis, there is no standout commonality among the best and worst routes for delays or early arrivals.  Let's explore volume per day at the airports in the top 5 and bottom 5 in the delay data to see if there is a signal there.

# In[39]:


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


# In[40]:


# Average volume / day at the airports in the worst routes
worst_filtered = (
    airport_daily_volume[airport_daily_volume["airport"].isin(top_worst_airports)]
)
worst_filtered_avg = worst_filtered.groupby("airport")["flights_per_day"].mean()


# In[41]:


# Average volume / day at the airports in the best routes
best_filtered = (
    airport_daily_volume[airport_daily_volume["airport"].isin(top_best_airports)]
)
best_filtered_avg = best_filtered.groupby("airport")["flights_per_day"].mean()


# In[42]:


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






# In[43]:


best_route_volumes_df = create_route_volume_df(best_routes,best_filtered_avg)
best_route_volumes_df


# In[44]:


worst_route_volumes_df = create_route_volume_df(worst_routes,worst_filtered_avg)
worst_route_volumes_df


# In[45]:


#Best vs Worst Average Total Volumes
print("Best Route Total Volume:",best_route_volumes_df['total_volume'].mean())
print("Worst Route Total Volume:",worst_route_volumes_df['total_volume'].mean())


# In[46]:


#Best vs Worst Average Volume Difference
print("Best Route Volume Diff:",best_route_volumes_df['volume_diff'].mean())
print("Worst Route Volume Diff:",worst_route_volumes_df['volume_diff'].mean())


# There is signal in both the difference and totals in volumes between an origin and destination for more exploration. Next, we'll do a regression of these two variables on the entire set.

# In[75]:


avg_daily_volume = airport_daily_volume.groupby("airport")["flights_per_day"].mean()
route_volume_df = create_route_volume_df(route_delay,avg_daily_volume)


# In[76]:


merged_route_volumes = route_volume_df.merge(route_delay,on="route")


# In[77]:


merged_route_volumes = merged_route_volumes[merged_route_volumes["n_flights"] >= min_flights]
merged_route_volumes.head()


# In[78]:


#Single Variate Regression for volume difference
X = merged_route_volumes[["volume_diff"]] #predictor
y = merged_route_volumes["avg_delay_per_flight"] #predictand

X = sm.add_constant(X) #Intercept

# Fit model
model = sm.OLS(y, X).fit()

print(model.summary())


# In[74]:


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


# In[84]:


#Single Variate Regression for total volume
X = merged_route_volumes[["total_volume"]] #predictor
y = merged_route_volumes["avg_delay_per_flight"] #predictand

X = sm.add_constant(X) #Intercept

# Fit model
model = sm.OLS(y, X).fit()

print(model.summary())


# In[85]:


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


# The total volume of both origin and destination is slightly better predictor of average delay (1.8% contribution to variance based on R-squared) than the volume difference (~0.3% contribution) but both are tiny.  Next, we'll explore the relationship between flight distance and average delay.

# ### How do flight lengths correlate with delays?

# In[92]:


# Initial Histogram of distances
plt.figure(figsize=(10,4))
sns.histplot(df["Distance"], bins=50)
plt.title("Distribution of Flight Distance")
plt.xlabel("Distance (miles)")
plt.show()


# In[95]:


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


# Based on the scatter plot, there isn't a linear relationship, but let's check correlation.

# In[97]:


corr = df["Distance"].corr(df["ArrDelay"])
corr


# Correlation (R-squared) is near 0.  As expected, there is almost no relationship between flight delay and length, at least as a predictor.  

# In[117]:


dep = df.copy()

# Convert the FlightDate columnn to datetime
dep["FlightDate"] = pd.to_datetime(dep["FlightDate"], errors="coerce")
dep


# In[121]:


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


# In[127]:


#Check to see how many rows we lost in the operation
rows_lost = len(df.index) - len(dep.index)
rows_lost


# We'll first examine the hours of day with the highest and lowest average delay to check for a signal worth exploring.

# In[129]:


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



# In[132]:


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

print("Departure hours with hgihest average delay:")
display(most_delay_hours)


# In[133]:


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


# In[135]:


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


# #### Conclusion
# It's clear that morning flights (6 to 9am) are the best in terms of delays, while afternoon flights are more delay prone.

# ### Weather Effects on Delays
# We'll examine how weather causes delays.  We'll start the exploration with exploring the distribution of delay times throughout the year as well as geographically. 
