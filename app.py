import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# Setup data storage
if 'exepnses' not in st.session_state:
    st.session_state.exepnses = pd.DataFrame({
    'Date':[],
    'Amount':[],
    'Category':[],
    'Description':[]

    })

# Basic page title and description
st.title("Expense Tracker")
st.write("Welcome! Let's track your expenses.")

# Create a simple test button
if st.button("test Button"):
    st.write("Button works! We're ready to move forward.")
