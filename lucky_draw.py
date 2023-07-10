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

    # Main lucky draw program
    st.title("Lucky Draw Program")
    st.write("Welcome to the lucky draw!")

    # Upload Excel file
    st.write("Step 1: Upload the Excel file with the participants' names.")
    file = st.file_uploader("Upload Excel File", type=["xlsx"])
    participants = []
    if file is not None:
        participants = load_participants(file)

    rounds = []
    round_index = 1

    while True:
        round_name = st.text_input(f"Round {round_index} - Name", key=f"round_name_{round_index}")
        round_select_number = st.number_input(f"Round {round_index} - Number of Winners", min_value=1, value=1, step=1, key=f"round_select_number_{round_index}")

        start_lucky_draw = st.button(f"Start Round {round_index}")
        if start_lucky_draw:
            if len(participants) < round_select_number:
                st.write(f"Not enough participants for Round '{round_name}'")
            else:
                winners = random.sample(participants, round_select_number)
                st.write(f"\nRound: {round_name}")
                st.write(f"Congratulations to the {round_select_number} winners of {round_name}!")

                for i, winner in enumerate(winners, start=1):
                    st.write(f"Winner {i}: {winner}")

                results_df = pd.DataFrame({"Winner": winners})
                st.write("\nDownload the winners' list:")
                st.write(results_df.to_csv(index=False), download_button=True, file_name=f"winners_list_round_{round_index}.csv", mime="text/csv")

                add_another_round = st.button("Add Another Round")
                if not add_another_round:
                    break

                rounds.append((round_name, winners))
                participants = [participant for participant in participants if participant not in winners]

        round_index += 1

    # Download final results
    if rounds:
        st.write("\n\nDownload the final winners' list:")
        results_df = pd.DataFrame([(round_name, winner) for round_name, winners in rounds for winner in winners], columns=["Round", "Winner"])
        st.write(results_df.to_csv(index=False), download_button=True, file_name="final_winners_list.csv", mime="text/csv")

# Run the lucky draw program
run_lucky_draw()
