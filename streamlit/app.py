import streamlit as st
from core import BtsData

@st.cache_resource
def load_bts_data():
    return BtsData()

bts_data = load_bts_data()

if st.button("Plot Airport Delays"):
    st.write(bts_data.airport_delay_plot)

if st.button("Plot Airport Delays by Month"):
    st.write(bts_data.airport_delays_by_month)

if st.button("Plot Airport Delays vs Route Volume"):
    st.write(bts_data.route_volume_plot)

