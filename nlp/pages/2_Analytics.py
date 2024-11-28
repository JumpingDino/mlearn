import sys
sys.path.append('../')

import numpy as np
import pandas as pd

import streamlit as st
st.set_page_config(
    page_title="AufDeutsch - Analytics",
    page_icon="📓",
)

#@st.cache_data(ttl=3600)
def load_data(path='data/cards.csv'):
    return pd.read_csv(path)

df = load_data(path='data/cards.csv')
n_rows = len(df)
st.dataframe(df, height=n_rows*36, hide_index=True)
