from sqlalchemy import create_engine
from sqlalchemy.sql import text
from dotenv import load_dotenv
import os
import streamlit as st
import pandas as pd

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


df = pd.read_csv("Data Science - MetadaDatabase.csv")
st.dataframe(df)

if st.button('Buat Database'):
    with engine.connect() as conn:
    # Memastikan eksekusi tidak berada dalam transaksi (autocommit mode)
        conn = conn.execution_options(isolation_level="AUTOCOMMIT")
        for index,row in df.iterrows():
            conn.execute(text(f'CREATE DATABASE "{row['Nama Sekarang']}";'))
            st.write(f"Database {row['Nama Sekarang']} berhasil dibuat!")

if st.button('HAPUS Database'):
    with engine.connect() as conn:
    # Memastikan eksekusi tidak berada dalam transaksi (autocommit mode)
        conn = conn.execution_options(isolation_level="AUTOCOMMIT")
        for index,row in df.iterrows():
            conn.execute(text(f'DROP DATABASE "{row['Nama Sekarang']}";'))
            st.write(f"Database {row['Nama Sekarang']} berhasil dibuat!")