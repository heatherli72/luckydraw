import pandas as pd
import random
import streamlit as st

def load_participants(file):
    participants = pd.read_excel(file)
    return participants["Name"].tolist()

def run_lucky_draw(participants):
    st.title("Lucky Draw Program")
    st.write("Welcome to the lucky draw!")
    
    # Upload Excel file
    st.write("Step 1: Upload the Excel file with the participants' names.")
    file = st.file_uploader("Upload Excel File", type=["xlsx"])
    if file is not None:
        participants = load_participants(file)

    # Rounds of lucky draw
    st.write("Step 2: Enter the details for each round of lucky draw.")
    rounds = []
    round_index = 1
    while True:
        round_name = st.text_input(f"Round {round_index} - Name", key=f"round_name_{round_index}")
        round_select_number = st.number_input(f"Round {round_index} - Number of Winners", min_value=1, value=1, step=1, key=f"round_select_number_{round_index}")
        rounds.append((round_name, int(round_select_number)))
        
        add_round = st.button("Add Another Round")
        if not add_round:
            break
        round_index += 1
    
    # Start lucky draw
    start_lucky_draw = st.button("Start Lucky Draw")
    if start_lucky_draw:
        winners = []
        for round_name, round_select_number in rounds:
            if len(participants) < round_select_number:
                st.write(f"Not enough participants for Round '{round_name}'")
                continue
            
            st.write(f"\nRound: {round_name}")
            selected_winners = random.sample(participants, round_select_number)
            winners.extend(selected_winners)
            for winner in selected_winners:
                participants.remove(winner)
                st.write(f"Winner: {winner}")
            st.write(f"Congratulations to the {round_select_number} winners of {round_name}!")

        # Download results
        if len(winners) > 0:
            results_df = pd.DataFrame({"Round": [round_name for round_name, _ in rounds for _ in range(round_select_number)],
                                       "Winner": winners})
            st.write("\n\n")
            st.write("Download the results:")
            st.write(results_df)
            st.write(results_df.to_csv(index=False), download_button=True, file_name="lucky_draw_results.csv", mime="text/csv")

# Run the lucky draw program
run_lucky_draw([])
