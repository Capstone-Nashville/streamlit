import pandas as pd

# function untuk laod data yang sudah dibersihkan dari csv
def load_clean_data():
    df = pd.read_csv('Dashboard_Penjualan_Bonbon.csv')
    df["Tanggal Transaksi"] = pd.to_datetime(df["Tanggal Transaksi"])
    df["Waktu Transaksi"] = pd.to_datetime(df["Waktu Transaksi"], format='%H:%M:%S').dt.time
    return df

# function untuk load data cluster
def load_cluster_data():
    df = pd.read_csv('Data Cluster Transaksi.csv')
    df['Outlet'].replace({'BONBON ICE CREAM CENDANA':' CENDANA SMD','BONBON ICE CREAM AWS':'BONBON AWS SMD',
                        'BONBON ICE CREAM CUT NYAK DIEN (TGR)':'BONBON CUT NYAK DIEN (TGR)','BONBON ICE CREAM BIG MALL':'BONBON BIG MALL SMD',
                        'BONBON ICE CREAM KAMPUNG BARU (TGR)':'BONBON KAMPUNG BARU (TGR)'}, inplace=True)
    return df

# function untuk load data pca dengan cluster
def load_pca_cluster_data():
    df = pd.read_csv('PCA with Cluster.csv')
    return df