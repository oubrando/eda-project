import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt



def read_data():
    df_path = Path("../data/Raw/Source_Data.zip")
    return pd.read_csv(df_path, compression="zip", parse_dates=["FL_DATE"], low_memory=False)

def top_ten_avg_wx_delay_major_carriers(df):

    # Work on a copy
    df = df.copy()

    # Filter to only the major carriers
    allowed_carriers = ["AA", "DL", "UA", "WN", "F9"]
    df = df[df["OP_CARRIER"].isin(allowed_carriers)]

    # Replace missing weather delay with zero
    df["WEATHER_DELAY"] = df["WEATHER_DELAY"].fillna(0)

    summary = (
        df.groupby("DEST_CITY_NAME")
          .agg(
              total_flights=("FLIGHTS", "sum"),
              total_weather_delay=("WEATHER_DELAY", "sum"),
          )
          .assign(
              avg_weather_delay_per_flight=lambda x: 
                  x["total_weather_delay"] / x["total_flights"]
          )
          .sort_values("avg_weather_delay_per_flight", ascending=False)
          .head(10)
    )

    return summary


def plot_top_ten_avg_wx_delay(df):
    """Create a bar chart figure for the top 10 by avg weather delay per flight."""


    fig, ax = plt.subplots(figsize=(10, 5))

    ax.bar(df.index, df["avg_weather_delay_per_flight"])
    ax.set_title(f"Top 10 Destination City by Average Weather Delay per Flight")
    ax.set_xlabel("Destination City")
    ax.set_ylabel("Avg Weather Delay per Flight (minutes)")
    ax.tick_params(axis="x", rotation=90)

    fig.tight_layout()
    return fig
