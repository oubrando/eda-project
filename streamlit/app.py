import streamlit as st
from core import BtsData

st.title("BTS Flight Delay Analysis")

# Year selection
available_years = list(range(2020, 2025))  
selected_years = st.multiselect(
    "Select Years", 
    options=available_years,
    default=[2020]
)

# Sample size input
use_sample = st.checkbox("Use Sample Data (sample months within selected years)", value=True)

if use_sample:
    sample_pct = st.slider("Sample Size (%)", min_value=1, max_value=100, value=10)
    sample_frac = sample_pct / 100
else:
    sample_frac = None

# Load button
if st.button("Load Data"):
    @st.cache_resource
    def load_bts_data(years, sample_frac):
        return BtsData(years=years, sample_frac=sample_frac)
    
    with st.spinner("Loading data..."):
        bts_data = load_bts_data(tuple(selected_years), sample_frac)
    
    st.session_state['bts_data'] = bts_data
    st.success("Data loaded!")

# Show plots only if data is loaded
if 'bts_data' in st.session_state:
    bts_data = st.session_state['bts_data']
    
    if st.button("Plot Airport Delays"):
        st.pyplot(bts_data.airport_delay_plot)

    if st.button("Plot Airport Delays by Month"):
        st.pyplot(bts_data.airport_delays_by_month)

    if st.button("Plot Airport Delays vs Route Volume"):
        st.pyplot(bts_data.route_volume_plot)

    if st.button("Plot Distance vs Delay"):
        st.pyplot(bts_data.distance_delay_plot)

    if st.button("Plot Departure Time Window Delays"):
        st.pyplot(bts_data.departure_time_window_plot)

    if st.button("Plot Monthly Delays"):
        st.pyplot(bts_data.monthly_delay_plot)

    if st.button("Plot Monthly Weather Delays"):
        st.pyplot(bts_data.monthly_weather_delay_plot)
    
    # Add number input for airport weather delays
    n_airports = st.number_input(
        "Number of top airports to display", 
        min_value=5, 
        max_value=100, 
        value=20,
        step=5
    )

    if st.button("Plot Airport Weather Delays"):
        fig = bts_data.create_airport_weather_delay_plot(top_n=n_airports)
        st.pyplot(fig)

    if st.button("Plot Hourly Airline Delays"):
        st.pyplot(bts_data.hourly_airline_delay_plot)

    if st.button("Plot Delay Recovery by Airline"):
        st.pyplot(bts_data.delay_recovery_plot)