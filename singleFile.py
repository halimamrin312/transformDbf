import streamlit as st
import pandas as pd
from dbfread import DBF
from io import StringIO
import sqlalchemy as db
import tempfile
import os

# Atribut Connection Postgress
username = "postgres";
password = 12345;
host = "localhost:5432"
dbDefault = "DbTest";

def connectDatabase(username,password,host,dbName):
    engine = db.create_engine(f'postgresql://{username}:{password}@{host}/{dbName}')
    return engine

# Connection Postgress
engine = connectDatabase(username,password,host,dbDefault)
with engine.connect() as conn:
    st.write(f"berhasil terhubung dengan database - {dbDefault}")

# Get Database List
query = db.text("SELECT datname FROM pg_database WHERE datistemplate = false;")
result = engine.connect().execute(query)
databases = [row[0] for row in result]
st.write(databases)

#  Pilih Databases
dbName = st.selectbox("Pilih Database",databases)
st.write(dbName)

# Ganti Databases
if st.button('Ganti Database'):
    # Inisialisasi State Nama Engine
    if 'newEngine' not in st.session_state:
        # Koneksi dengan engine baru 
        st.session_state.newEngine = connectDatabase(username,password,host,dbName)
    # test Koneksi dengan engine baru   
    with st.session_state.newEngine.connect() as conn:
        st.write(f"berhasil terhubung dengan database - {dbName}")

# Upload FIle
uploaded_file = st.file_uploader("Choose a file",type=[".DBF",".xlsx"])
# Cek Upload File
if uploaded_file is not None:
    # namaFile = uploaded_file.name
    with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as tmp:
        tmp.write(uploaded_file.getvalue())
        tmp_path = tmp.name
    dbf = DBF(tmp_path)
    dbf = pd.DataFrame(dbf)

    st.dataframe(dbf)

# Input Nama Table
namaFile = uploaded_file.name.rsplit(".", 1)[0] 
namaTable = st.text_input("Input Nama Table",namaFile)
st.write(len(namaTable))

if len(namaTable) == 0:
    disableButton = True
else:
    disableButton = False

# Make Button
if st.button('Submit Data', disabled = disableButton):
    # Insert TO Postgres
    dbf.to_sql(name=namaTable,con=st.session_state.newEngine, if_exists='replace', index=False)