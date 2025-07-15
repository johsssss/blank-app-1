import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO

st.set_page_config(page_title="🌍 Environmental Impact Simulator", layout="wide")

st.title("🌍 Environmental Impact Simulator")
st.markdown("This tool models the impact of industrial growth on employment, emissions, water usage, and community health.")

# Sidebar inputs
st.sidebar.header("🛠️ Simulation Settings")
time_steps = st.sidebar.slider("Years to simulate", 5, 50, 20)
initial_operations = st.sidebar.slider("Initial operations", 10, 500, 100)
growth_rate = st.sidebar.slider("Growth rate (%)", 1, 20, 5) / 100
jobs_per_op = st.sidebar.slider("Jobs per operation", 1, 100, 10)
emission_per_op = st.sidebar.slider("Emissions per operation", 0.1, 2.0, 0.8)
water_per_op = st.sidebar.slider("Water use per operation", 0.1, 2.0, 0.5)
health_impact = st.sidebar.slider("Health impact factor", 0.1, 2.0, 0.3)

# 🧠 Run Simulation
years = list(range(1, time_steps + 1))
operations = initial_operations
employment, emissions, water_use, health_index = [], [], [], []
health = 100

for _ in years:
    emp = jobs_per_op * operations
    emi = emission_per_op * operations
    wat = water_per_op * operations
    hea = max(0, 100 - health_impact * emi)

    employment.append(emp)
    emissions.append(emi)
    water_use.append(wat)
    health_index.append(hea)
    operations *= (1 + growth_rate)

df = pd.DataFrame({
    "Year": years,
    "Employment": employment,
    "Emissions": emissions,
    "Water Use": water_use,
    "Health Index": health_index
})

# Tabs for visual outputs
tab1, tab2, tab3 = st.tabs(["📈 Line Chart", "🗺️ Area Chart", "📊 Data Summary"])

# 🎨 Custom Colors
colors = {
    "Employment": "#1f77b4",
    "Emissions": "#d62728",
    "Water Use": "#2ca02c",
    "Health Index": "#9467bd"
}

with tab1:
    st.subheader("📈 Simulation Trends Over Time")
    fig, ax = plt.subplots(figsize=(10, 5))
    for col in df.columns[1:]:
        ax.plot(df["Year"], df[col], label=col, color=colors[col], linewidth=2)
    ax.set_xlabel("Year")
    ax.set_ylabel("Value")
    ax.set_title("Growth of Key Metrics")
    ax.legend()
    ax.grid(True)
    st.pyplot(fig)

with tab2:
    st.subheader("🗺️ Environmental Impact (Emissions + Water Use)")
    fig2, ax2 = plt.subplots(figsize=(10, 5))
    ax2.stackplot(df["Year"], df["Emissions"], df["Water Use"],
                  labels=["Emissions", "Water Use"],
                  colors=[colors["Emissions"], colors["Water Use"]],
                  alpha=0.6)
    ax2.set_xlabel("Year")
    ax2.set_ylabel("Index Value")
    ax2.set_title("Stacked Environmental Impact")
    ax2.legend(loc='upper left')
    ax2.grid(True)
    st.pyplot(fig2)

with tab3:
    st.subheader("📊 Final Year Summary")
    st.dataframe(df.tail(1).T)

    st.markdown("### Full Data Table")
    st.dataframe(df)

    # ✅ Excel export
    @st.cache_data
    def convert_to_excel(data):
        buffer = BytesIO()
        with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
            data.to_excel(writer, index=False)
        buffer.seek(0)
        return buffer

    excel_data = convert_to_excel(df)

    st.download_button(
        label="💾 Download Full Dataset as Excel",
        data=excel_data,
        file_name="environment_simulation.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
