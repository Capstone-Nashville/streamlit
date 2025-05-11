import pandas as pd

def load_clean_data():
    df = pd.read_csv('Dashboard_Penjualan_Bonbon.csv')
    df["Tanggal Transaksi"] = pd.to_datetime(df["Tanggal Transaksi"])
    df["Waktu Transaksi"] = pd.to_datetime(df["Waktu Transaksi"], format='%H:%M:%S').dt.time
    return df


load_clean_data()