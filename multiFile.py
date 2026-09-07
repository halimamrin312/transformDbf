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

#  Upload File
uploaded_file = st.file_uploader("Choose a file",accept_multiple_files=True,type=".DBF")
fileList = {"nameFile" : [],"pathFile":[]}

# Check and View Single File

if uploaded_file is not None:
    for i in range(len(uploaded_file)):
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file[i].name)[1]) as tmp:
            tmp.write(uploaded_file[i].getvalue())
            tmp_path = tmp.name
            # st.write({"nameFile":uploaded_file[i].name,"pathFile":tmp_path})
            fileList['nameFile'].append(uploaded_file[i].name)
            fileList['pathFile'].append(tmp_path)
        # Pass tmp_path to any library that requires a file path

fileList = pd.DataFrame(fileList)

event = st.dataframe(
    fileList,
    key="data",
    on_select="rerun",
    selection_mode=["single-row"],
)

selectionFile = fileList.iloc[event.selection.rows]

if not selectionFile.empty:
    selectionPath = selectionFile.iloc[0]["pathFile"]
    selectionName = selectionFile.iloc[0]["nameFile"]
    dbf = DBF(selectionPath)
    dbf = pd.DataFrame(dbf)


    # Make Button
    if st.button('Tampilkan Data'):
        # Tampilkan Dataframe
        st.dataframe(dbf)

    if st.button('Submit Data yang dipilih'):
        # Insert TO Postgres
        st.write(f"Menginputkan data {selectionName} menggunakan engine {st.session_state.newEngine}")
        dbf.to_sql(name=selectionName,con=st.session_state.newEngine, if_exists='replace', index=False)

if st.button('Submit semua data'):
    # Insert TO Postgres
    # st.write(f"Menginputkan data {selectionName} menggunakan engine {st.session_state.newEngine}")
    
    # st.write(len(fileList))
    for index, row in fileList.iterrows():
        # st.write(index, row['nameFile'],row['pathFile'])
        selectionPath = row['pathFile']
        nameFile = row['nameFile']
        dbf = DBF(selectionPath)
        dbf = pd.DataFrame(dbf)
        dbf.to_sql(name=nameFile,con=st.session_state.newEngine, if_exists='replace', index=False)
