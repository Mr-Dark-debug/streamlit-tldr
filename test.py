import streamlit as st
from streamlit_tldraw import st_tldraw

st.title("tldraw in Streamlit")

# Basic usage
result = st_tldraw(key="my_canvas")


# Display the result
if result:
    st.write("Canvas data:", result)