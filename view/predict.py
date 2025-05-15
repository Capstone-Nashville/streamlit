import streamlit as st
from streamlit_option_menu import option_menu
import plotly.express as px
import pandas as pd
import warnings
from model import model as data
warnings.filterwarnings("ignore")

data_cluster = data.load_cluster_data()
data_pca = data.load_pca_cluster_data()



def cluster_card(df):
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
            border: 4px solid #EC0A0B !important;,
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

    cluster0 = df[df['Clusters'] == 0]
    jumlah_cluster0 = cluster0['Clusters'].count()
    cluster1 = df[df['Clusters'] == 1]
    jumlah_cluster1 = cluster1['Clusters'].count()
    cluster2 = df[df['Clusters'] == 2]
    jumlah_cluster2 = cluster2['Clusters'].count()
    cluster3 = df[df['Clusters'] == 3]
    jumlah_cluster3 = cluster3['Clusters'].count()

    st.subheader('Informasi singkat per Kluster')
    st.markdown('\n')
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.subheader('Cluster 0')
        st.metric("Jumlah Transaksi dalam cluster 0", jumlah_cluster0, delta_color="off")
        st.metric("Top Outlet dalam cluster 0", cluster0['Outlet'].mode()[0], delta_color="off")

    with col2:
        st.subheader('Cluster 1')
        st.metric("Jumlah Transaksi dalam cluster 1", jumlah_cluster1, delta_color="off")
        st.metric("Top Outlet dalam cluster 1", cluster1['Outlet'].mode()[0], delta_color="off")

    with col3:
        st.subheader('Cluster 2')
        st.metric("Jumlah Transaksi dalam cluster 2", jumlah_cluster2, delta_color="off")
        st.metric("Top Outlet dalam cluster 2", cluster2['Outlet'].mode()[0], delta_color="off")

    with col4:
        st.subheader('Cluster 3')
        st.metric("Jumlah Transaksi dalam cluster 3", jumlah_cluster3, delta_color="off")
        st.metric("Top Outlet dalam cluster 3", cluster3['Outlet'].mode()[0], delta_color="off")

def plot_cluster(df):
    st.subheader("Persebaran Data Setiap Cluster")
    fig = px.scatter(df, x='PCA 1', y='PCA 2', color='Clusters',
                    color_continuous_scale=px.colors.qualitative.Set1)
    st.plotly_chart(fig, use_container_width=True, style={'border': '1px solid black'})

def cluster_comparison(df):
    st.subheader("Perbandingan Jumlah Cluster Setiap Outlet")
    frekuensi_model = df.groupby(['Outlet', 'Clusters']).size().reset_index(name='frekuensi')
    sorting_frekuensi = frekuensi_model.sort_values(by='frekuensi', ascending=False)
    fig = px.bar(sorting_frekuensi, x='Outlet', y='frekuensi', color='Clusters',
                color_continuous_scale=px.colors.qualitative.Set1)
    st.plotly_chart(fig, use_container_width=True, style={'border': '1px solid black'})
    
    st.markdown('\n')
    st.subheader("Statistik Tiap Cluster")
    st.markdown('\n')
    avg_per_cluster = df.groupby('Clusters')['Avg_Harga'].mean().reset_index()
    # Membuat bar chart
    fig_harga = px.bar(avg_per_cluster, x='Clusters', y='Avg_Harga',
                labels={'Avg_Harga': 'Rata-rata Total Harga yang dibeli', 'Clusters': 'Cluster'},
                title='Rata-rata Total Harga yang Dibeli per Cluster')
    st.plotly_chart(fig_harga, use_container_width=True)
    st.markdown('\n')
    col1, col2 = st.columns(2)
    with col1:
        avg_per_cluster = df.groupby('Clusters')['Total_Pembelian'].mean().reset_index()
        # Membuat bar chart
        fig_pembelian = px.bar(avg_per_cluster, x='Clusters', y='Total_Pembelian',
                    labels={'Total_Pembelian': 'Rata-rata Total Pembelian', 'Clusters': 'Cluster'},
                    title='Rata-rata Total Pembelian per Cluster')

        st.plotly_chart(fig_pembelian, use_container_width=True)
    with col2:
        avg_per_cluster = df.groupby('Clusters')['Total_Quantity'].mean().reset_index()
        # Membuat bar chart
        fig_kuantitas = px.bar(avg_per_cluster, x='Clusters', y='Total_Quantity',
                    labels={'Total_Quantity': 'Rata-rata Total Item yang dibeli', 'Clusters': 'Cluster'},
                    title='Rata-rata Total Item yang dibeli per Cluster')

        st.plotly_chart(fig_kuantitas, use_container_width=True)
    st.markdown('\n')
    col3, col4 = st.columns(2)
    with col3:
        avg_per_cluster = df.groupby('Clusters')['Produk_Unik'].mean().reset_index()
        # Membuat bar chart
        fig = px.bar(avg_per_cluster, x='Clusters', y='Produk_Unik',
                    labels={'Produk_Unik': 'Rata-rata Total Produk yang dibeli', 'Clusters': 'Cluster'},
                    title='Rata-rata Total Pembelian per Cluster')
        st.plotly_chart(fig, use_container_width=True)
    with col4:
        avg_per_cluster = df.groupby('Clusters')['Kategori_Unik'].mean().reset_index()
        # Membuat bar chart
        fig = px.bar(avg_per_cluster, x='Clusters', y='Kategori_Unik',
                    labels={'Kategori_Unik': 'Rata-rata Total Kategori yang dibeli', 'Clusters': 'Cluster'},
                    title='Rata-rata Total Kategori yang dibeli per Cluster')
        st.plotly_chart(fig, use_container_width=True)
    st.markdown("---")

def main():
    st.markdown(
        """
        <style>
        [data-testid="stMetricValue"] {
            font-size: 25px;
            font-weight: bold;
        }

        .e1kosxz23 {
            color: #FFFFFFFF !important;
        }
        """,
        unsafe_allow_html=True,
    )
    st.title("Clustering :mag:")
    st.markdown("\n")
    with st.expander("Lihat Dataset"):
        st.dataframe(data_cluster)
    st.markdown("\n")
    plot_cluster(data_pca)
    cluster_card(data_cluster)
    cluster_comparison(data_cluster)