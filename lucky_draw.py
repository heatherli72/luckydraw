import streamlit as st
import pandas as pd
import random

# Create a dictionary to store the results of each round
results = {}

# Display an option to upload an image for background (this is optional and won't affect the function of the app)
uploaded_file_bg = st.sidebar.file_uploader("Upload an image for background", type=['png', 'jpg', 'jpeg'])

# Display an option to upload the participant list
uploaded_file = st.file_uploader("Upload the participant list", type=['csv', 'xlsx'])

# If a file is uploaded, load it into a dataframe
if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file)
    except Exception as e:
        df = pd.read_excel(uploaded_file)

    participants = df.iloc[:, 0].values.tolist()  # assuming participant names are in the first column

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
        st.markdown(get_table_download_link(results), unsafe_allow_html=True)

# Function to create a download link for the results
def get_table_download_link(results):
    df_results = pd.DataFrame(results)
    csv = df_results.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # some strings <-> bytes conversions necessary here
    href = f'<a href="data:file/csv;base64,{b64}">Download Results</a>'
    return href
