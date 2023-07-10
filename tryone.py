import random
import streamlit as st

def run_lucky_draw(participants):
    st.title("Lucky Draw Program")
    st.write("Welcome to the lucky draw!")

    # Display sample data format
    st.subheader("Sample Data")
    st.write("The participants' names:")
    st.write(participants)

    # Rounds of lucky draw
    st.write("Step 1: Enter the details for each round of lucky draw.")
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
        winners = []
        for round_index, (round_name, round_select_number) in enumerate(rounds, start=1):
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
            st.write("\n\n")
            st.write("Download the results:")
            results = [(round_name, winner) for (round_name, _), winner in zip(rounds, winners)]
            st.write(results)

# Run the lucky draw program
participants_list = ["John", "Jane", "Michael", "Emily", "David"]
run_lucky_draw(participants_list)
