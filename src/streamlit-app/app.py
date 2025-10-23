#!/usr/bin/env python3
import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Streamlit Demo", layout="centered")
st.title("Streamlit UI Demo")
name = st.text_input("Name", value="World")
if st.button("Greet"):
    st.success(f"Hello {name}")

st.subheader("Random Chart")
st.line_chart(pd.DataFrame(np.random.randn(30, 3), columns=list("ABC")))

with st.sidebar:
    st.info("Use the sidebar for settings")
