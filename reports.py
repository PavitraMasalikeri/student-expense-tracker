import pandas as pd
import matplotlib.pyplot as plt


def create_dataframe(expenses):
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

    return df


def category_report(df):
    report = (
        df.groupby("Category")["Amount"]
        .sum()
        .sort_values(ascending=False)
    )

    return report


def monthly_report(df):
    df = df.copy()

    df["Month"] = df["Date"].str[:7]

    report = (
        df.groupby("Month")["Amount"]
        .sum()
        .reset_index()
    )

    return report


def daily_report(df):
    report = (
        df.groupby("Date")["Amount"]
        .sum()
        .reset_index()
    )

    return report


def category_bar_chart(category_data):
    fig, ax = plt.subplots()

    ax.bar(
        category_data.index,
        category_data.values
    )

    ax.set_xlabel("Category")
    ax.set_ylabel("Amount")
    ax.set_title("Category-wise Spending")

    plt.xticks(rotation=45)

    return fig


def monthly_bar_chart(monthly_data):
    fig, ax = plt.subplots()

    ax.bar(
        monthly_data["Month"],
        monthly_data["Amount"]
    )

    ax.set_xlabel("Month")
    ax.set_ylabel("Amount")
    ax.set_title("Monthly Spending")

    return fig


def daily_bar_chart(daily_data):
    fig, ax = plt.subplots()

    ax.bar(
        daily_data["Date"],
        daily_data["Amount"]
    )

    ax.set_xlabel("Date")
    ax.set_ylabel("Amount")
    ax.set_title("Daily Spending")

    plt.xticks(rotation=45)

    return fig


def expense_pie_chart(category_data):
    fig, ax = plt.subplots()

    ax.pie(
        category_data.values,
        labels=category_data.index,
        autopct="%1.1f%%"
    )

    ax.set_title("Expense Distribution by Category")

    return fig