import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

# =============================
# Page Config
# =============================
st.set_page_config(
    page_title="YouTube Analytics Dashboard",
    page_icon="",
    layout="wide"
)

# =============================
# Basic Clean Styling
# =============================
st.markdown("""
<style>
.main-title {
    font-size: 36px;
    font-weight: 700;
    color: #0f172a;
}

.subtitle {
    font-size: 16px;
    color: #475569;
    margin-bottom: 20px;
}

.kpi-card {
    background-color: #ffffff;
    border-radius: 10px;
    padding: 20px;
    border: 1px solid #e5e7eb;
    text-align: center;
}

.kpi-title {
    color: #64748b;
    font-size: 14px;
    margin-bottom: 5px;
}

.kpi-value {
    color: #0f172a;
    font-size: 28px;
    font-weight: 700;
}

.section-title {
    font-size: 22px;
    font-weight: 600;
    color: #0f172a;
    margin-top: 30px;
    margin-bottom: 10px;
}
</style>
""", unsafe_allow_html=True)

# =============================
# Load Data
# =============================
DATA_PATH = Path("../data/sample_cleaned.csv")

if not DATA_PATH.exists():
    st.error("data/sample_cleaned.csv not found. Please add your CSV file.")
    st.stop()

df = pd.read_csv(DATA_PATH)
df.columns = [c.strip().lower() for c in df.columns]

# Ensure numeric columns
if "views" in df.columns:
    df["views"] = pd.to_numeric(df["views"], errors="coerce").fillna(0)

if "likes" in df.columns:
    df["likes"] = pd.to_numeric(df["likes"], errors="coerce").fillna(0)

# =============================
# Header
# =============================
st.markdown('<div class="main-title">YouTube Analytics Dashboard</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Overview of processed YouTube trending data</div>', unsafe_allow_html=True)

# =============================
# KPI Section
# =============================
st.markdown('<div class="section-title">Overview</div>', unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

total_videos = len(df)
total_channels = df["channel_title"].nunique() if "channel_title" in df.columns else 0
max_views = int(df["views"].max()) if "views" in df.columns else 0

if "likes" in df.columns and "views" in df.columns:
    valid_rows = df[(df["views"] > 0) & (df["likes"].notna())]
    if len(valid_rows) > 0:
        avg_engagement = (valid_rows["likes"] / valid_rows["views"]).mean()
    else:
        avg_engagement = 0
else:
    avg_engagement = 0

def kpi(col, title, value):
    col.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">{title}</div>
        <div class="kpi-value">{value}</div>
    </div>
    """, unsafe_allow_html=True)

kpi(col1, "Total Videos", total_videos)
kpi(col2, "Total Channels", total_channels)
kpi(col3, "Max Views", f"{max_views:,}")
kpi(col4, "Avg Engagement", f"{avg_engagement:.4f}")

# =============================
# Charts Section
# =============================
st.markdown('<div class="section-title">Analytics</div>', unsafe_allow_html=True)

left, right = st.columns(2)

# ---- Total Views by Category ----
if "category_id" in df.columns and "views" in df.columns:
    views_by_cat = (
        df.groupby("category_id")["views"]
        .sum()
        .reset_index()
        .sort_values("views", ascending=False)
    )

    fig1 = px.bar(
        views_by_cat,
        x="category_id",
        y="views",
        title="Total Views by Category",
        color_discrete_sequence=["#2563eb"]
    )
    fig1.update_layout(template="plotly_white", title_font_size=16)
    left.plotly_chart(fig1, use_container_width=True)

# ---- Average Engagement by Category (SAFE) ----
if "category_id" in df.columns and "likes" in df.columns and "views" in df.columns:

    temp = df.copy()

    # Keep only valid rows
    temp = temp[(temp["views"] > 0) & (temp["likes"].notna())]

    if len(temp) > 0:
        temp["engagement"] = temp["likes"] / temp["views"]

        eng_by_cat = (
            temp.groupby("category_id")["engagement"]
            .mean()
            .reset_index()
            .sort_values("engagement", ascending=False)
        )

        fig2 = px.bar(
            eng_by_cat,
            x="category_id",
            y="engagement",
            title="Average Engagement by Category",
            color_discrete_sequence=["#0f766e"]
        )
        fig2.update_layout(template="plotly_white", title_font_size=16)
        right.plotly_chart(fig2, use_container_width=True)
    else:
        right.info("Not enough valid data to compute engagement.")

# =============================
# Top Videos Section
# =============================
st.markdown('<div class="section-title">Top Videos</div>', unsafe_allow_html=True)

if "views" in df.columns:
    top_videos = df.sort_values("views", ascending=False).head(10)

    fig3 = px.bar(
        top_videos,
        x="views",
        y="title" if "title" in top_videos.columns else top_videos.index,
        orientation="h",
        title="Top 10 Videos by Views",
        color_discrete_sequence=["#334155"]
    )
    fig3.update_layout(template="plotly_white", title_font_size=16, yaxis=dict(autorange="reversed"))
    st.plotly_chart(fig3, use_container_width=True)

    st.dataframe(top_videos, use_container_width=True)

# =============================
# Footer
# =============================
st.markdown("---")
st.caption("Built by Himanshi • YouTube Data Engineering & Analytics Project")
