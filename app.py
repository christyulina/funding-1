import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

st.set_page_config(page_title="Monitoring Deposito", layout="wide")
st.title("📊 Dashboard Monitoring Deposito Bulanan")

bulan_dict = {
    '01': 'Januari', '02': 'Februari', '03': 'Maret', '04': 'April',
    '05': 'Mei', '06': 'Juni', '07': 'Juli', '08': 'Agustus',
    '09': 'September', '10': 'Oktober', '11': 'November', '12': 'Desember'
}


def miliar_formatter(x, pos):
    return f'{x:,.1f}'

def with_all_checkbox(label, options, key):
    select_all = st.sidebar.checkbox(f"Pilih semua {label}", key=f"{key}_all")
    selected = st.sidebar.multiselect(f"Pilih {label}:", options=options, default=options if select_all else [], key=f"{key}_select")
    return selected

data_file = st.sidebar.file_uploader("📂 Upload file Excel", type=[".xlsx", ".xls"])

if data_file:
    try:
        df = pd.read_excel(data_file)

        expected_columns = {'Tanggal', 'Bank', 'Nominal', 'Bunga'}
        if not expected_columns.issubset(set(df.columns)):
            st.error(f"File harus memiliki kolom: {expected_columns}")
        else:
            df['Tanggal'] = pd.to_datetime(df['Tanggal'])
            df['Bank'] = df['Bank'].astype(str).str.strip().str.title()
            df['Bulan'] = df['Tanggal'].dt.month.astype(str).str.zfill(2)
            df['Tahun'] = df['Tanggal'].dt.year.astype(str)
            df['NamaBulan'] = df['Tanggal'].dt.month.astype(int).apply(lambda x: bulan_dict[str(x).zfill(2)])
            df['BulanTahun'] = df['NamaBulan'] + ' ' + df['Tahun']

            buku_iv = [b.title() for b in ["Bank BRI", "Bank Mandiri", "Bank BNI"]]
            buku_iii = [b.title() for b in ["Bank BTN", "BSI", "BTN Syariah"]]

            df['NominalM'] = df['Nominal'] / 1_000_000_000
            df['BungaM'] = df['Bunga'] / 1_000_000_000

            all_months = sorted(df['NamaBulan'].unique(), key=lambda x: list(bulan_dict.values()).index(x))
            all_years = sorted(df['Tahun'].unique())
            all_banks = sorted(df['Bank'].unique())

            selected_bulan = with_all_checkbox("Bulan", all_months, "global_bulan")
            selected_bank = with_all_checkbox("Bank", all_banks, "global_bank")
            selected_tahun = with_all_checkbox("Tahun", all_years, "global_tahun")

            df_filtered = df.copy()
            if selected_bulan:
                df_filtered = df_filtered[df_filtered['NamaBulan'].isin(selected_bulan)]
            if selected_bank:
                df_filtered = df_filtered[df_filtered['Bank'].isin(selected_bank)]
            if selected_tahun:
                df_filtered = df_filtered[df_filtered['Tahun'].isin(selected_tahun)]

            ordered_bulans = df_filtered[['NamaBulan', 'Tahun']].drop_duplicates()
            ordered_bulans['BulanTahun'] = ordered_bulans['NamaBulan'] + ' ' + ordered_bulans['Tahun']
            ordered_bulans['order'] = ordered_bulans['NamaBulan'].apply(lambda x: list(bulan_dict.values()).index(x))
            ordered_bulans = ordered_bulans.sort_values(['Tahun', 'order'])['BulanTahun'].tolist()

            df_filtered['BulanTahun'] = pd.Categorical(df_filtered['BulanTahun'], categories=ordered_bulans, ordered=True)

            st.subheader("📈 Total Bunga Deposito per Bulan (Miliar Rp)")
            bunga_bulanan = df_filtered.groupby('BulanTahun')['BungaM'].sum().sort_index()
            fig1, ax1 = plt.subplots()
            bunga_bulanan.plot(kind='line', marker='o', ax=ax1)
            ax1.yaxis.set_major_formatter(FuncFormatter(miliar_formatter))
            for i, v in enumerate(bunga_bulanan):
                ax1.text(i, v, f"{v:,.1f}", ha='center', va='bottom')
            ax1.set_ylabel("Total Bunga (Miliar Rp)")
            ax1.set_xlabel("Bulan")
            ax1.tick_params(axis='x', rotation=45)
            ax1.grid(True)
            st.pyplot(fig1)

            st.markdown("---")

            st.subheader("📊 Total Deposito per Bulan (Miliar Rp)")
            deposito_bulanan = df_filtered.groupby('BulanTahun')['NominalM'].sum().sort_index()
            fig2, ax2 = plt.subplots()
            deposito_bulanan.plot(kind='bar', ax=ax2)
            ax2.yaxis.set_major_formatter(FuncFormatter(miliar_formatter))
            for i, v in enumerate(deposito_bulanan):
                ax2.text(i, v, f"{v:,.1f}", ha='center', va='bottom')
            ax2.set_ylabel("Total Deposito (Miliar Rp)")
            ax2.set_xlabel("Bulan")
            ax2.tick_params(axis='x', rotation=45)
            ax2.grid(axis='y')
            st.pyplot(fig2)

            st.markdown("---")

            st.subheader("🥧 Total Deposito per Bank (dalam Miliar Rupiah)")
            deposito_bank = df_filtered.groupby('Bank')['NominalM'].sum()
            fig_pie, ax_pie = plt.subplots()
            deposito_bank.plot(kind='pie', ax=ax_pie, autopct=lambda pct: f'{pct:.1f}%\n({(pct/100)*deposito_bank.sum():.1f})', startangle=90)
            ax_pie.set_ylabel("")
            st.pyplot(fig_pie)

            st.markdown("---")

            st.subheader("📘 Bunga Bulanan Buku IV per Bank (dalam Miliar Rupiah)")
            df_buku_iv = df_filtered[df_filtered['Bank'].isin(buku_iv)]
            df_buku_iv_grouped = df_buku_iv.groupby(['BulanTahun', 'Bank'])['BungaM'].sum().unstack().reindex(index=ordered_bulans, columns=buku_iv)
            fig_iv, ax_iv = plt.subplots()
            df_buku_iv_grouped.plot(ax=ax_iv, marker='o')
            for bank in df_buku_iv_grouped.columns:
                for i, v in enumerate(df_buku_iv_grouped[bank]):
                    if not pd.isna(v):
                        ax_iv.text(i, v, f"{v:,.1f}", ha='center', va='bottom', fontsize=8)
            ax_iv.set_ylabel("Bunga (Miliar Rp)")
            ax_iv.set_xlabel("Bulan")
            ax_iv.yaxis.set_major_formatter(FuncFormatter(miliar_formatter))
            ax_iv.tick_params(axis='x', rotation=45)
            ax_iv.grid(True)
            st.pyplot(fig_iv)

            st.markdown("---")

            st.subheader("📙 Bunga Bulanan Buku III per Bank (dalam Miliar Rupiah)")
            df_buku_iii = df_filtered[df_filtered['Bank'].isin(buku_iii)]
            df_buku_iii_grouped = df_buku_iii.groupby(['BulanTahun', 'Bank'])['BungaM'].sum().unstack().reindex(index=ordered_bulans, columns=buku_iii)
            fig_iii, ax_iii = plt.subplots()
            df_buku_iii_grouped.plot(ax=ax_iii, marker='o')
            for bank in df_buku_iii_grouped.columns:
                for i, v in enumerate(df_buku_iii_grouped[bank]):
                    if not pd.isna(v):
                        ax_iii.text(i, v, f"{v:,.1f}", ha='center', va='bottom', fontsize=8)
            ax_iii.set_ylabel("Bunga (Miliar Rp)")
            ax_iii.set_xlabel("Bulan")
            ax_iii.yaxis.set_major_formatter(FuncFormatter(miliar_formatter))
            ax_iii.tick_params(axis='x', rotation=45)
            ax_iii.grid(True)
            st.pyplot(fig_iii)

    except Exception as e:
        st.error(f"Gagal membaca file: {e}")
else:
    st.info("Silakan upload file Excel yang berisi data deposito.")
