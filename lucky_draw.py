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

    # Function to run lucky draw round
    def run_lucky_draw_round(round_name, round_select_number, participants):
        if len(participants) < round_select_number:
            st.write(f"Not enough participants for Round '{round_name}'")
            return

        st.write(f"\nRound: {round_name}")
        winners = random.sample(participants, round_select_number)
        for i, winner in enumerate(winners, start=1):
            st.write(f"Winner {i}: {winner}")
        st.write(f"Congratulations to the {round_select_number} winners of {round_name}!")

        # Remove winners from the participant list
        participants = [participant for participant in participants if participant not in winners]
        return participants, winners

    # Main lucky draw program
    st.title("Lucky Draw Program")
    st.write("Welcome to the lucky draw!")

    # Upload Excel file
    st.write("Step 1: Upload the Excel file with the participants' names.")
    file = st.file_uploader("Upload Excel File", type=["xlsx"])
    participants = []
    if file is not None:
        participants = load_participants(file)

    # Rounds of lucky draw
    st.write("Step 2: Enter the details for each round of lucky draw.")
    rounds = []
    round_index = 1
    while True:
        round_name = st.text_input(f"Round {round_index} - Name", key=f"round_name_{round_index}")
        round_select_number = st.number_input(f"Round {round_index} - Number of Winners", min_value=1, value=1, step=1, key=f"round_select_number_{round_index}")
        rounds.append((round_name, round_select_number))

        add_round = st.button(f"Add Another Round {round_index}")
        if not add_round:
            break
        round_index += 1

    # Start lucky draw
    start_lucky_draw = st.button("Start Lucky Draw")
    if start_lucky_draw:
        all_winners = []
        add_another_round = True
        while add_another_round:
            for round_name, round_select_number in rounds:
                participants, winners = run_lucky_draw_round(round_name, round_select_number, participants)
                all_winners.append((round_name, winners))
                
            add_another_round = st.button("Add Another Round")

        # Download results
        st.write("\n\nDownload the results:")
        results_df = pd.DataFrame([(round_name, winner) for round_name, winners in all_winners for winner in winners], columns=["Round", "Winner"])
        st.write(results_df.to_csv(index=False), download_button=True, file_name="lucky_draw_results.csv", mime="text/csv")

# Run the lucky draw program
run_lucky_draw()
