import streamlit as st

pages = {
    "Transformer Tools": [
        st.Page("multiFile.py", title="DBF Converter"),
        st.Page("xlsxFile.py", title="XLSX Converter"),
        st.Page("savFile.py", title="SAV Converter"),
    ],
    "Database": [
        st.Page("createDatabase.py", title="Create Database"),
    ],
    "Testing Code": [
        st.Page("test.py", title="test"),
    ]
}

pg = st.navigation(pages)
pg.run()