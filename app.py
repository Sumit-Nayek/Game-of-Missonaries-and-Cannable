# src/app.py
# Streamlit app for interactive Missionaries and Cannibals game.

import streamlit as st
from main import is_valid, get_children, bfs  # Import from same directory

if 'state' not in st.session_state:
    st.session_state.state = (3, 3, 1)
    st.session_state.moves = []
    st.session_state.game_over = False
    st.session_state.message = ""

def display_state(state):
    m_left, c_left, boat = state
    m_right = 3 - m_left
    c_right = 3 - c_left
    left = f"{'🧑' * m_left}{'👹' * c_left}" or "Empty"
    right = f"{'🧑' * m_right}{'👹' * c_right}" or "Empty"
    return f"Left: {left} | {'Boat ~~~ ' if boat else '~~~ Boat '}Right: {right}"

def reset_game():
    st.session_state.state = (3, 3, 1)
    st.session_state.moves = []
    st.session_state.game_over = False
    st.session_state.message = ""

st.title("Missionaries and Cannibals Game")
st.write("Get 3 missionaries (🧑) and 3 cannibals (👹) across the river safely.")

st.subheader("Current State")
st.text(display_state(st.session_state.state))

if st.session_state.state == (0, 0, 0):
    st.session_state.game_over = True
    st.session_state.message = "You won! 🎉"

if not st.session_state.game_over:
    st.subheader("Choose a Move")
    moves = [(1, 0, "🧑"), (2, 0, "🧑🧑"), (0, 1, "👹"), (0, 2, "👹👹"), (1, 1, "🧑👹")]
    cols = st.columns(5)
    for i, (dm, dc, label) in enumerate(moves):
        with cols[i]:
            if st.button(label):
                m, c, boat = st.session_state.state
                dir = -1 if boat else 1
                new_m = m + dir * dm
                new_c = c + dir * dc
                new_state = (new_m, new_c, 1 - boat)
                if 0 <= new_m <= 3 and 0 <= new_c <= 3 and is_valid(new_state):
                    st.session_state.state = new_state
                    st.session_state.moves.append((dm, dc, "right" if boat else "left"))
                    st.session_state.message = f"Moved {label} to the {'right' if boat else 'left'}."
                else:
                    st.session_state.message = "Invalid move! 😕"
                st.rerun()

if st.session_state.message:
    st.write(st.session_state.message)

if st.session_state.moves:
    st.subheader("Move History")
    for i, (dm, dc, direction) in enumerate(st.session_state.moves, 1):
        label = f"{'🧑' * dm}{'👹' * dc}"
        st.write(f"Move {i}: Sent {label} to the {direction}")

if st.button("Reset Game"):
    reset_game()
    st.rerun()

if st.button("Show BFS Solution"):
    solution = bfs()
    if solution:
        st.subheader("BFS Solution")
        left_m, left_c, boat = (3, 3, 1)
        for i, (dm, dc, direction) in enumerate(solution, 1):
            left_m -= dm if direction == "right" else -dm
            left_c -= dc if direction == "right" else -dc
            label = f"{'🧑' * dm}{'👹' * dc}"
            st.write(f"Move {i}: Send {label} to the {direction}")
            st.write(f"Left: {left_m}🧑 {left_c}👹 | Right: {3-left_m}🧑 {3-left_c}👹 | Boat on {'left' if boat else 'right'}")
            boat = 1 - boat

with st.expander("How to Play"):
    st.write("- Goal: All to the right side.\n- Rule: No outnumbering cannibals.\n- Click buttons to move.")