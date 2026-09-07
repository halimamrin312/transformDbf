import streamlit as st

pages = {
    ".DBF Converter": [
        st.Page("singleFile.py", title="Single File"),
        st.Page("multiFile.py", title="Multi File"),
    ]
}

pg = st.navigation(pages)
pg.run()