import streamlit as st
import core


df = core.read_data()

if st.button("DF Head"):
    st.write(df.head())

avg_wx_delay_top_ten = core.top_ten_avg_wx_delay_major_carriers(df)

st.write(core.plot_top_ten_avg_wx_delay(avg_wx_delay_top_ten))