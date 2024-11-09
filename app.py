import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# Setup data storage
if 'exepnses' not in st.session_state:
    st.session_state.expenses = pd.DataFrame({
    'Date':[],
    'Amount':[],
    'Category':[],
    'Description':[]

    })

# Basic page title and description
st.title("Expense Tracker")

# Sidebar for input fields
# st.sidebar creates a left side panel 
st.sidebar.header("Add New Expense")

# Add input fields to sidebar
date = st.sidebar.date_input("Date", datetime.now())
amount = st.sidebar.number_input("Amount ($)", min_value=00.01, step=0.01)
category = st.sidebar.selectbox(
    "Category",
    options=["Food", "Transportation", "Entertainment", "Bills", "Shopping", "Other"]
)
description = st.sidebar.text_input("Description", placeholder="Enter description...")

# Expense button
if st.sidebar.button("Add Expense"):
    new_expense = pd.DataFrame({
        'Date': [date],
        'Amount': [amount],
        'Category': [category],
        'Description': [description]
    })
    st.session_state.expenses = pd.concat([st.session_state.expenses, new_expense],
    ignore_index=True)
    st.sidebar.success("Expense added")

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