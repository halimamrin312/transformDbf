import os
from dotenv import load_dotenv
import streamlit as st

# Load the environment variables from the .env file
load_dotenv()

# Atribut Connection Postgress
username = os.getenv("DB_USERNAME")
password = os.getenv("DB_PASSWORD")
host = os.getenv("DB_HOST")
dbDefault = os.getenv("DB_DATABASE")

st.write(username)