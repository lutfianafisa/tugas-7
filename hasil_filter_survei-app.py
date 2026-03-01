import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

# =====================================================
# KONFIGURASI HALAMAN
# =====================================================
st.set_page_config(
    page_title="Dashboard Survei Pendidikan Fisika",
    layout="wide"
)

st.title("📊 Dashboard Survei Pendidikan Fisika")
st.markdown("Visualisasi Data 100 Responden")

# =====================================================
# LOAD DATA
# =====================================================
df = pd.read_csv("survey_pendidikan_fisika.csv")

# =====================================================
# SIDEBAR FILTER
# =====================================================
st.sidebar.header("🔎 Filter Data")

jk_filter = st.sidebar.multiselect(
    "Jenis Kelamin",
    options=df["JK"].unique(),
    default=df["JK"].unique()
)

pendidikan_filter = st.sidebar.multiselect(
    "Pendidikan",
    options=df["Pendidikan"].unique(),
    default=df["Pendidikan"].unique()
)

metode_filter = st.sidebar.multiselect(
    "Metode Pembelajaran",
    options=df["Metode"].unique(),
    default=df["Metode"].unique()
)

df = df[
    (df["JK"].isin(jk_filter)) &
    (df["Pendidikan"].isin(pendidikan_filter)) &
    (df["Metode"].isin(metode_filter))
]

# =====================================================
# RINGKASAN STATISTIK
# =====================================================
st.subheader("📌 Ringkasan Statistik")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Jumlah Responden", len(df))
col2.metric("Rata-rata Nilai", round(df["Nilai"].mean(), 2))
col3.metric("Rata-rata Minat", round(df["Minat"].mean(), 2))
col4.metric("Rata-rata Jam Belajar", round(df["Jam_Belajar"].mean(), 2))

# =====================================================
# TABEL DATA
# =====================================================
st.subheader("📄 Data Responden")
st.dataframe(df, use_container_width=True)

# =====================================================
# GRAFIK 1: MINAT VS NILAI
# =====================================================
st.subheader("📈 Hubungan Minat dan Nilai")

fig1 = px.scatter(
    df,
    x="Minat",
    y="Nilai",
    color="JK",
    trendline="ols",
    title="Minat vs Nilai UAS"
)

st.plotly_chart(fig1, use_container_width=True)

# =====================================================
# GRAFIK 2: JAM BELAJAR VS NILAI
# =====================================================
st.subheader("📉 Jam Belajar vs Nilai")

fig2 = px.scatter(
    df,
    x="Jam_Belajar",
    y="Nilai",
    color="Pendidikan",
    trendline="ols",
    title="Jam Belajar vs Nilai"
)

st.plotly_chart(fig2, use_container_width=True)

# =====================================================
# GRAFIK 3: DISTRIBUSI METODE FAVORIT
# =====================================================
st.subheader("📊 Distribusi Metode Pembelajaran Favorit")

fig3 = px.histogram(
    df,
    x="Metode",
    color="Metode",
    title="Distribusi Metode Favorit"
)

st.plotly_chart(fig3, use_container_width=True)

# =====================================================
# ANALISIS KORELASI
# =====================================================
st.subheader("📌 Analisis Korelasi")

corr_minat = np.corrcoef(df["Minat"], df["Nilai"])[0,1]
corr_jam = np.corrcoef(df["Jam_Belajar"], df["Nilai"])[0,1]

st.write(f"Korelasi Minat dan Nilai: **{round(corr_minat,3)}**")
st.write(f"Korelasi Jam Belajar dan Nilai: **{round(corr_jam,3)}**")

# =====================================================
# HEATMAP KORELASI
# =====================================================
st.subheader("🔥 Heatmap Korelasi")

numeric_df = df[["Minat", "Kesulitan", "Jam_Belajar", "Nilai"]]
corr_matrix = numeric_df.corr()

fig4 = px.imshow(
    corr_matrix,
    text_auto=True,
    title="Matriks Korelasi"
)

st.plotly_chart(fig4, use_container_width=True)

# =====================================================
# DOWNLOAD DATA
# =====================================================
st.subheader("⬇ Download Data")

csv = df.to_csv(index=False).encode('utf-8')
st.download_button(
    label="Download Data CSV",
    data=csv,
    file_name="hasil_filter_survei.csv",
    mime="text/csv"
)