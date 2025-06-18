# app.py
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

st.set_page_config(page_title="Monitoring Deposito", layout="wide")
st.title("📊 Dashboard Monitoring Deposito Bulanan")

data_file = st.file_uploader("📂 Upload file Excel", type=[".xlsx", ".xls"])

if data_file:
    try:
        df = pd.read_excel(data_file)

        expected_columns = {'Tanggal', 'Bank', 'Nominal', 'Bunga'}
        if not expected_columns.issubset(set(df.columns)):
            st.error(f"File harus memiliki kolom: {expected_columns}")
        else:
            df['Tanggal'] = pd.to_datetime(df['Tanggal'])
            df['Bulan'] = df['Tanggal'].dt.to_period('M').astype(str)

            buku_iv = ["Bank BRI", "Bank Mandiri", "Bank BNI"]
            buku_iii = ["Bank BTN", "BSI", "BTN Syariah"]

            col1, col2 = st.columns(2)

            with col1:
                st.subheader("📈 Total Bunga Deposito per Bulan")
                bunga_bulanan = df.groupby('Bulan')['Bunga'].sum()
                fig1, ax1 = plt.subplots()
                bunga_bulanan.plot(kind='line', marker='o', ax=ax1)
                ax1.set_ylabel("Total Bunga")
                ax1.set_xlabel("Bulan")
                ax1.grid(True)
                st.pyplot(fig1)

            with col2:
                st.subheader("📊 Total Deposito per Bulan")
                deposito_bulanan = df.groupby('Bulan')['Nominal'].sum()
                fig2, ax2 = plt.subplots()
                deposito_bulanan.plot(kind='bar', ax=ax2)
                ax2.set_ylabel("Total Deposito")
                ax2.set_xlabel("Bulan")
                ax2.grid(axis='y')
                st.pyplot(fig2)

            st.subheader("🧾 Distribusi Deposito per Bank")
            deposito_bank = df.groupby('Bank')['Nominal'].sum()
            fig3, ax3 = plt.subplots()
            deposito_bank.plot(kind='pie', autopct='%1.1f%%', ax=ax3)
            ax3.set_ylabel("")
            ax3.set_title("Total Deposito per Bank")
            st.pyplot(fig3)

            col3, col4 = st.columns(2)

            with col3:
                st.subheader("📘 Bunga Bulanan - Buku IV")
                df_buku_iv = df[df['Bank'].isin(buku_iv)]
                bunga_buku_iv = df_buku_iv.groupby('Bulan')['Bunga'].sum()
                fig4, ax4 = plt.subplots()
                bunga_buku_iv.plot(kind='line', marker='o', ax=ax4)
                ax4.set_ylabel("Bunga Buku IV")
                ax4.set_xlabel("Bulan")
                ax4.grid(True)
                st.pyplot(fig4)

            with col4:
                st.subheader("📙 Bunga Bulanan - Buku III")
                df_buku_iii = df[df['Bank'].isin(buku_iii)]
                bunga_buku_iii = df_buku_iii.groupby('Bulan')['Bunga'].sum()
                fig5, ax5 = plt.subplots()
                bunga_buku_iii.plot(kind='line', marker='o', ax=ax5)
                ax5.set_ylabel("Bunga Buku III")
                ax5.set_xlabel("Bulan")
                ax5.grid(True)
                st.pyplot(fig5)

            st.subheader("📋 Tabel Ringkasan Data")
            st.dataframe(df)

    except Exception as e:
        st.error(f"Gagal membaca file: {e}")
else:
    st.info("Silakan upload file Excel yang berisi data deposito.")
