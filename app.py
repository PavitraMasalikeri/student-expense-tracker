import streamlit as st
import pandas as pd

from database import (
    add_expense,
    get_expenses,
    update_expense,
    delete_expense,
    register_user,
    login_user
)

from reports import (
    create_dataframe,
    category_report,
    monthly_report,
    daily_report,
    category_bar_chart,
    monthly_bar_chart,
    daily_bar_chart,
    expense_pie_chart
)


st.set_page_config(
    page_title="Student Expense Tracker",
    page_icon="💰",
    layout="wide"
)


st.markdown(
    """
    <style>

    .stApp {
        background-color: #f5f7fb;
    }

    [data-testid="stSidebar"] {
        background-color: #1f2937;
    }

    [data-testid="stSidebar"] * {
        color: white;
    }

    h1 {
        color: #1f2937;
        font-weight: 700;
    }

    h2, h3 {
        color: #374151;
    }

    [data-testid="stMetric"] {
        background-color: white;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0px 2px 8px rgba(0, 0, 0, 0.08);
    }

    .stButton > button {
        width: 100%;
        border-radius: 8px;
        font-weight: 600;
        padding: 10px;
    }

    [data-testid="stDataFrame"] {
        border-radius: 10px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = ""


if not st.session_state.logged_in:

    st.title("💰 Student Expense Tracker")

    st.write(
        "Please login or create a new account to continue."
    )

    st.divider()

    login_tab, signup_tab = st.tabs(
        [
            "🔐 Login",
            "📝 Signup"
        ]
    )

    with login_tab:

        st.subheader("🔐 Student Login")

        username = st.text_input(
            "Username",
            key="login_username"
        )

        password = st.text_input(
            "Password",
            type="password",
            key="login_password"
        )

        if st.button(
            "🔐 Login",
            key="login_button"
        ):

            if username.strip() == "":

                st.error(
                    "❌ Please enter your username."
                )

            elif password == "":

                st.error(
                    "❌ Please enter your password."
                )

            else:

                success = login_user(
                    username.strip(),
                    password
                )

                if success:

                    st.session_state.logged_in = True
                    st.session_state.username = username.strip()

                    st.success(
                        "✅ Login successful!"
                    )

                    st.rerun()

                else:

                    st.error(
                        "❌ Invalid username or password."
                    )

    with signup_tab:

        st.subheader("📝 Create New Account")

        new_username = st.text_input(
            "Create Username",
            key="signup_username"
        )

        new_password = st.text_input(
            "Create Password",
            type="password",
            key="signup_password"
        )

        confirm_password = st.text_input(
            "Confirm Password",
            type="password",
            key="confirm_password"
        )

        st.info(
            """
            **Username requirements:**
            - At least 5 characters
            - At least one uppercase letter
            - At least one lowercase letter
            - At least one number

            **Password requirements:**
            - At least 8 characters
            - At least one uppercase letter
            - At least one lowercase letter
            - At least one number
            - At least one special character
            """
        )

        if st.button(
            "📝 Create Account",
            key="signup_button"
        ):

            username = new_username.strip()
            password = new_password

            if username == "":

                st.error(
                    "❌ Username cannot be empty."
                )

            elif len(username) < 5:

                st.error(
                    "❌ Username must contain at least 5 characters."
                )

            elif not any(
                char.isupper()
                for char in username
            ):

                st.error(
                    "❌ Username must contain at least one uppercase letter."
                )

            elif not any(
                char.islower()
                for char in username
            ):

                st.error(
                    "❌ Username must contain at least one lowercase letter."
                )

            elif not any(
                char.isdigit()
                for char in username
            ):

                st.error(
                    "❌ Username must contain at least one number."
                )

            elif password == "":

                st.error(
                    "❌ Password cannot be empty."
                )

            elif len(password) < 8:

                st.error(
                    "❌ Password must contain at least 8 characters."
                )

            elif not any(
                char.isupper()
                for char in password
            ):

                st.error(
                    "❌ Password must contain at least one uppercase letter."
                )

            elif not any(
                char.islower()
                for char in password
            ):

                st.error(
                    "❌ Password must contain at least one lowercase letter."
                )

            elif not any(
                char.isdigit()
                for char in password
            ):

                st.error(
                    "❌ Password must contain at least one number."
                )

            elif not any(
                not char.isalnum()
                for char in password
            ):

                st.error(
                    "❌ Password must contain at least one special character."
                )

            elif password != confirm_password:

                st.error(
                    "❌ Passwords do not match."
                )

            else:

                success = register_user(
                    username,
                    password
                )

                if success:

                    st.success(
                        "✅ Account created successfully! You can now login."
                    )

                else:

                    st.error(
                        "❌ Username already exists."
                    )


else:

    current_username = st.session_state.username

    st.sidebar.title("💰 Expense Tracker")

    st.sidebar.write(
        f"Welcome, {current_username}! 👋"
    )

    st.sidebar.divider()

    menu = st.sidebar.radio(
        "Navigation",
        [
            "📊 Dashboard",
            "➕ Add Expense",
            "📋 View Expenses",
            "✏️ Edit Expense",
            "🗑️ Delete Expense",
            "📈 Reports"
        ]
    )

    st.sidebar.divider()

    if st.sidebar.button("🚪 Logout"):

        st.session_state.logged_in = False
        st.session_state.username = ""

        st.rerun()


    if menu == "📊 Dashboard":

        st.title("📊 Dashboard")

        st.write(
            "Overview of your student expenses."
        )

        expenses = get_expenses(
            current_username
        )

        if expenses:

            df = pd.DataFrame(
                expenses,
                columns=[
                    "ID",
                    "Date",
                    "Category",
                    "Description",
                    "Amount"
                ]
            )

            total_expenses = df["Amount"].sum()

            today = str(
                pd.Timestamp.today().date()
            )

            todays_expenses = df[
                df["Date"] == today
            ]["Amount"].sum()

            current_month = (
                pd.Timestamp.today()
                .strftime("%Y-%m")
            )

            monthly_expenses = df[
                df["Date"].str.startswith(
                    current_month
                )
            ]["Amount"].sum()

            highest_category = (
                df.groupby("Category")["Amount"]
                .sum()
                .idxmax()
            )

            col1, col2, col3, col4 = st.columns(4)

            col1.metric(
                "Total Expenses",
                f"₹{total_expenses:.2f}"
            )

            col2.metric(
                "Today's Expenses",
                f"₹{todays_expenses:.2f}"
            )

            col3.metric(
                "Monthly Expenses",
                f"₹{monthly_expenses:.2f}"
            )

            col4.metric(
                "Highest Category",
                highest_category
            )

            st.divider()

            st.subheader("Recent Expenses")

            recent_expenses = df.head(5)

            st.dataframe(
                recent_expenses,
                use_container_width=True
            )

        else:

            st.info(
                "No expenses available for dashboard."
            )


    elif menu == "➕ Add Expense":

        st.title("➕ Add Expense")

        st.write(
            "Record a new expense in your tracker."
        )

        st.divider()

        col1, col2 = st.columns(2)

        with col1:

            expense_date = st.date_input(
                "Select expense date"
            )

            category = st.selectbox(
                "Select expense category",
                [
                    "Food",
                    "Travel",
                    "Shopping",
                    "College Fees",
                    "Mobile Recharge",
                    "Entertainment",
                    "Other"
                ]
            )

        with col2:

            description = st.text_input(
                "Enter description"
            )

            amount = st.number_input(
                "Enter amount",
                min_value=0.0,
                step=1.0
            )

        st.divider()

        if st.button("💾 Save Expense"):

            if description.strip() == "":

                st.error(
                    "❌ Description cannot be empty."
                )

            elif amount <= 0:

                st.error(
                    "❌ Amount must be greater than ₹0."
                )

            else:

                success = add_expense(
                    current_username,
                    str(expense_date),
                    category,
                    description.strip(),
                    amount
                )

                if success:

                    st.success(
                        "✅ Expense saved successfully!"
                    )

                else:

                    st.error(
                        "❌ Something went wrong while saving the expense."
                    )


    elif menu == "📋 View Expenses":

        st.title("📋 View Expenses")

        st.write(
            "View and filter all your recorded expenses."
        )

        expenses = get_expenses(
            current_username
        )

        if expenses:

            df = pd.DataFrame(
                expenses,
                columns=[
                    "ID",
                    "Date",
                    "Category",
                    "Description",
                    "Amount"
                ]
            )

            st.divider()

            categories = [
                "All"
            ] + sorted(
                df["Category"].unique().tolist()
            )

            selected_category = st.selectbox(
                "Filter by Category",
                categories
            )

            if selected_category != "All":

                df = df[
                    df["Category"] == selected_category
                ]

            filter_by_date = st.checkbox(
                "Filter by Date"
            )

            if filter_by_date:

                selected_date = st.date_input(
                    "Select Date"
                )

                selected_date = str(
                    selected_date
                )

                df = df[
                    df["Date"] == selected_date
                ]

            st.divider()

            st.dataframe(
                df,
                use_container_width=True
            )

            filtered_total = df["Amount"].sum()

            st.metric(
                "Total Displayed Expenses",
                f"₹{filtered_total:.2f}"
            )

        else:

            st.info(
                "No expenses found."
            )


    elif menu == "✏️ Edit Expense":

        st.title("✏️ Edit Expense")

        st.write(
            "Modify an existing expense."
        )

        expenses = get_expenses(
            current_username
        )

        if expenses:

            expense_ids = [
                expense[0]
                for expense in expenses
            ]

            selected_id = st.selectbox(
                "Select Expense ID",
                expense_ids
            )

            selected_expense = next(
                expense
                for expense in expenses
                if expense[0] == selected_id
            )

            current_date = selected_expense[1]
            current_category = selected_expense[2]
            current_description = selected_expense[3]
            current_amount = selected_expense[4]

            st.divider()

            st.write(
                "**Current Expense Date:**",
                current_date
            )

            category_list = [
                "Food",
                "Travel",
                "Shopping",
                "College Fees",
                "Mobile Recharge",
                "Entertainment",
                "Other"
            ]

            new_category = st.selectbox(
                "Select New Category",
                category_list,
                index=category_list.index(
                    current_category
                )
            )

            new_description = st.text_input(
                "New Description",
                value=current_description
            )

            new_amount = st.number_input(
                "New Amount",
                min_value=0.0,
                value=float(current_amount),
                step=1.0
            )

            st.divider()

            if st.button("🔄 Update Expense"):

                if new_description.strip() == "":

                    st.error(
                        "❌ Description cannot be empty."
                    )

                elif new_amount <= 0:

                    st.error(
                        "❌ Amount must be greater than ₹0."
                    )

                else:

                    success = update_expense(
                        current_username,
                        selected_id,
                        new_category,
                        new_description.strip(),
                        new_amount
                    )

                    if success:

                        st.success(
                            "✅ Expense updated successfully!"
                        )

                    else:

                        st.error(
                            "❌ Unable to update the expense."
                        )

        else:

            st.info(
                "No expenses available to edit."
            )


    elif menu == "🗑️ Delete Expense":

        st.title("🗑️ Delete Expense")

        st.write(
            "Remove an existing expense from your tracker."
        )

        expenses = get_expenses(
            current_username
        )

        if expenses:

            expense_ids = [
                expense[0]
                for expense in expenses
            ]

            selected_id = st.selectbox(
                "Select Expense ID to Delete",
                expense_ids
            )

            selected_expense = next(
                expense
                for expense in expenses
                if expense[0] == selected_id
            )

            st.divider()

            st.write(
                "**Date:**",
                selected_expense[1]
            )

            st.write(
                "**Category:**",
                selected_expense[2]
            )

            st.write(
                "**Description:**",
                selected_expense[3]
            )

            st.write(
                "**Amount:**",
                f"₹{selected_expense[4]:.2f}"
            )

            st.warning(
                "Deleting this expense cannot be undone."
            )

            st.divider()

            confirm_delete = st.checkbox(
                "I confirm that I want to delete this expense."
            )

            if confirm_delete:

                if st.button("🗑️ Delete Expense"):

                    success = delete_expense(
                        current_username,
                        selected_id
                    )

                    if success:

                        st.success(
                            "✅ Expense deleted successfully!"
                        )

                    else:

                        st.error(
                            "❌ Unable to delete the expense."
                        )

        else:

            st.info(
                "No expenses available to delete."
            )


    elif menu == "📈 Reports":

        st.title("📈 Expense Reports")

        st.write(
            "Analyze your spending patterns using reports and charts."
        )

        expenses = get_expenses(
            current_username
        )

        if expenses:

            df = create_dataframe(
                expenses
            )

            st.subheader(
                "Category-wise Spending"
            )

            category_data = category_report(
                df
            )

            st.dataframe(
                category_data.reset_index(),
                use_container_width=True
            )

            st.subheader(
                "Category-wise Expense Chart"
            )

            fig = category_bar_chart(
                category_data
            )

            st.pyplot(fig)

            st.subheader(
                "Monthly Spending"
            )

            monthly_data = monthly_report(
                df
            )

            st.dataframe(
                monthly_data,
                use_container_width=True
            )

            st.subheader(
                "Monthly Spending Chart"
            )

            fig = monthly_bar_chart(
                monthly_data
            )

            st.pyplot(fig)

            st.subheader(
                "Daily Spending"
            )

            daily_data = daily_report(
                df
            )

            st.dataframe(
                daily_data,
                use_container_width=True
            )

            st.subheader(
                "Daily Spending Chart"
            )

            fig = daily_bar_chart(
                daily_data
            )

            st.pyplot(fig)

            st.subheader(
                "Expense Distribution"
            )

            fig = expense_pie_chart(
                category_data
            )

            st.pyplot(fig)

        else:

            st.info(
                "No expenses available for reports."
            )