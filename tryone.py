import streamlit as st
import pandas as pd

# Function to handle the file upload
def file_upload():
    uploaded_file = st.file_uploader("Upload Excel", type=['xlsx'])
    if uploaded_file is not None:
        data = pd.read_excel(uploaded_file)
        st.write(data)
        return data
    return None

# Function to draw the winners
def draw(data, num_winners):
    if st.button('Draw'):
        winners = data.sample(n=num_winners)
        st.write('Winners:')
        st.write(winners)

# Main program
def main():
    data = file_upload()
    if data is not None:
        num_winners = st.number_input('Number of winners', min_value=1, max_value=len(data), value=1, step=1)
        draw(data, num_winners)

# Run the main program
if __name__ == "__main__":
    main()
