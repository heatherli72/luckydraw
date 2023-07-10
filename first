import streamlit as st
import pandas as pd
import random
import base64
from faker import Faker

# Function to create a download link for the dataframes
def get_table_download_link(df, filename, linkname):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # some strings <-> bytes conversions necessary here
    href = f'<a href="data:file/csv;base64,{b64}" download="{filename}">{linkname}</a>'
    return href

# Generate a sample participant list
def generate_sample_list(num_participants=500):
    fake = Faker()
    names = [fake.name() for _ in range(num_participants)]
    df_sample = pd.DataFrame(names, columns=['Name'])
    return df_sample

# Create a dictionary to store the results of each round
results = {}

df_sample = generate_sample_list()
st.sidebar.markdown(get_table_download_link(df_sample, 'sample_participant_list.csv', 'Download Sample Participant List'), unsafe_allow_html=True)

# Display an option to upload the participant list
uploaded_file = st.file_uploader("Upload the participant list", type=['csv', 'xlsx'])

# If a file is uploaded, load it into a dataframe
if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file)
    except Exception as e:
        df = pd.read_excel(uploaded_file)

    participants = df['Name'].tolist()  # assuming participant names are in the 'Name' column

    # Allow the user to input the number of rounds and number of winners for each round
    num_rounds = st.number_input('Enter the number of rounds', min_value=1, value=1, step=1)
    winners_each_round = st.number_input('Enter the number of winners in each round', min_value=1, value=1, step=1)

    # Start the lucky draw with a button
    start = st.button("Start the lucky draw")

    if start:
        for i in range(num_rounds):
            round_name = "Round " + str(i+1)
            if len(participants) >= winners_each_round:
                winners = random.sample(participants, winners_each_round)
                results[round_name] = winners

                # Display the winners and round name
                st.success(f"Congratulations to the {winners_each_round} winners of {round_name}: {', '.join(winners)}")

                # Remove winners from the participants list
                participants = [participant for participant in participants if participant not in winners]
            else:
                st.error("Not enough participants for another round.")
                break

        # After all rounds, allow the user to download the results
        df_results = pd.DataFrame.from_dict(results, orient='index').transpose()
        st.markdown(get_table_download_link(df_results, 'draw_results.csv', 'Download Draw Results'), unsafe_allow_html=True)
