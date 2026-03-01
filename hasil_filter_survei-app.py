import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Dashboard Survei Pendidikan Fisika", layout="wide")

st.title("📊 Dashboard Survei Pendidikan Fisika")
st.markdown("### Visualisasi dan Analisis Data 100 Responden")

# =====================================================
# LOAD DATA
# =====================================================
df = pd.read_excel("survei_pendidikan_fisika.xlsx", skiprows=2)

df.columns = df.columns.str.strip()
df = df.dropna(how="all")

# =====================================================
# SIDEBAR FILTER
# =====================================================
st.sidebar.header("🔎 Filter Data")

jk_filter = st.sidebar.multiselect(
    "Pilih Jenis Kelamin",
    options=df["JK"].unique(),
    default=df["JK"].unique()
)

pendidikan_filter = st.sidebar.multiselect(
    "Pilih Pendidikan",
    options=df["Pendidikan"].unique(),
    default=df["Pendidikan"].unique()
)

df_filtered = df[
    (df["JK"].isin(jk_filter)) &
    (df["Pendidikan"].isin(pendidikan_filter))
]

# =====================================================
# METRIC UTAMA
# =====================================================
st.divider()

col1, col2, col3 = st.columns(3)

col1.metric("👥 Jumlah Responden", len(df_filtered))
col2.metric("📈 Rata-rata Nilai", round(df_filtered["Nilai"].mean(), 2))
col3.metric("❤️ Rata-rata Minat", round(df_filtered["Minat"].mean(), 2))

st.divider()

# =====================================================
# VISUALISASI
# =====================================================
st.subheader("📊 Visualisasi Data")

# ------------------ ROW 1 ------------------
col4, col5 = st.columns(2)

with col4:
    fig_jk = px.pie(
        df_filtered,
        names="JK",
        title="Distribusi Jenis Kelamin"
    )
    st.plotly_chart(fig_jk, use_container_width=True)

with col5:
    fig_pendidikan = px.histogram(
        df_filtered,
        x="Pendidikan",
        title="Distribusi Pendidikan",
        text_auto=True
    )
    st.plotly_chart(fig_pendidikan, use_container_width=True)

# ------------------ ROW 2 ------------------
col6, col7 = st.columns(2)

with col6:
    fig_metode = px.box(
        df_filtered,
        x="Metode",
        y="Nilai",
        title="Perbandingan Nilai Berdasarkan Metode"
    )
    st.plotly_chart(fig_metode, use_container_width=True)

with col7:
    avg_nilai = df_filtered.groupby("Metode")["Nilai"].mean().reset_index()

    fig_avg = px.bar(
        avg_nilai,
        x="Metode",
        y="Nilai",
        title="Rata-rata Nilai per Metode",
        text_auto=".2f"
    )
    st.plotly_chart(fig_avg, use_container_width=True)

# ------------------ ROW 3 ------------------
fig_scatter = px.scatter(
    df_filtered,
    x="Minat",
    y="Nilai",
    color="Metode",
    size="Jam belajar",
    title="Hubungan Minat, Nilai, dan Jam Belajar",
    hover_data=["JK", "Pendidikan"]
)

st.plotly_chart(fig_scatter, use_container_width=True)

# =====================================================
# INSIGHT OTOMATIS
# =====================================================
st.divider()
st.subheader("📌 Insight Otomatis")

# Metode terbaik
metode_terbaik = avg_nilai.sort_values(by="Nilai", ascending=False).iloc[0]

st.success(
    f"Metode dengan rata-rata nilai tertinggi adalah **{metode_terbaik['Metode']}** "
    f"dengan rata-rata nilai **{round(metode_terbaik['Nilai'],2)}**."
)

# Korelasi minat dan nilai
korelasi = df_filtered["Minat"].corr(df_filtered["Nilai"])

st.info(
    f"Korelasi antara Minat dan Nilai sebesar **{round(korelasi,2)}**. "
    "Semakin mendekati 1 berarti hubungan semakin kuat."
)

st.caption("Dashboard dibuat menggunakan Streamlit dan Plotly Express.")
