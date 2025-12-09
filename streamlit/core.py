import pandas as pd
import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt
import seaborn as sns
import zipfile
from pathlib import Path
import random
import re


class BtsData:
    def __init__(self,sample_frac,years):
        print("Loading Data")
        self.years = years
        self.sample_frac = sample_frac
        self.df = self._read_data()
        print("Creating Airport Delay Plot")
        self.airport_delay_plot = self.create_airport_delay_plot()

        self.monthly_stats = self.create_monthly_stats()

        self.airport_delays_by_month = self.create_airport_by_month_plot()

        self.route_volume_plot = self.create_route_volume_plot()

        self.distance_delay_plot = self.create_distance_delay_plot()

        self.departure_time_window_plot = self.create_departure_time_window_plot()

        self.monthly_delay_plot = self.create_monthly_delay_plot()

        self.monthly_weather_delay_plot = self.create_monthly_weather_delay_plot()

        self.hourly_airline_delay_plot = self.create_hourly_airline_delay_plot()

        self.delay_recovery_plot = self.create_delay_recovery_plot()

    
    def _read_data(self):
        
        data_dir = Path("../data/raw/bts_on_time")
        
        # Get all zip files
        all_zip_files = sorted(data_dir.glob("*.zip"))
        
        # Filter by selected years
        zip_files = []
        for zip_path in all_zip_files:
            # Extract year from filename like "..._2020_1.zip"
            match = re.search(r'_(\d{4})_\d+\.zip$', zip_path.name)
            if match:
                year = int(match.group(1))
                if self.years is None or year in self.years:
                    zip_files.append(zip_path)
        
        print(f"Found {len(zip_files)} files for selected years: {self.years}")
        
        # Load data from selected zip files
        dfs = []
        for zip_path in zip_files:
            with zipfile.ZipFile(zip_path, 'r') as z:
                # Find the CSV file in the zip
                csv_files = [f for f in z.namelist() if f.endswith('.csv')]
                if csv_files:
                    csv_name = csv_files[0]
                    with z.open(csv_name) as f:
                        df_month = pd.read_csv(f)
                        
                        # Sample rows if requested
                        if self.sample_frac is not None and self.sample_frac < 1.0:
                            df_month = df_month.sample(frac=self.sample_frac, random_state=42)
                        
                        dfs.append(df_month)
                        print(f"Loaded {zip_path.name}: {len(df_month):,} rows")
        
        if not dfs:
            raise ValueError("No data loaded. Check year selection and file names.")
        
        # Combine all dataframes
        df = pd.concat(dfs, ignore_index=True)
        print(f"Total rows loaded: {len(df):,}")
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

    def create_distance_delay_plot(self):
        """Create scatter plot of flight distance vs arrival delay."""
        
        # Sample data for plotting (use subset to avoid overplotting)
        sample_size = min(50000, len(self.df))
        df_sample = self.df.sample(n=sample_size, random_state=42)
        
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # Scatter plot
        ax.scatter(
            df_sample["Distance"],
            df_sample["ArrDelay"],
            alpha=0.25,
            s=10
        )
        
        # Calculate correlation
        corr = self.df["Distance"].corr(self.df["ArrDelay"])
        
        ax.set_xlabel("Distance (miles)")
        ax.set_ylabel("Arrival Delay (min)")
        ax.set_title(f"Flight Distance vs Arrival Delay (Correlation: {corr:.3f})")
        ax.grid(True, alpha=0.3)
        ax.axhline(y=0, color='red', linestyle='--', alpha=0.5, linewidth=1)
        
        plt.tight_layout()
        return fig

    def create_departure_time_window_plot(self):
        """Create bar plot of average departure delay by departure time window."""
        
        # Create departure hour from CRSDepDateTime
        df_dep = self.df.copy()
        df_dep["dep_hour"] = df_dep["CRSDepDateTime"].dt.hour
        
        # Define time windows
        bins = [0, 6, 10, 14, 18, 22, 24]
        labels = [
            "Late Night (00-05)",
            "Morning (06-09)",
            "Late Morning (10-13)",
            "Afternoon (14-17)",
            "Evening (18-21)",
            "Late Evening (22-23)",
        ]
        
        df_dep["dep_window"] = pd.cut(df_dep["dep_hour"], bins=bins, labels=labels, right=False)
        
        # Calculate statistics by window
        window_delay = (
            df_dep.groupby("dep_window", observed=True)["DepDelay"]
            .agg(
                n_flights="size",
                avg_dep_delay="mean",
                median_dep_delay="median"
            )
            .reset_index()
        )
        
        # Create bar plot
        fig, ax = plt.subplots(figsize=(12, 6))
        
        sns.barplot(
            data=window_delay,
            x="dep_window",
            y="avg_dep_delay",
            palette="viridis",
            ax=ax
        )
        
        ax.set_xlabel("Departure Time Window")
        ax.set_ylabel("Average Departure Delay (minutes)")
        ax.set_title("Average Departure Delay by Departure Time Window")
        ax.tick_params(axis='x', rotation=30)
        ax.grid(True, alpha=0.3, axis='y')
        
        plt.tight_layout()
        return fig

    def create_monthly_delay_plot(self):
        """Create bar plot of average delay minutes per month."""
        
        df_monthly = self.df.copy()
        df_monthly["month_num"] = df_monthly["FlightDate"].dt.month
        df_monthly["month_name"] = df_monthly["FlightDate"].dt.month_name()
        
        # Calculate monthly delay statistics
        monthly_delay_stats = (
            df_monthly.groupby(["month_num", "month_name"])["ArrDelay"]
            .agg(
                n_flights="size",
                mean_delay="mean",
                median_delay="median"
            )
            .sort_index()
        )
        
        # Create bar plot
        fig, ax = plt.subplots(figsize=(12, 6))
        
        sns.barplot(
            data=monthly_delay_stats.reset_index(),
            x="month_name",
            y="mean_delay",
            order=monthly_delay_stats.reset_index()["month_name"]
        )
        
        ax.set_xlabel("Month")
        ax.set_ylabel("Average Delay (minutes)")
        ax.set_title("Average Arrival Delay per Month")
        ax.tick_params(axis='x', rotation=45)
        ax.grid(True, alpha=0.3, axis='y')
        
        plt.tight_layout()
        return fig

    def create_monthly_weather_delay_plot(self):
        """Create bar plot of average weather delay minutes per month."""
        
        df_weather = self.df.copy()
        df_weather["month_num"] = df_weather["FlightDate"].dt.month
        df_weather["month_name"] = df_weather["FlightDate"].dt.month_name()
        
        # Calculate monthly weather delay statistics
        monthly_weather_stats = (
            df_weather.groupby(["month_num", "month_name"])["WeatherDelay"]
            .agg(
                n_flights="size",
                mean_weather_delay="mean",
                total_weather_delay="sum"
            )
            .reset_index()
            .sort_values("month_num")
        )
        
        # Create bar plot
        fig, ax = plt.subplots(figsize=(12, 6))
        
        sns.barplot(
            data=monthly_weather_stats,
            x="month_name",
            y="mean_weather_delay",
            palette="Blues",
            ax=ax
        )
        
        ax.set_xlabel("Month")
        ax.set_ylabel("Average Weather Delay (minutes)")
        ax.set_title("Average Weather Delay per Month")
        ax.tick_params(axis='x', rotation=45)
        ax.grid(True, alpha=0.3, axis='y')
        
        plt.tight_layout()
        return fig
    
    def create_airport_weather_delay_plot(self, top_n=20):
        """
        Create bar plot of average weather delay per flight for top airports by volume.
        
        Parameters:
        -----------
        top_n : int
            Number of top airports to display (max 100)
        """
        top_n = min(top_n, 100)  # Cap at 100
        
        # Calculate airport volume
        airport_volume = (
            self.df.melt(
                id_vars=["FlightDate"],
                value_vars=["Origin", "Dest"],
                var_name="role",
                value_name="airport"
            )
            .groupby("airport")
            .size()
            .reset_index(name="flight_volume")
            .sort_values("flight_volume", ascending=False)
        )
        
        # Get top N airports
        top_airports = airport_volume.head(top_n)["airport"].tolist()
        
        # Calculate weather delay statistics for top airports
        df_weather = self.df.copy()
        df_weather["WeatherDelay"] = df_weather["WeatherDelay"].fillna(0)
        
        airport_weather = (
            df_weather.melt(
                id_vars=["WeatherDelay"],
                value_vars=["Origin", "Dest"],
                var_name="role",
                value_name="airport"
            )
            .query("airport in @top_airports")
            .groupby("airport")["WeatherDelay"]
            .agg(
                total_weather_delay="sum",
                n_flights="size"
            )
            .assign(avg_weather_delay_per_flight=lambda x: x["total_weather_delay"] / x["n_flights"])
            .reset_index()
            .sort_values("avg_weather_delay_per_flight", ascending=False)
        )
        
        # Create bar plot
        fig, ax = plt.subplots(figsize=(14, max(8, top_n * 0.3)))
        
        sns.barplot(
            data=airport_weather,
            y="airport",
            x="avg_weather_delay_per_flight",
            palette="magma",
            ax=ax
        )
        
        ax.set_xlabel("Average Weather Delay per Flight (minutes)")
        ax.set_ylabel("Airport")
        ax.set_title(f"Weather Delay Minutes per Flight - Top {top_n} Airports by Volume")
        ax.grid(True, alpha=0.3, axis='x')
        
        plt.tight_layout()
        return fig

    def create_hourly_airline_delay_plot(self):
        """Create line plot of average departure delay by hour of day for each airline."""
        
        df_hourly = self.df.copy()
        df_hourly["dep_hour"] = df_hourly["CRSDepDateTime"].dt.hour
        
        # Calculate average delay by hour and airline
        avg_delay_by_hour = (
            df_hourly.groupby(["Airline", "dep_hour"])["DepDelay"]
            .mean()
            .reset_index()
        )
        
        # Create line plot
        fig, ax = plt.subplots(figsize=(14, 7))
        
        sns.lineplot(
            data=avg_delay_by_hour,
            x="dep_hour",
            y="DepDelay",
            hue="Airline",
            marker="o",
            ax=ax
        )
        
        ax.set_xlabel("Hour of Day (0-23)")
        ax.set_ylabel("Average Departure Delay (minutes)")
        ax.set_title("Average Departure Delay by Hour of Day for Each Airline", fontsize=16)
        ax.set_xticks(range(0, 24))
        ax.grid(True, alpha=0.3)
        ax.axhline(y=0, color='red', linestyle='--', alpha=0.5, linewidth=1)
        ax.legend(title="Airline", bbox_to_anchor=(1.05, 1), loc='upper left')
        
        plt.tight_layout()
        return fig

    def create_delay_recovery_plot(self):
        """Create bar plot showing delay recovery analysis by airline."""
        
        df_recovery = self.df.copy()
        
        # Sort by tail number and scheduled departure time
        df_recovery = df_recovery.sort_values(["Tail_Number", "CRSDepDateTime"])
        
        # Get previous flight's arrival delay for the same aircraft
        df_recovery["PrevArrDelay"] = df_recovery.groupby("Tail_Number")["ArrDelay"].shift(1)
        
        # Classify previous flight as late or on-time (15 minute threshold)
        df_recovery["PrevLate"] = df_recovery["PrevArrDelay"] > 15
        
        # Current flight's departure delay
        df_recovery["NextDepDelay"] = df_recovery["DepDelay"]
        
        # Group by airline and previous flight status
        recovery_by_carrier = (
            df_recovery.groupby(["Airline", "PrevLate"])["NextDepDelay"]
            .mean()
            .unstack(fill_value=0)
        )
        
        # Rename columns for clarity
        recovery_by_carrier.columns = ["After On-Time", "After Late"]
        recovery_by_carrier = recovery_by_carrier.sort_values("After Late", ascending=False)
        
        # Create grouped bar plot
        fig, ax = plt.subplots(figsize=(14, 7))
        
        x = np.arange(len(recovery_by_carrier))
        width = 0.35
        
        ax.bar(x - width/2, recovery_by_carrier["After On-Time"], width, 
            label="After On-Time Previous Flight", color='lightblue')
        ax.bar(x + width/2, recovery_by_carrier["After Late"], width, 
            label="After Late Previous Flight (>15 min)", color='coral')
        
        ax.set_xticks(x)
        ax.set_xticklabels(recovery_by_carrier.index, rotation=45, ha="right")
        ax.set_ylabel("Average Departure Delay (minutes)")
        ax.set_title("Delay Recovery Analysis by Airline", fontsize=14)
        ax.grid(axis="y", alpha=0.3)
        ax.legend()
        ax.axhline(y=0, color='black', linestyle='-', alpha=0.3, linewidth=1)
        
        plt.tight_layout()
        return fig