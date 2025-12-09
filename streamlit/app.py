import streamlit as st
from core import BtsData

st.set_page_config(page_title="BTS Flight Delay Analysis", layout="wide")
st.title("BTS Flight Delay Analysis")

# ---------------------------
# Data selection controls
# ---------------------------
available_years = list(range(2020, 2025))
selected_years = st.multiselect(
    "Select Years",
    options=available_years,
    default=[2020],
    help="Choose which years of BTS On-Time data to include."
)

use_sample = st.checkbox(
    "Use Sample Data (sample months within selected years)",
    value=True
)

if use_sample:
    sample_pct = st.slider(
        "Sample Size (%)",
        min_value=1,
        max_value=100,
        value=10
    )
    sample_frac = sample_pct / 100
else:
    sample_frac = None

@st.cache_resource
def load_bts_data(years, sample_frac):
    return BtsData(years=years, sample_frac=sample_frac)

# ---------------------------
# Load data
# ---------------------------
if st.button("Load Data"):
    with st.spinner("Loading data..."):
        bts_data = load_bts_data(tuple(selected_years), sample_frac)
    st.session_state["bts_data"] = bts_data
    st.success("Data loaded!")

# ---------------------------
# Plots (only if data loaded)
# ---------------------------
if "bts_data" in st.session_state:
    bts_data = st.session_state["bts_data"]

    # Create tabs for sections
    tab_general, tab_weather, tab_routes, tab_recovery = st.tabs(
        ["General", "Weather", "Routes", "Delay Recovery"]
    )

    # -----------------------
    # GENERAL
    # -----------------------
    with tab_general:
        st.header("General Delay Patterns")

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Airport Delays (Overall)")
            if st.button("Plot Airport Delays", key="btn_airport_delays"):
                st.pyplot(bts_data.airport_delay_plot)

        with col2:
            st.subheader("Airport Delays by Month")
            if st.button("Plot Airport Delays by Month", key="btn_airport_delays_by_month"):
                st.pyplot(bts_data.airport_delays_by_month)

        st.markdown("---")

        col3, col4 = st.columns(2)

        with col3:
            st.subheader("Departure Time Window Delays")
            if st.button("Plot Departure Time Window Delays", key="btn_dep_window"):
                st.pyplot(bts_data.departure_time_window_plot)

        with col4:
            st.subheader("Monthly Arrival Delays")
            if st.button("Plot Monthly Delays", key="btn_monthly_delays"):
                st.pyplot(bts_data.monthly_delay_plot)

        st.markdown("---")



    # -----------------------
    # WEATHER
    # -----------------------
    with tab_weather:
        st.header("Weather-Related Delays")

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Average Weather Delay by Month")
            if st.button("Plot Monthly Weather Delays", key="btn_monthly_weather"):
                st.pyplot(bts_data.monthly_weather_delay_plot)

        with col2:
            st.subheader("Weather Delay per Flight by Airport")

            n_airports = st.number_input(
                "Number of top airports to display",
                min_value=5,
                max_value=100,
                value=20,
                step=5,
                key="num_airports_weather"
            )

            if st.button("Plot Airport Weather Delays", key="btn_airport_weather"):
                fig = bts_data.create_airport_weather_delay_plot(top_n=n_airports)
                st.pyplot(fig)

    # -----------------------
    # ROUTES
    # -----------------------
    with tab_routes:
        st.header("Routes and Distance Effects")

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Route Volume vs Delay")
            if st.button("Plot Airport Delays vs Route Volume", key="btn_route_volume"):
                st.pyplot(bts_data.route_volume_plot)

        with col2:
            st.subheader("Distance vs Arrival Delay")
            if st.button("Plot Distance vs Delay", key="btn_distance_delay"):
                st.pyplot(bts_data.distance_delay_plot)

    # -----------------------
    # DELAY RECOVERY
    # -----------------------
    with tab_recovery:
        st.header("Delay Recovery Analysis")

        st.write(
            "This view examines how well airlines recover from late arrivals by "
            "comparing the next departure delay after on-time vs. late previous flights."
        )

        if st.button("Plot Delay Recovery by Airline", key="btn_delay_recovery"):
            st.pyplot(bts_data.delay_recovery_plot)

        st.subheader("Hourly Airline Delays")
        if st.button("Plot Hourly Airline Delays", key="btn_hourly_airline"):
            st.pyplot(bts_data.hourly_airline_delay_plot)

else:
    st.info("Select years, choose sampling options, and click **Load Data** to begin.")
