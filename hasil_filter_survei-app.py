import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Dashboard Survei Pendidikan Fisika", layout="wide")

st.title("📊 Dashboard Survei Pendidikan Fisika")
st.subheader("Visualisasi Data 100 Responden")

# =====================================================
# LOAD DATA (HEADER ADA DI BARIS KE-3 EXCEL)
# =====================================================
df = pd.read_excel("survei_pendidikan_fisika.xlsx", header=2)

# Bersihkan nama kolom dari spasi tersembunyi
df.columns = df.columns.str.strip()

# DEBUG (boleh dihapus kalau sudah normal)
st.write("Kolom terbaca:", df.columns)

# =====================================================
# SIDEBAR FILTER
# =====================================================
st.sidebar.header("Filter Data")

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
# METRIC
# =====================================================
col1, col2, col3 = st.columns(3)

col1.metric("Jumlah Responden", len(df_filtered))
col2.metric("Rata-rata Nilai", round(df_filtered["Nilai"].mean(), 2))
col3.metric("Rata-rata Minat", round(df_filtered["Minat"].mean(), 2))

st.divider()

# =====================================================
# VISUALISASI
# =====================================================

# Grafik Jenis Kelamin
fig_jk = px.histogram(df_filtered, x="JK", title="Distribusi Jenis Kelamin")
st.plotly_chart(fig_jk, use_container_width=True)

# Grafik Pendidikan
fig_pendidikan = px.histogram(df_filtered, x="Pendidikan", title="Distribusi Pendidikan")
st.plotly_chart(fig_pendidikan, use_container_width=True)

# Grafik Nilai berdasarkan Metode
fig_metode = px.box(
    df_filtered,
    x="Metode",
    y="Nilai",
    title="Perbandingan Nilai Berdasarkan Metode Pembelajaran"
)
st.plotly_chart(fig_metode, use_container_width=True)

# Scatter Minat vs Nilai
fig_scatter = px.scatter(
    df_filtered,
    x="Minat",
    y="Nilai",
    color="JK",
    title="Hubungan Minat dengan Nilai"
)
st.plotly_chart(fig_scatter, use_container_width=True)
