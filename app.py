import streamlit as st
import pandas as pd
import datetime
from PIL import Image
import plotly.express as px
import plotly.graph_objects as go

# ---------------- PAGE CONFIG ----------------
st.set_page_config(layout="wide")

st.markdown("""
<style>
div.block-container{
    padding-top:1rem;
}
</style>
""", unsafe_allow_html=True)

# ---------------- LOAD DATA ----------------
df = pd.read_excel("Adidas.xlsx")

# ---------------- HEADER SECTION ----------------
image = Image.open("adidas-logo.jpg")

col1, col2 = st.columns([0.1, 0.9])

with col1:
    st.image(image, width=100)

html_title = """
<center>
    <h1 style="color:#000000;">
        Adidas Interactive Sales Dashboard
    </h1>
</center>
"""

with col2:
    st.markdown(html_title, unsafe_allow_html=True)

# ---------------- DATE SECTION ----------------
col3, col4, col5 = st.columns([0.15, 0.42, 0.42])

with col3:
    today = datetime.datetime.now().strftime("%d %B %Y")
    st.write(f"### Last Updated")
    st.write(today)

# ---------------- BAR CHART ----------------
with col4:
    retailer_sales = df.groupby("Retailer")["TotalSales"].sum().reset_index()

    fig = px.bar(
        retailer_sales,
        x="Retailer",
        y="TotalSales",
        title="Total Sales by Retailer",
        text_auto=True,
        template="plotly_white"
    )

    st.plotly_chart(fig, use_container_width=True)

# ---------------- LINE CHART ----------------
df["Month_Year"] = df["InvoiceDate"].dt.strftime("%b-%Y")

monthly_sales = (
    df.groupby("Month_Year")["TotalSales"]
    .sum()
    .reset_index()
)

with col5:
    fig1 = px.line(
        monthly_sales,
        x="Month_Year",
        y="TotalSales",
        markers=True,
        title="Monthly Sales Trend",
        template="plotly_white"
    )

    st.plotly_chart(fig1, use_container_width=True)

# ---------------- DOWNLOAD SECTION ----------------
_, view1, dwn1, view2, dwn2 = st.columns([0.1, 0.2, 0.2, 0.2, 0.2])

with view1:
    expander = st.expander("View Retailer Sales")
    expander.write(retailer_sales)

with dwn1:
    st.download_button(
        "Download Retailer Data",
        retailer_sales.to_csv(index=False).encode("utf-8"),
        file_name="RetailerSales.csv",
        mime="text/csv"
    )

with view2:
    expander = st.expander("View Monthly Sales")
    expander.write(monthly_sales)

with dwn2:
    st.download_button(
        "Download Monthly Sales",
        monthly_sales.to_csv(index=False).encode("utf-8"),
        file_name="MonthlySales.csv",
        mime="text/csv"
    )

st.divider()

# ---------------- COMBO CHART ----------------
state_data = (
    df.groupby("State")[["TotalSales", "UnitsSold"]]
    .sum()
    .reset_index()
)

fig3 = go.Figure()

fig3.add_trace(
    go.Bar(
        x=state_data["State"],
        y=state_data["TotalSales"],
        name="Total Sales"
    )
)

fig3.add_trace(
    go.Scatter(
        x=state_data["State"],
        y=state_data["UnitsSold"],
        mode="lines+markers",
        name="Units Sold",
        yaxis="y2"
    )
)

fig3.update_layout(
    title="Total Sales and Units Sold by State",
    xaxis=dict(title="State"),
    yaxis=dict(title="Total Sales"),
    yaxis2=dict(
        title="Units Sold",
        overlaying="y",
        side="right"
    ),
    template="plotly_white",
    legend=dict(x=0.8, y=1.1)
)

_, col6 = st.columns([0.05, 1])

with col6:
    st.plotly_chart(fig3, use_container_width=True)

_, view3, dwn3 = st.columns([0.5, 0.25, 0.25])

with view3:
    expander = st.expander("View State Wise Sales")
    expander.write(state_data)

with dwn3:
    st.download_button(
        "Download State Data",
        state_data.to_csv(index=False).encode("utf-8"),
        file_name="StateSales.csv",
        mime="text/csv"
    )

st.divider()

# ---------------- HEATMAP SECTION ----------------
st.subheader("🔥 Heatmap: Region vs City Sales")

heatmap_data = (
    df.groupby(["Region", "City"])["TotalSales"]
    .sum()
    .reset_index()
)

pivot_table = heatmap_data.pivot(
    index="Region",
    columns="City",
    values="TotalSales"
)

fig4 = px.imshow(
    pivot_table,
    text_auto=True,
    aspect="auto",
    title="Sales Heatmap by Region and City",
    template="plotly_white"
)

st.plotly_chart(fig4, use_container_width=True)

_, view4, dwn4 = st.columns([0.5, 0.25, 0.25])

with view4:
    expander = st.expander("View Heatmap Data")
    expander.write(pivot_table)

with dwn4:
    st.download_button(
        "Download Heatmap Data",
        pivot_table.to_csv().encode("utf-8"),
        file_name="HeatmapData.csv",
        mime="text/csv"
    )

st.divider()

# ---------------- RAW DATA ----------------
_, view5, dwn5 = st.columns([0.5, 0.25, 0.25])

with view5:
    expander = st.expander("View Raw Dataset")
    expander.write(df)

with dwn5:
    st.download_button(
        "Download Raw Data",
        df.to_csv(index=False).encode("utf-8"),
        file_name="RawData.csv",
        mime="text/csv"
    )