import streamlit as st
from streamlit_extras.metric_cards import style_metric_cards
from streamlit_option_menu import option_menu
import plotly.express as px
import pandas as pd
import numpy as np
import os
import warnings
import matplotlib.pyplot as plt
import seaborn as sns
import datetime as dt
from model import model as data
warnings.filterwarnings("ignore")

data_dashboard = data.load_clean_data()



def card_analytics(df):
    st.markdown(
        """
        <style>
        [data-testid="stMetricValue"] {
            font-size: 25px;
            font-weight: bold;
        }

        .erovr380 {
            color: #EC0A0B !important;
        }

        .stMultiSelect {
            color: #EC0A0B !important;
            border-radius: 10px;
            padding: 10px;
        }

        .erovr382 {
            background-color: #ffffff !important;
            border-radius: 10px;
            padding: 10px;
            color: #EC0A0B !important;
            border: 2px solid #EC0A0B !important;,
            border-color: #EC0A0B
        }

        .e1lln2w82 {
            background-color: #ffffff !important;
            border-radius: 10px;
            padding: 10px;
            color: #EC0A0B !important;
            border: 2px solid #EC0A0B !important;,
            border-color: #EC0A0B
        }

        .e14qm3312 {
            background-color: #ffffff !important;
            border-radius: 10px;
            color: #EC0A0B !important;
        }

        .e14qm3311 {
            background-color: #ffffff !important;
            border-radius: 10px;
            color: #EC0A0B !important;
        }

        .stAlertContainer {
            color: #ffffff !important;
            border-radius: 10px;
            padding: 10px;
        }

        """,
        unsafe_allow_html=True,
    )



     # Menambahkan opsi 'Pilih Semua' di bulan dan menjadikannya default
    bulan_tahun_options = df['Tanggal Transaksi'].dt.strftime('%B %Y').unique()
    bulan_tahun_options = ['All'] + list(bulan_tahun_options)  # Menambahkan 'All' sebagai pilihan pertama
    bulan_terpilih = st.multiselect('Pilih Bulan dan Tahun', bulan_tahun_options, default=['All'])  # Default 'All' dipilih

    # Jika 'All' dipilih, semua bulan dipilih
    if 'All' in bulan_terpilih:
        bulan_terpilih = bulan_tahun_options[1:]  # Menghapus 'All' jika dipilih

    # Filter data berdasarkan bulan yang dipilih
    df_bulan = df[df['Tanggal Transaksi'].dt.strftime('%B %Y').isin(bulan_terpilih)]

    if not bulan_terpilih:
        st.warning("Silakan pilih minimal satu bulan untuk melihat data.")
        return 

    total_penjualan = df_bulan["Sub Total"].sum()
    total_penjualan_item = df_bulan["Quantity"].sum()
    formatted_penjualan_item = f"{total_penjualan_item:,}".replace(",", ".")

    produk_terlaris = df_bulan.groupby('Nama Produk')['Quantity'].sum()
    produk_terlaris_nama = produk_terlaris.idxmax()  # Nama produk terlaris
    produk_terlaris_kuantitas = produk_terlaris.max()  # Kuantitas produk terlaris
    formatted_kuantitas_produk = f"{produk_terlaris_kuantitas:,}".replace(",", ".")

    outlet_terlaris = df_bulan.groupby('Outlet')['Sub Total'].sum()
    outlet_terlaris_nama = outlet_terlaris.idxmax()  # Nama outlet terlaris
    outlet_terlaris_penjualan = outlet_terlaris.max()  # Total penjualan outlet terlaris

    col1, col2, col3 = st.columns(3)
    with col1:
        st.subheader('Total Penjualan')
        st.metric("Total", f"Rp {total_penjualan:,}".replace(",", "."), delta_color="off")
        st.metric("Total Penjualan Item", f"{formatted_penjualan_item} item", delta_color="off")

    with col2:
        st.subheader('Produk Terlaris')
        st.metric("Produk", f"{produk_terlaris_nama}", delta_color="off")
        st.metric("Terjual", f"{formatted_kuantitas_produk} item", delta_color="off")

    with col3:
        st.subheader('Outlet Terlaris')
        st.metric("Outlet", f"{outlet_terlaris_nama}", delta_color="off")
        st.metric("Pendapatan", f"Rp {outlet_terlaris_penjualan:,}".replace(",", "."), delta_color="off")


def comparison(df):
    st.subheader("Diagram Line Chart Penjualan Bonbon Ice Cream per Bulan (2023)")
    st.markdown("\n")

    # Mengonversi kolom 'Tanggal Transaksi' menjadi datetime
    df['Tanggal Transaksi'] = pd.to_datetime(df['Tanggal Transaksi'])

    # Mengelompokkan berdasarkan bulan dan menghitung jumlah penjualan per bulan
    total_penjualan_per_bulan = df.groupby(df['Tanggal Transaksi'].dt.strftime('%B %Y'))['Sub Total'].sum().reset_index(name='Total Pendapatan')

    # Urutan bulan yang benar (Mei 2024 sampai April 2025)
    bulan_urutan = ['May 2024', 'June 2024', 'July 2024', 'August 2024', 'September 2024', 'October 2024',
                    'November 2024', 'December 2024', 'January 2025', 'February 2025', 'March 2025', 'April 2025']

    # Mengubah kolom 'Tanggal Transaksi' menjadi kategori dengan urutan bulan yang benar
    total_penjualan_per_bulan['Tanggal Transaksi'] = pd.Categorical(total_penjualan_per_bulan['Tanggal Transaksi'],
                                                        categories=bulan_urutan, ordered=True)
    total_penjualan_per_bulan = total_penjualan_per_bulan.sort_values('Tanggal Transaksi')

    # Membuat line chart
    fig_line = px.line(total_penjualan_per_bulan, x='Tanggal Transaksi', y='Total Pendapatan')
    fig_line.update_xaxes(title='Bulan')
    fig_line.update_yaxes(title='Total Pendapatan')
    fig_line.update_layout(
        plot_bgcolor='#ffffff',  
        paper_bgcolor='#ffffff',  # Warna font
        margin=dict(t=30, b=30, l=30, r=30),  # Menambahkan margin agar grafik tidak terlalu rapat
        font=dict(color="red")
    )
    fig_line.update_traces(line=dict(color='#FDD776', width=3))  # Mengubah warna garis menjadi merah
        # Mengubah label sumbu X dan Y
    fig_line.update_xaxes(
        title='Bulan',  # Mengubah label sumbu X
        title_font=dict(size=14, color='#EC0A0B'),  # Mengubah font dan warna label X
        tickmode='array',  # Mengatur mode tick untuk menampilkan bulan dalam urutan yang benar
        tickfont=dict(color='#EC0A0B')
    )
    fig_line.update_yaxes(
        title='Total Pendapatan',  # Mengubah label sumbu Y
        title_font=dict(size=14, color='#EC0A0B'),  # Mengubah font dan warna label Y
        tickfont=dict(color='#EC0A0B')  # Mengubah warna angka di sumbu Y menjadi merah
    )

    # Menampilkan grafik
    st.plotly_chart(fig_line, use_container_width=True, style={'border': '1px solid black'})

    st.markdown("---")

    st.subheader("Perbandingan Penjualan")
    st.markdown("\n")
    jumlah_penjualan = df.groupby('Nama Produk')['Sub Total'].sum().reset_index()
    jumlah_penjualan = jumlah_penjualan.head().sort_values('Sub Total', ascending=True)
    jumlah_penjualan.columns = ['Nama Produk', 'Sub Total']
    fig_nama_produk  = px.bar(jumlah_penjualan, y='Nama Produk', x='Sub Total',
                            orientation='h', title='Total Penjualan berdasarkan Nama Produk')
    fig_nama_produk.update_xaxes(title='Sub Total')
    fig_nama_produk.update_yaxes(title='Nama Produk')
    st.plotly_chart(fig_nama_produk, use_container_width=True, style={'border': '1px solid black'})


def relation(df):
    print("Relation")

def composition(df):
    print("Compotition")

def distribution(df):
    print("Distribution")

def main():
    st.title("Dashboard Penjualan Bonbon Ice Cream 🍦")

    card_analytics(data_dashboard)

    chart_type = st.selectbox("Pilih Jenis Grafik yang Ingin Ditampilkan", ["Comparison", "Relation", "Composition", "Distribution"])

    if chart_type == "Comparison":
        comparison(data_dashboard)



if __name__ == "__main__":
    main()