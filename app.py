import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import os  # For checking if file exists

# File path for our CSV
EXPENSE_FILE = "expenses.csv"

# Function to load expense file aka existing expenses
def load_expenses():
    if os.path.exists(EXPENSE_FILE):
        return pd.read_csv(EXPENSE_FILE, parse_dates=['Date'])
    return pd.DataFrame({
        'Date':[],
        'Amount':[],
        'Category':[],
        'Description':[]
    })


# Save expenses to CSV
def save_expenses(df):
    df.to_csv(EXPENSE_FILE, index=False)

# Initialize expenses in session state
if 'expenses' not in st.session_state:
    st.session_state.expenses = load_expenses()

# Initialize date value
if 'date_value' not in st.session_state:
    st.session_state.date_value = datetime.now()

st.title("Expense Tracker")
st.sidebar.header("Add New Expense")

def update_date():
    st.session_state.date_value = st.session_state.date_input

# Input fields
date = st.sidebar.date_input(
    "Date", 
    value=st.session_state.date_value, 
    key="date_input", 
    on_change=update_date
)
amount = st.sidebar.number_input(
    "Amount ($)", 
    min_value=0.01, 
    step=0.01, 
    key="amount_input"
)
category = st.sidebar.selectbox(
    "Category",
    options=["Food", "Transportation", "Entertainment", "Bills", "Shopping", "Other"],
    key="category_input"
)
description = st.sidebar.text_input(
    "Description", 
    placeholder="Enter description...", 
    key="description_input"
)

# Add expense button
if st.sidebar.button("Add Expense"):
    new_expenses = pd.DataFrame({
        'Date': [date],
        'Amount': [amount],
        'Category': [category],
        'Description': [description]
    })
    # Add to session state
    st.session_state.expenses = pd.concat([st.session_state.expenses, new_expenses],
        ignore_index=True)
    # Save to CSV
    save_expenses(st.session_state.expenses)
    st.sidebar.success("Expense added and saved!")

#  Main page analysis
if not st.session_state.expenses.empty:
    # 3 columns for metrics
    # st.columns splits the page into equal columns
    col1, col2, col3 = st.columns(3)

    with col1:
        # calculate and display total expenses
        total = st.session_state.expenses['Amount'].sum()
        st.metric("Total Expenses", f"${total:.2f}")
    
    with col2:
        # calculate and display avg expense
        average = st.session_state.expenses['Amount'].mean()
        st.metric("Average Expense", f"${average:.2f}")

    with col3:
        # total number of expenses
        count = len(st.session_state.expenses)
        st.metric("Number of Expenses", count)
    
    # Create charts
    st.subheader("Expense Analysis")

    # Pie chart, group expenses by category and sum the amounts
    category_totals = st.session_state.expenses.groupby('Category')['Amount'].sum()

    # create pie chart using plotly express
    fig1 = px.pie(
        values=category_totals.values,
        names=category_totals.index,
        title="Expenses by Category"
    )
    # Display pie chart
    st.plotly_chart(fig1)

    # show expense table with sorting
    st.subheader("Expense Details")
    # sort expenses by date, most recent first
    sorted_expenses = st.session_state.expenses.sort_values('Date', ascending=False)
    #display as interactive table
    st.dataframe(sorted_expenses, use_container_width=True)

else:
    st.info("No expenses added yet. Use the sidebar to add your first expense")
