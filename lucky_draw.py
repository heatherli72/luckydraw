import pandas as pd
import random
import streamlit as st

def load_participants(file):
    participants = pd.read_excel(file)
    return participants["Name"].tolist()

def run_lucky_draw():
    st.set_page_config(
        page_title="Lucky Draw Program",
        layout="wide",
        initial_sidebar_state="collapsed"
    )

    # Upload background image
    st.sidebar.title("Lucky Draw Settings")
    background_img = st.sidebar.file_uploader("Upload Background Image", type=["jpg", "jpeg", "png"])

    # Set background image
    if background_img is not None:
        st.markdown(
            f"""
            <style>
            .reportview-container {{
                background: url(data:image/png;base64,{background_img.read().encode("base64").decode()}) no-repeat center center fixed;
                background-size: cover;
            }}
            </style>
            """,
            unsafe_allow_html=True
        )

    # Function to run lucky draw
    def run_lucky_draw_round(participants, round_name, round_select_number):
        if len(participants) < round_select_number:
            st.write(f"Not enough participants for Round '{round_name}'")
            return

        st.write(f"\nRound: {round_name}")
        selected_winners = random.sample(participants, round_select_number)
        for winner in selected_winners:
            participants.remove(winner)
            st.write(f"Winner: {winner}")
        st.write(f"Congratulations to the {round_select_number} winners of {round_name}!")

        return participants

    # Main lucky draw program
    st.title("Lucky Draw Program")
    st.write("Welcome to the lucky draw!")

    # Upload Excel file
    st.write("Step 1: Upload the Excel file with the participants' names.")
    file = st.file_uploader("Upload Excel File", type=["xlsx"])
    participants = []
    if file is not None:
        participants = load_participants(file)

    # Display participants' names
    st.write("\nParticipants:")
    st.write(participants)

    # Rounds of lucky draw
    st.write("Step 2: Enter the details for each round of lucky draw.")
    rounds = []
    round_index = 1
    while True:
        round_name = st.text_input(f"Round {round_index} - Name", key=f"round_name_{round_index}")
        round_select_number = st.number_input(f"Round {round_index} - Number of Winners", min_value=1, value=1, step=1, key=f"round_select_number_{round_index}")
        rounds.append((round_name, int(round_select_number)))

        add_round = st.button(f"Add Another Round {round_index}")
        if not add_round:
            break
        round_index += 1

    # Start lucky draw
    start_lucky_draw = st.button("Start Lucky Draw")
    if start_lucky_draw:
        for round_name, round_select_number in rounds:
            participants = run_lucky_draw_round(participants, round_name, round_select_number)

        # Download results
        if len(participants) == 0:
            st.write("\n\n")
            st.write("Download the results:")
            results_df = pd.DataFrame({
                "Round": [round_name for round_name, _ in rounds for _ in range(round_select_number)],
                "Winner": [winner for _, round_select_number in rounds for winner in random.sample(participants, round_select_number)]
            })
            st.write(results_df)
            st.write(results_df.to_csv(index=False), download_button=True, file_name="lucky_draw_results.csv", mime="text/csv")

# Run the lucky draw program
run_lucky_draw()
