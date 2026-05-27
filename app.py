import streamlit as st
import requests
import pandas as pd

# Backend URL from Streamlit Secrets
server_url = st.secrets["server_url"]

st.title("Expense Tracker Application")

option = st.sidebar.selectbox(
    "Choose Any One",
    [
        "Add Expense",
        "View Expenses",
        "Update Expense",
        "Delete Expense",
        "Search Expense",
        "Analyze Spending"
    ]
)

# Add Expense
if option == "Add Expense":

    st.subheader("Add Expense")

    title = st.text_input("Enter Title")
    amount = st.number_input("Enter Amount")
    category = st.text_input("Enter Category")

    if st.button("Add"):

        payload = {
            "title": title,
            "amount": amount,
            "category": category
        }

        res = requests.post(
            f"{server_url}/add_expense",
            json=payload
        )

        st.success(res.json()["message"])

# View Expenses
elif option == "View Expenses":

    st.subheader("View Expenses")

    res = requests.get(f"{server_url}/view_expenses")

    data = res.json()

    if data:
        df = pd.DataFrame(data)
        st.dataframe(df)

# Update Expense
elif option == "Update Expense":

    st.subheader("Update Expense")

    expense_id = st.number_input("Enter Expense ID", step=1)

    title = st.text_input("New Title")
    amount = st.number_input("New Amount")
    category = st.text_input("New Category")

    if st.button("Update"):

        payload = {
            "title": title,
            "amount": amount,
            "category": category
        }

        res = requests.put(
            f"{server_url}/update_expense/{expense_id}",
            json=payload
        )

        st.success(res.json()["message"])

# Delete Expense
elif option == "Delete Expense":

    st.subheader("Delete Expense")

    expense_id = st.number_input("Enter Expense ID", step=1)

    if st.button("Delete"):

        res = requests.delete(
            f"{server_url}/delete_expense/{expense_id}"
        )

        st.success(res.json()["message"])

# Search Expense
elif option == "Search Expense":

    st.subheader("Search Expense")

    keyword = st.text_input("Enter Keyword")

    if st.button("Search"):

        res = requests.get(
            f"{server_url}/search_expense/{keyword}"
        )

        data = res.json()

        if data:
            df = pd.DataFrame(data)
            st.dataframe(df)
        else:
            st.warning("No Data Found")

# Analyze Spending
elif option == "Analyze Spending":

    st.subheader("Analyze Spending")

    res = requests.get(f"{server_url}/analyze_spending")

    data = res.json()

    st.success(
        f"Total Spending: {data['total_spending']['total']}"
    )

    df = pd.DataFrame(data["category_spending"])

    st.dataframe(df)