import streamlit as st
import pandas as pd
import plotly.express as px

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="SaaS Analytics Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------- TITLE ----------------
st.title("🚀 SaaS Growth Dashboard")
st.markdown("Monitor user growth, conversions, and revenue performance")

# ---------------- LOAD DATA ----------------
df = pd.read_csv("data.csv")
df['signup_date'] = pd.to_datetime(df['signup_date'])

# ---------------- SIDEBAR ----------------
st.sidebar.header("🎛 Filters")

countries = st.sidebar.multiselect(
    "Country",
    options=df['country'].unique(),
    default=df['country'].unique()
)

channels = st.sidebar.multiselect(
    "Channel",
    options=df['channel'].unique(),
    default=df['channel'].unique()
)

plans = st.sidebar.multiselect(
    "Plan",
    options=df['plan'].unique(),
    default=df['plan'].unique()
)

# Filter data
filtered_df = df[
    (df['country'].isin(countries)) &
    (df['channel'].isin(channels)) &
    (df['plan'].isin(plans))
]

# ---------------- KPIs ----------------
st.markdown("## 📊 Key Metrics")

total_users = len(filtered_df)
converted = filtered_df['converted'].sum()
conversion_rate = (converted / total_users) * 100 if total_users else 0
revenue = filtered_df['revenue'].sum()
avg_session = filtered_df['session_time'].mean()

k1, k2, k3, k4, k5 = st.columns(5)

k1.metric("Users", total_users)
k2.metric("Conversions", int(converted))
k3.metric("Conversion Rate", f"{conversion_rate:.2f}%")
k4.metric("Revenue", f"{revenue} DKK")
k5.metric("Avg Session", f"{avg_session:.1f} min")

st.markdown("---")

# ---------------- GROWTH SECTION ----------------
st.markdown("## 📈 Growth Trends")

col1, col2 = st.columns(2)

with col1:
    users_time = filtered_df.groupby('signup_date').size().reset_index(name='users')
    fig_users = px.line(users_time, x='signup_date', y='users',
                        title="User Growth Over Time")
    st.plotly_chart(fig_users, use_container_width=True)

with col2:
    revenue_time = filtered_df.groupby('signup_date')['revenue'].sum().reset_index()
    fig_rev = px.line(revenue_time, x='signup_date', y='revenue',
                      title="Revenue Growth Over Time")
    st.plotly_chart(fig_rev, use_container_width=True)

st.markdown("---")

# ---------------- FUNNEL ----------------
st.markdown("## 🧭 Funnel Analysis")

funnel = filtered_df['step'].value_counts().reset_index()
funnel.columns = ['step', 'count']

fig_funnel = px.bar(funnel, x='step', y='count',
                    title="User Journey Drop-off")
st.plotly_chart(fig_funnel, use_container_width=True)

st.markdown("---")

# ---------------- SEGMENTATION ----------------
st.markdown("## 🌍 Segmentation Insights")

col3, col4 = st.columns(2)

with col3:
    country_rev = filtered_df.groupby('country')['revenue'].sum().reset_index()
    fig_country = px.bar(country_rev, x='country', y='revenue',
                         title="Revenue by Country")
    st.plotly_chart(fig_country, use_container_width=True)

with col4:
    channel_conv = filtered_df.groupby('channel')['converted'].mean().reset_index()
    fig_channel = px.bar(channel_conv, x='channel', y='converted',
                         title="Conversion Rate by Channel")
    st.plotly_chart(fig_channel, use_container_width=True)

st.markdown("---")

# ---------------- PRODUCT ----------------
st.markdown("## 💰 Product Performance")

plan_rev = filtered_df.groupby('plan')['revenue'].sum().reset_index()

fig_plan = px.bar(plan_rev, x='plan', y='revenue',
                  title="Revenue by Plan")
st.plotly_chart(fig_plan, use_container_width=True)

st.markdown("---")

# ---------------- DEVICE ----------------
st.markdown("## 📱 Device Usage")

device = filtered_df['device'].value_counts().reset_index()
device.columns = ['device', 'count']

fig_device = px.pie(device, names='device', values='count',
                    title="Device Distribution")
st.plotly_chart(fig_device, use_container_width=True)

st.markdown("---")

# ---------------- INSIGHTS ----------------
st.markdown("## 🧠 Key Insights")

if total_users == 0:
    st.warning("No data available for selected filters.")
else:
    if conversion_rate < 40:
        st.warning("⚠️ Low conversion rate → optimize onboarding funnel")

    best_channel = channel_conv.sort_values(by='converted', ascending=False).iloc[0]['channel']
    best_country = country_rev.sort_values(by='revenue', ascending=False).iloc[0]['country']
    best_plan = plan_rev.sort_values(by='revenue', ascending=False).iloc[0]['plan']

    st.success(f"🚀 Best Channel: {best_channel}")
    st.success(f"🌍 Top Country: {best_country}")
    st.success(f"💰 Best Plan: {best_plan}")

st.markdown("---")

# ---------------- FOOTER ----------------
st.caption("Built for demonstrating KPI tracking, funnel analysis, and growth insights by Aryan Rijal")