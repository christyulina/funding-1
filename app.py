import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

st.set_page_config(page_title="Monitoring Deposito", layout="wide")
st.title("📊 Dashboard Monitoring Deposito Bulanan")

bulan_dict = {
    '01': 'Januari', '02': 'Februari', '03': 'Maret', '04': 'April',
    '05': 'Mei', '06': 'Juni', '07': 'Juli', '08': 'Agustus',
    '09': 'September', '10': 'Oktober', '11': 'November', '12': 'Desember'
}

data_file = st.file_uploader("📂 Upload file Excel", type=[".xlsx", ".xls"])

if data_file:
    try:
        df = pd.read_excel(data_file)

        expected_columns = {'Tanggal', 'Bank', 'Nominal', 'Bunga'}
        if not expected_columns.issubset(set(df.columns)):
            st.error(f"File harus memiliki kolom: {expected_columns}")
        else:
            df['Tanggal'] = pd.to_datetime(df['Tanggal'])
            df['Bulan'] = df['Tanggal'].dt.month.astype(str).str.zfill(2)
            df['Tahun'] = df['Tanggal'].dt.year.astype(str)
            df['BulanTahun'] = df['Bulan'] + '-' + df['Tahun']
            df['BulanTahun'] = df['BulanTahun'].apply(lambda x: f"{bulan_dict[x[:2]]} {x[3:]}")

            df['Nominal'] = df['Nominal'] / 1_000_000  # dalam jutaan
            df['Bunga'] = df['Bunga'] / 1_000_000  # dalam jutaan

            buku_iv = ["Bank BRI", "Bank Mandiri", "Bank BNI"]
            buku_iii = ["Bank BTN", "BSI", "BTN Syariah"]

            col1, col2 = st.columns(2)

            with col1:
                st.subheader("📈 Total Bunga Deposito per Bulan (Jutaan Rp)")
                bunga_bulanan = df.groupby('BulanTahun')['Bunga'].sum()
                fig1, ax1 = plt.subplots()
                bunga_bulanan.plot(kind='line', marker='o', ax=ax1)
                for i, v in enumerate(bunga_bulanan):
                    ax1.text(i, v, f"{v:.2f}", ha='center', va='bottom')
                ax1.set_ylabel("Total Bunga (Jutaan)")
                ax1.set_xlabel("Bulan")
                ax1.grid(True)
                st.pyplot(fig1)

            with col2:
                st.subheader("📊 Total Deposito per Bulan (Jutaan Rp)")
                deposito_bulanan = df.groupby('BulanTahun')['Nominal'].sum()
                fig2, ax2 = plt.subplots()
                deposito_bulanan.plot(kind='bar', ax=ax2)
                for i, v in enumerate(deposito_bulanan):
                    ax2.text(i, v, f"{v:.2f}", ha='center', va='bottom')
                ax2.set_ylabel("Total Deposito (Jutaan)")
                ax2.set_xlabel("Bulan")
                ax2.grid(axis='y')
                st.pyplot(fig2)

            st.subheader("🏦 Total Deposito per Bank (Jutaan Rp)")
            deposito_bank = df.groupby('Bank')['Nominal'].sum()
            fig3, ax3 = plt.subplots()
            deposito_bank.plot(kind='bar', ax=ax3)
            for i, v in enumerate(deposito_bank):
                ax3.text(i, v, f"{v:.2f}", ha='center', va='bottom')
            ax3.set_ylabel("Total Deposito (Jutaan)")
            ax3.set_xlabel("Bank")
            ax3.set_title("Deposito per Bank")
            ax3.grid(axis='y')
            st.pyplot(fig3)

            col3, col4 = st.columns(2)

            with col3:
                st.subheader("📘 Bunga Bulanan - Buku IV (Jutaan Rp)")
                df_buku_iv = df[df['Bank'].isin(buku_iv)]
                bunga_buku_iv = df_buku_iv.groupby('BulanTahun')['Bunga'].sum()
                fig4, ax4 = plt.subplots()
                bunga_buku_iv.plot(kind='line', marker='o', ax=ax4)
                for i, v in enumerate(bunga_buku_iv):
                    ax4.text(i, v, f"{v:.2f}", ha='center', va='bottom')
                ax4.set_ylabel("Bunga Buku IV (Jutaan)")
                ax4.set_xlabel("Bulan")
                ax4.grid(True)
                st.pyplot(fig4)

            with col4:
                st.subheader("📙 Bunga Bulanan - Buku III (Jutaan Rp)")
                df_buku_iii = df[df['Bank'].isin(buku_iii)]
                bunga_buku_iii = df_buku_iii.groupby('BulanTahun')['Bunga'].sum()
                fig5, ax5 = plt.subplots()
                bunga_buku_iii.plot(kind='line', marker='o', ax=ax5)
                for i, v in enumerate(bunga_buku_iii):
                    ax5.text(i, v, f"{v:.2f}", ha='center', va='bottom')
                ax5.set_ylabel("Bunga Buku III (Jutaan)")
                ax5.set_xlabel("Bulan")
                ax5.grid(True)
                st.pyplot(fig5)

            st.subheader("📋 Tabel Ringkasan Data (Nominal & Bunga dalam Jutaan Rp)")
            st.dataframe(df)

    except Exception as e:
        st.error(f"Gagal membaca file: {e}")
else:
    st.info("Silakan upload file Excel yang berisi data deposito.")
