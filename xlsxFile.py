import streamlit as st
import pandas as pd
import sqlalchemy as db
import tempfile
import os
from dotenv import load_dotenv

# Load the environment variables from the .env file
load_dotenv()

# Atribut Connection Postgres
username = os.getenv("DB_USERNAME")
password = os.getenv("DB_PASSWORD")
host = os.getenv("DB_HOST")
dbDefault = os.getenv("DB_DATABASE")

@st.cache_resource
def connectDatabase(username, password, host, dbName):
    engine = db.create_engine(f'postgresql://{username}:{password}@{host}/{dbName}')
    return engine

# Connection Postgres
engine = connectDatabase(username, password, host, dbDefault)
with engine.connect() as conn:
    st.write(f"berhasil terhubung dengan database - {dbDefault}")

# Get Database List
query = db.text("SELECT datname FROM pg_database WHERE datistemplate = false;")
result = engine.connect().execute(query)
databases = [row[0] for row in result]

# Pilih Database
dbName = st.selectbox("Pilih Database", databases)
st.write(dbName)

# Ganti Database
if st.button('Ganti Database'):
    st.session_state.newEngine = connectDatabase(username, password, host, dbName)
    with st.session_state.newEngine.connect() as conn:
        st.write(f"berhasil terhubung dengan database - {dbName}")

# Upload File (single atau multiple)
uploaded_files = st.file_uploader("Choose a file", accept_multiple_files=True, type=[".xlsx"])

if uploaded_files:
    # Simpan semua file ke temp path
    fileList = {"nameFile": [], "pathFile": [], "sheets": []}
    for f in uploaded_files:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx") as tmp:
            tmp.write(f.getvalue())
            tmp_path = tmp.name
        # Baca nama sheet yang tersedia
        xl = pd.ExcelFile(tmp_path)
        fileList['nameFile'].append(f.name.rsplit(".", 1)[0])
        fileList['pathFile'].append(tmp_path)
        fileList['sheets'].append(xl.sheet_names)

    fileList = pd.DataFrame(fileList)

    # Jika hanya 1 file
    if len(fileList) == 1:
        selectionPath = fileList.iloc[0]["pathFile"]
        selectionName = fileList.iloc[0]["nameFile"]
        sheetNames = fileList.iloc[0]["sheets"]

        # Pilih sheet
        selectedSheet = st.selectbox("Pilih Sheet", sheetNames)
        df = pd.read_excel(selectionPath, sheet_name=selectedSheet)
        st.dataframe(df)

        namaTable = st.text_input("Input Nama Table", f"{selectionName}_{selectedSheet}")
        disableButton = len(namaTable) == 0

        if st.button('Submit Data', disabled=disableButton):
            if 'newEngine' not in st.session_state:
                st.warning("Silahkan pilih database terlebih dahulu.")
            else:
                df.to_sql(name=namaTable, con=st.session_state.newEngine, if_exists='replace', index=False)
                st.success(f"Data '{namaTable}' berhasil diinputkan.")

    # Jika lebih dari 1 file
    else:
        # Tampilkan tabel file (tanpa kolom sheets)
        event = st.dataframe(
            fileList[["nameFile", "pathFile"]],
            key="data",
            on_select="rerun",
            selection_mode=["single-row"],
        )

        selectionFile = fileList.iloc[event.selection.rows]

        if not selectionFile.empty:
            selectionPath = selectionFile.iloc[0]["pathFile"]
            selectionName = selectionFile.iloc[0]["nameFile"]
            sheetNames = selectionFile.iloc[0]["sheets"]

            # Pilih sheet dari file yang dipilih
            selectedSheet = st.selectbox("Pilih Sheet", sheetNames)
            df = pd.read_excel(selectionPath, sheet_name=selectedSheet)

            if st.button('Tampilkan Data'):
                st.dataframe(df)

            if st.button('Submit Data yang dipilih'):
                if 'newEngine' not in st.session_state:
                    st.warning("Silahkan pilih database terlebih dahulu.")
                else:
                    namaTable = f"{selectionName}_{selectedSheet}"
                    df.to_sql(name=namaTable, con=st.session_state.newEngine, if_exists='replace', index=False)
                    st.success(f"Data '{namaTable}' berhasil diinputkan.")

        if st.button('Submit semua data (sheet pertama tiap file)'):
            if 'newEngine' not in st.session_state:
                st.warning("Silahkan pilih database terlebih dahulu.")
            else:
                for _, row in fileList.iterrows():
                    first_sheet = row['sheets'][0]
                    df = pd.read_excel(row['pathFile'], sheet_name=first_sheet)
                    namaTable = f"{row['nameFile']}_{first_sheet}"
                    df.to_sql(name=namaTable, con=st.session_state.newEngine, if_exists='replace', index=False)
                st.success(f"{len(fileList)} file berhasil diinputkan.")
