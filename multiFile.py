import streamlit as st
import pandas as pd
from dbfread import DBF
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
uploaded_files = st.file_uploader("Choose a file", accept_multiple_files=True, type=[".DBF"])

if uploaded_files:
    # Simpan semua file ke temp path
    fileList = {"nameFile": [], "pathFile": []}
    for f in uploaded_files:
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(f.name)[1]) as tmp:
            tmp.write(f.getvalue())
            fileList['nameFile'].append(f.name.rsplit(".", 1)[0])
            fileList['pathFile'].append(tmp.name)
    fileList = pd.DataFrame(fileList)

    # Jika hanya 1 file, langsung tampilkan tanpa perlu pilih dari tabel
    if len(fileList) == 1:
        selectionPath = fileList.iloc[0]["pathFile"]
        selectionName = fileList.iloc[0]["nameFile"]
        dbf = pd.DataFrame(DBF(selectionPath))
        st.dataframe(dbf)

        namaTable = st.text_input("Input Nama Table", selectionName)
        disableButton = len(namaTable) == 0

        if st.button('Submit Data', disabled=disableButton):
            if 'newEngine' not in st.session_state:
                st.warning("Silahkan pilih database terlebih dahulu.")
            else:
                dbf.to_sql(name=namaTable, con=st.session_state.newEngine, if_exists='replace', index=False)
                st.success(f"Data '{namaTable}' berhasil diinputkan.")

    # Jika lebih dari 1 file, tampilkan tabel seleksi
    else:
        event = st.dataframe(
            fileList,
            key="data",
            on_select="rerun",
            selection_mode=["single-row"],
        )

        selectionFile = fileList.iloc[event.selection.rows]

        # Tampilkan preview file yang dipilih
        if not selectionFile.empty:
            selectionPath = selectionFile.iloc[0]["pathFile"]
            selectionName = selectionFile.iloc[0]["nameFile"]
            dbf = pd.DataFrame(DBF(selectionPath))

            if st.button('Tampilkan Data'):
                st.dataframe(dbf)

            if st.button('Submit Data yang dipilih'):
                if 'newEngine' not in st.session_state:
                    st.warning("Silahkan pilih database terlebih dahulu.")
                else:
                    dbf.to_sql(name=selectionName, con=st.session_state.newEngine, if_exists='replace', index=False)
                    st.success(f"Data '{selectionName}' berhasil diinputkan.")

        if st.button('Submit semua data'):
            if 'newEngine' not in st.session_state:
                st.warning("Silahkan pilih database terlebih dahulu.")
            else:
                for _, row in fileList.iterrows():
                    dbf = pd.DataFrame(DBF(row['pathFile']))
                    dbf.to_sql(name=row['nameFile'], con=st.session_state.newEngine, if_exists='replace', index=False)
                st.success(f"{len(fileList)} file berhasil diinputkan.")
