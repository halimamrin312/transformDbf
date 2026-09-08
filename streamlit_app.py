import streamlit as st

pages = {
    ".DBF Converter": [
        st.Page("singleFile.py", title="Single File"),
        st.Page("multiFile.py", title="Multi File"),
    ],
    "Testing Code": [
        st.Page("test.py", title="test"),
    ]
}

pg = st.navigation(pages)
pg.run()