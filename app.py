import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Page configuration
st.set_page_config(
    page_title="Ireland Job Market Dashboard",
    layout="wide"
)

# Title and description
st.title("🇮🇪 Ireland Job Market – Open Roles")
st.caption(
    "Based on aggregated JSearch job listings. "
    "Counts represent sampled demand, not a full census."
)

# Load data
@st.cache_data
def load_data():
    return pd.read_csv("ireland_open_roles_by_title.csv")

df = load_data()
df = df.sort_values("open_roles", ascending=False)

# KPI section
col1, col2 = st.columns(2)

with col1:
    st.metric("Roles tracked", len(df))

with col2:
    st.metric("Total open roles (sampled)", int(df["open_roles"].sum()))

st.divider()

# Role filter
selected_roles = st.multiselect(
    "Select job roles",
    options=df["job_title"].tolist(),
    default=df["job_title"].tolist()
)

filtered_df = df[df["job_title"].isin(selected_roles)]

# Bar chart
st.subheader("📊 Open roles by job title")

fig, ax = plt.subplots(figsize=(10, 5))
ax.barh(filtered_df["job_title"], filtered_df["open_roles"])
ax.invert_yaxis()
ax.set_xlabel("Number of open roles")

st.pyplot(fig)

# Data table
st.subheader("📋 Detailed data")
st.dataframe(filtered_df, use_container_width=True)
