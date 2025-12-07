import pandas as pd
import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt
import seaborn as sns


class BtsData:
    def __init__(self):
        print("Loading Data")
        self.df = self._read_data()
        print("Creating Airport Delay Plot")
        self.airport_delay_plot = self.create_airport_delay_plot()

        self.monthly_stats = self.create_monthly_stats()

        self.airport_delays_by_month = self.create_airport_by_month_plot()

        self.route_volume_plot = self.create_route_volume_plot()

    
    def _read_data(self):
        df = pd.read_parquet("../data/bts_all.parquet") #initital load of parquet file containing main DF data from Beaurue of Transportation Stats
        df_aircraft = pd.read_csv("../data/Aircraft.csv") #csv file of aircraft tail numbers and their makes and models
        df_airports = pd.read_csv("../data/Airports.csv") #csv file of airport codes and their country
        df_airline = pd.read_csv("../data/Airline.csv") #csv file of airline codes and they're full names

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

        # Tail Number: Remove leading "N" and merge aircraft data
        df['Tail_Number'] = df['Tail_Number'].str.lstrip('N')
        df = df.merge(
            df_aircraft.drop(columns='MFR MDL CODE').rename(columns={
                'N-NUMBER': 'Tail_Number',
                'MFR': 'Manufacturer',
                'NO-SEATS': 'Number_of_Seats'
            }),
            on='Tail_Number',
            how='left'
        )

        # Airport: Merge and determine flight type in one pass
        df = (df
            .merge(df_airports.rename(columns={'lid': 'DepAirport_code', 'country': 'dep_country'})[['DepAirport_code', 'dep_country']], 
                left_on='Origin', right_on='DepAirport_code', how='left')
            .merge(df_airports.rename(columns={'lid': 'DestAirport_code', 'country': 'dest_country'})[['DestAirport_code', 'dest_country']], 
                left_on='Dest', right_on='DestAirport_code', how='left')
        )

        df['flight_type'] = np.where((df['dep_country'] != 'US') | (df['dest_country'] != 'US'), 'International', 'Domestic')
        df = df.drop(columns=['DepAirport_code', 'dep_country', 'DestAirport_code', 'dest_country'])

        # Airline: Merge and clean names
        df = (df
            .merge(df_airline.rename(columns={'OP_UNIQUE_CARRIER': 'Reporting_Airline'}), 
                on='Reporting_Airline', how='left')
            .rename(columns={'Description': 'Airline'})
            .drop(columns=['Reporting_Airline'])
        )

        df['Airline'] = df['Airline'].str.replace(r' Inc\.$| Co\.$', '', regex=True)
        df = df.dropna(subset=['Airline'])

        return df

    def create_airport_delay_plot(self):
        #Airports with worst departure and arrival delays
        airports_origin = self.df['Origin'].unique().tolist()
        airports_dest = self.df['Dest'].unique().tolist()
        worst_dep = self.df.groupby('Origin')['DepDelay'].sum().sort_values(ascending=False).reset_index()
        worst_arr = self.df.groupby('Dest')['ArrDelay'].sum().sort_values(ascending=False).reset_index()

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
        
        return fig

    def create_monthly_stats(self):
        self.df['Year'] = self.df['FlightDate'].dt.year #extracting year
        self.df['Month'] = self.df['FlightDate'].dt.month #extracting month

        #Departures
        self.worst_dep_yr = self.df.groupby(['Year', 'Origin']).agg( #groupby year and origin airport to aggegrate sum, mean and median of depdelays per year and sort them in ascending order by total delays
            total_dep_delays=('DepDelay', 'sum'),
            avg_dep_delay=('DepDelay', 'mean'),
            median_dep_delay=('DepDelay', 'median')
        ).sort_values(['Year', 'total_dep_delays'], ascending=[True,False]).groupby('Year').head(5)

        self.worst_dep_mo = self.df.groupby(['Month', 'Origin']).agg( #groupby month and origin airport to aggegrate sum, mean and median of depdelays per month and sort them in ascending order by total delays
            total_dep_delays=('DepDelay', 'sum'),
            avg_dep_delay=('DepDelay', 'mean'),
            median_dep_delay=('DepDelay', 'median')
        ).sort_values(['Month', 'total_dep_delays'], ascending=[True,False]).groupby('Month').head(5)

        #Arrivals
        self.worst_dest_yr = self.df.groupby(['Year', 'Dest']).agg( #groupby year and origin airport to aggegrate sum, mean and median of depdelays per year and sort them in ascending order by total delays
            total_arr_delays=('ArrDelay', 'sum'),
            avg_arr_delay=('ArrDelay', 'mean'),
            median_arr_delay=('ArrDelay', 'median')
        ).sort_values(['Year', 'total_arr_delays'], ascending=[True,False]).groupby('Year').head(5)

        self.worst_dest_mo = self.df.groupby(['Month', 'Dest']).agg( #groupby month and origin airport to aggegrate sum, mean and median of depdelays per month and sort them in ascending order by total delays
            total_arr_delays=('ArrDelay', 'sum'),
            avg_arr_delay=('ArrDelay', 'mean'),
            median_arr_delay=('ArrDelay', 'median')
        ).sort_values(['Month', 'total_arr_delays'], ascending=[True,False]).groupby('Month').head(5)

    def create_airport_by_month_plot(self):
        # Reset index once
        plot_mo = self.worst_dep_mo.reset_index()
        months = plot_mo['Month'].unique()  # No need to sort if order doesn't matter critically

        # Calculate grid dimensions dynamically
        num_months = len(months)
        cols = 3
        rows = (num_months + cols - 1) // cols  # Ceiling division

        # Create figure
        fig, axes = plt.subplots(rows, cols, figsize=(20, 16), squeeze=False)
        axes_flat = axes.flatten()

        # Pre-filter data once using groupby
        month_groups = {mo: group for mo, group in plot_mo.groupby('Month')}

        # Plot each month
        for i, mo in enumerate(months):
            ax = axes_flat[i]
            data = month_groups[mo]
            
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

        # Turn off unused subplots
        for j in range(num_months, len(axes_flat)):
            axes_flat[j].axis('off')

        plt.tight_layout()
        return fig  

    def create_route_volume_plot(self):
        """Create scatter plot of average delay per flight vs total route volume."""
        
        # Create route column
        df_routes = self.df.copy()
        df_routes["route"] = df_routes["Origin"] + "_" + df_routes["Dest"]
        
        # Calculate route delay statistics
        route_delay = (
            df_routes.groupby("route")
            .agg(
                total_arr_delay=("ArrDelay", "sum"),
                n_flights=("ArrDelay", "count")
            )
            .assign(avg_delay_per_flight=lambda x: x['total_arr_delay'] / x['n_flights'])
        )
        
        # Calculate daily volume per airport
        airport_daily_volume = (
            df_routes.melt(
                id_vars=["FlightDate"],
                value_vars=["Origin", "Dest"],
                var_name="type",
                value_name="airport"
            )
            .groupby(["airport", "FlightDate"])
            .size()
            .reset_index(name="flights_per_day")
        )
        
        avg_daily_volume = airport_daily_volume.groupby("airport")["flights_per_day"].mean()
        
        # Calculate total volume for each route
        route_volumes = []
        for route in route_delay.index:
            origin, dest = route.split("_")
            total_volume = avg_daily_volume.get(origin, 0) + avg_daily_volume.get(dest, 0)
            route_volumes.append({
                "route": route,
                "total_volume": total_volume
            })
        
        route_volumes_df = pd.DataFrame(route_volumes).set_index("route")
        
        # Merge with delay data
        merged_data = route_volumes_df.merge(route_delay, left_index=True, right_index=True)
        
        # Filter to routes with minimum flights (95th percentile cutoff)
        min_flights = int(route_delay["n_flights"].quantile(0.05))
        filtered_data = merged_data[merged_data["n_flights"] >= min_flights]
        
        # Create scatter plot
        fig, ax = plt.subplots(figsize=(10, 6))
        
        x = filtered_data["total_volume"]
        y = filtered_data["avg_delay_per_flight"]
        
        # Fit linear trend
        m, b = np.polyfit(x, y, 1)
        
        ax.scatter(x, y, alpha=0.4, label="Routes")
        ax.plot(x, m*x + b, color="red", linewidth=2, label="Trend Line")
        
        ax.set_xlabel("Total Volume (Origin + Destination)")
        ax.set_ylabel("Average Delay per Flight (min)")
        ax.set_title("Average Delay per Flight vs Total Route Volume")
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        return fig