import streamlit as st
import requests
import pandas as pd
import plotly.express as px

# Backend URL from Streamlit Secrets
server_url = st.secrets["server_url"]

st.set_page_config(
    page_title="Expense Tracker",
    page_icon="💰",
    layout="wide"
)

st.title("💰 Expense Tracker Application")

# Sidebar Menu
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

# =========================
# ADD EXPENSE
# =========================

if option == "Add Expense":

    st.subheader("➕ Add Expense")

    title = st.text_input("Enter Title")

    amount = st.number_input(
        "Enter Amount",
        min_value=0.0,
        format="%.2f"
    )

    category = st.selectbox(
        "Choose the category",
        [
            "Food 🍛",
            "Travel 🚌",
            "Bills 📱",
            "Entertainment 🎬",
            "Health 💊",
            "Shopping 👕",
            "Others"
        ]
    )

    if st.button("Add Expense"):

        payload = {
            "title": title,
            "amount": amount,
            "category": category
        }

        try:

            res = requests.post(
                f"{server_url}/add_expense",
                json=payload
            )

            if res.status_code == 200:
                st.success(res.json()["message"])
            else:
                st.error("Failed to Add Expense")

        except Exception as e:
            st.error(f"Error: {e}")

# =========================
# VIEW EXPENSES
# =========================

elif option == "View Expenses":

    st.subheader("📋 View Expenses")

    try:

        res = requests.get(f"{server_url}/view_expenses")

        if res.status_code == 200:

            data = res.json()

            if data:

                df = pd.DataFrame(data)

                st.dataframe(
                    df,
                    use_container_width=True
                )

            else:
                st.warning("No Expenses Found")

        else:
            st.error("Unable to Fetch Data")

    except Exception as e:
        st.error(f"Error: {e}")

# =========================
# UPDATE EXPENSE
# =========================

elif option == "Update Expense":

    st.subheader("✏️ Update Expense")

    expense_id = st.number_input(
        "Enter Expense ID",
        min_value=1,
        step=1
    )

    title = st.text_input("New Title")

    amount = st.number_input(
        "New Amount",
        min_value=0.0,
        format="%.2f"
    )

    category = st.selectbox(
        "Choose New Category",
        [
            "Food 🍛",
            "Travel 🚌",
            "Bills 📱",
            "Entertainment 🎬",
            "Health 💊",
            "Shopping 👕",
            "Others"
        ]
    )

    if st.button("Update Expense"):

        payload = {
            "title": title,
            "amount": amount,
            "category": category
        }

        try:

            res = requests.put(
                f"{server_url}/update_expense/{expense_id}",
                json=payload
            )

            if res.status_code == 200:
                st.success(res.json()["message"])
            else:
                st.error("Expense Not Updated")

        except Exception as e:
            st.error(f"Error: {e}")

# =========================
# DELETE EXPENSE
# =========================

elif option == "Delete Expense":

    st.subheader("🗑️ Delete Expense")

    expense_id = st.number_input(
        "Enter Expense ID",
        min_value=1,
        step=1
    )

    if st.button("Delete Expense"):

        try:

            res = requests.delete(
                f"{server_url}/delete_expense/{expense_id}"
            )

            if res.status_code == 200:
                st.success(res.json()["message"])
            else:
                st.error("Expense Not Deleted")

        except Exception as e:
            st.error(f"Error: {e}")

# =========================
# SEARCH EXPENSE
# =========================

elif option == "Search Expense":

    st.subheader("🔍 Search Expense")

    keyword = st.text_input("Enter Keyword")

    if st.button("Search"):

        try:

            res = requests.get(
                f"{server_url}/search_expense/{keyword}"
            )

            if res.status_code == 200:

                data = res.json()

                if data:

                    df = pd.DataFrame(data)

                    st.dataframe(
                        df,
                        use_container_width=True
                    )

                else:
                    st.warning("No Data Found")

            else:
                st.error("Search Failed")

        except Exception as e:
            st.error(f"Error: {e}")

# =========================
# ANALYZE SPENDING
# =========================

elif option == "Analyze Spending":

    st.subheader("📊 Analyze Spending")

    try:

        res = requests.get(
            f"{server_url}/analyze_spending"
        )

        if res.status_code == 200:

            data = res.json()

            total = data["total_spending"]["total"]

            st.metric(
                label="Total Spending",
                value=f"₹ {total}"
            )

            category_data = data["category_spending"]

            if category_data:

                df = pd.DataFrame(category_data)

                st.dataframe(
                    df,
                    use_container_width=True
                )

                # Pie Chart
                fig = px.pie(
                    df,
                    names="category",
                    values="total",
                    title="Category Wise Spending"
                )

                st.plotly_chart(
                    fig,
                    use_container_width=True
                )

            else:
                st.warning("No Spending Data Found")

        else:
            st.error("Analysis Failed")

    except Exception as e:
        st.error(f"Error: {e}")