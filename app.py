# app.py
# Streamlit app for an interactive Missionaries and Cannibals game
# Users make moves via buttons; includes BFS solver from main.py

import streamlit as st
from main import is_valid, get_children, bfs  # Import logic from main.py

# Initialize session state to track game progress
if 'state' not in st.session_state:
    st.session_state.state = (3, 3, 1)  # (missionaries_left, cannibals_left, boat_on_left)
    st.session_state.moves = []  # Track moves made
    st.session_state.game_over = False
    st.session_state.message = ""

# Function to display state as text (e.g., "MMM CC | Boat ~~~ Right: ")
def display_state(state):
    m_left, c_left, boat = state
    m_right = 3 - m_left
    c_right = 3 - c_left
    left = f"{'M' * m_left}{'C' * c_left}" or "Empty"
    right = f"{'M' * m_right}{'C' * c_right}" or "Empty"
    boat_pos = "Left" if boat else "Right"
    return f"Left: {left} | {'Boat ~~~ ' if boat else '~~~ Boat '}Right: {right}"

# Function to reset game
def reset_game():
    st.session_state.state = (3, 3, 1)
    st.session_state.moves = []
    st.session_state.game_over = False
    st.session_state.message = ""

# Main app
st.title("Missionaries and Cannibals Game")
st.write("Get 3 missionaries (M) and 3 cannibals (C) across the river. Boat holds up to 2. Cannibals can't outnumber missionaries on either side.")

# Display current state
st.subheader("Current State")
st.text(display_state(st.session_state.state))

# Check if game is won
if st.session_state.state == (0, 0, 0):
    st.session_state.game_over = True
    st.session_state.message = "You won! Everyone crossed safely!"

# Move buttons (only show if game not over)
if not st.session_state.game_over:
    st.subheader("Choose a Move")
    moves = [(1, 0, "1 Missionary"), (2, 0, "2 Missionaries"), (0, 1, "1 Cannibal"), 
             (0, 2, "2 Cannibals"), (1, 1, "1 Missionary + 1 Cannibal")]
    cols = st.columns(5)  # 5 buttons in a row
    for i, (dm, dc, label) in enumerate(moves):
        with cols[i]:
            if st.button(label):
                m, c, boat = st.session_state.state
                dir = -1 if boat else 1  # Subtract if boat on left, add if on right
                new_m = m + dir * dm
                new_c = c + dir * dc
                new_state = (new_m, new_c, 1 - boat)
                if 0 <= new_m <= 3 and 0 <= new_c <= 3 and is_valid(new_state):
                    st.session_state.state = new_state
                    st.session_state.moves.append((dm, dc, "right" if boat else "left"))
                    st.session_state.message = f"Moved {label} to the {'right' if boat else 'left'}."
                else:
                    st.session_state.message = "Invalid move! Try another."
                st.rerun()  # Refresh app to update state

# Display message (e.g., invalid move or win)
if st.session_state.message:
    st.write(st.session_state.message)

# Show move history
if st.session_state.moves:
    st.subheader("Move History")
    for i, (dm, dc, direction) in enumerate(st.session_state.moves, 1):
        st.write(f"Move {i}: Sent {dm}M {dc}C to the {direction}")

# Reset button
if st.button("Reset Game"):
    reset_game()
    st.rerun()

# BFS solution button
if st.button("Show BFS Solution"):
    solution = bfs()
    if solution:
        st.subheader("BFS Solution (Shortest Path)")
        left_m, left_c, boat = (3, 3, 1)
        for i, (dm, dc, direction) in enumerate(solution, 1):
            left_m -= dm if direction == "right" else -dm
            left_c -= dc if direction == "right" else -dc
            st.write(f"Move {i}: Send {dm}M {dc}C to the {direction}")
            st.write(f"Left: {left_m}M {left_c}C | Right: {3-left_m}M {3-left_c}C | Boat on {'left' if boat else 'right'}")
            boat = 1 - boat
    else:
        st.write("No solution found.")

# Instructions
with st.expander("How to Play"):
    st.write("""
    - Goal: Move all 3 missionaries (M) and 3 cannibals (C) from left to right.
    - Boat holds up to 2 people and must have at least 1 to move.
    - Rule: Cannibals can't outnumber missionaries on either side (unless no missionaries).
    - Click buttons to make moves. Reset to start over. Use 'Show BFS Solution' for the answer.
    """)