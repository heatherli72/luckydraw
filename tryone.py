import streamlit as st
import pandas as pd
import random

# Upload the Excel file
uploaded_file = st.file_uploader("Upload Excel", type=['xlsx'])

# If file is uploaded, read and display the data
if uploaded_file is not None:
    data = pd.read_excel(uploaded_file)
    st.write(data)

    # Number of winners to select
    num_winners = st.number_input('Number of winners', min_value=1, max_value=len(data), value=1, step=1)

    # Button to perform the draw
    if st.button('Draw'):
        winners = data.sample(n=num_winners)
        st.write('Winners:')
        st.write(winners)
