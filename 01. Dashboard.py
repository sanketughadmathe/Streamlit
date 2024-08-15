import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st

# Page configuration
st.set_page_config(page_title="Sales Dashboard", page_icon=":bar_chart:", layout="wide")


# Load data
@st.cache_data
def load_data():
    # Replace this with your actual data loading logic
    df = pd.DataFrame(
        {
            "Date": pd.date_range(start="2023-01-01", end="2023-12-31", freq="D"),
            "Sales": np.random.randint(100, 1000, 365),
            "Category": np.random.choice(
                ["Electronics", "Clothing", "Food", "Books"], 365
            ),
            "Region": np.random.choice(["North", "South", "East", "West"], 365),
        }
    )
    return df


df = load_data()

# Sidebar
st.sidebar.header("Filter Options")

# Date range selector
min_date = df["Date"].min().to_pydatetime()
max_date = df["Date"].max().to_pydatetime()
start_date = st.sidebar.date_input(
    "Start Date", min_date, min_value=min_date, max_value=max_date
)
end_date = st.sidebar.date_input(
    "End Date", max_date, min_value=min_date, max_value=max_date
)

# Ensure end_date is not before start_date
if start_date > end_date:
    st.sidebar.error("Error: End date must be after start date.")
    st.stop()

# Category multiselect
categories = st.sidebar.multiselect(
    "Select Categories",
    options=df["Category"].unique(),
    default=df["Category"].unique(),
)

# Region multiselect
regions = st.sidebar.multiselect(
    "Select Regions", options=df["Region"].unique(), default=df["Region"].unique()
)

# Filter data
filtered_df = df[
    (df["Date"].dt.date >= start_date)
    & (df["Date"].dt.date <= end_date)
    & (df["Category"].isin(categories))
    & (df["Region"].isin(regions))
]

# Main content
st.title("📊 Sales Dashboard")
st.markdown("---")

# KPIs
col1, col2, col3, col4 = st.columns(4)

total_sales = filtered_df["Sales"].sum()
avg_daily_sales = filtered_df["Sales"].mean()
top_category = filtered_df.groupby("Category")["Sales"].sum().idxmax()
top_region = filtered_df.groupby("Region")["Sales"].sum().idxmax()

col1.metric("Total Sales", f"${total_sales:,.0f}")
col2.metric("Avg Daily Sales", f"${avg_daily_sales:,.0f}")
col3.metric("Top Category", top_category)
col4.metric("Top Region", top_region)

st.markdown("---")

# Charts
col1, col2 = st.columns(2)

# Sales over time
with col1:
    st.subheader("Sales Over Time")
    fig_line = px.line(filtered_df, x="Date", y="Sales", title="Daily Sales Trend")
    st.plotly_chart(fig_line, use_container_width=True)

# Sales by category
with col2:
    st.subheader("Sales by Category")
    fig_pie = px.pie(
        filtered_df,
        values="Sales",
        names="Category",
        title="Sales Distribution by Category",
    )
    st.plotly_chart(fig_pie, use_container_width=True)

# Sales by region
st.subheader("Sales by Region")
fig_bar = px.bar(
    filtered_df.groupby("Region")["Sales"].sum().reset_index(),
    x="Region",
    y="Sales",
    title="Total Sales by Region",
)
st.plotly_chart(fig_bar, use_container_width=True)

# Data table
st.subheader("Detailed Data")
st.dataframe(filtered_df.style.highlight_max(axis=0), use_container_width=True)

# Footer
st.markdown("---")
st.markdown("Created with ❤️ using Streamlit")
