import random
import streamlit as st

def run_lucky_draw(participants):
    st.title("Lucky Draw Program")
    st.write("Welcome to the lucky draw! Click the button below to select a winner.")

    winner = st.button("Select Winner")

    if winner:
        if len(participants) > 0:
            selected_winner = random.choice(participants)
            st.write(f"Congratulations! The winner is: {selected_winner}")
            participants.remove(selected_winner)
        else:
            st.write("There are no participants left.")

# Sample list of participants
participants_list = ["John", "Jane", "Michael", "Emily", "David"]

run_lucky_draw(participants_list)
