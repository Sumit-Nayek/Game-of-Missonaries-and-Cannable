# # src/app.py
# # Streamlit app for interactive Missionaries and Cannibals game.

# import streamlit as st
# from main import is_valid, get_children, bfs  # Import from same directory

# if 'state' not in st.session_state:
#     st.session_state.state = (3, 3, 1)
#     st.session_state.moves = []
#     st.session_state.game_over = False
#     st.session_state.message = ""

# def display_state(state):
#     m_left, c_left, boat = state
#     m_right = 3 - m_left
#     c_right = 3 - c_left
#     left = f"{'🧑' * m_left}{'👹' * c_left}" or "Empty"
#     right = f"{'🧑' * m_right}{'👹' * c_right}" or "Empty"
#     return f"Left: {left} | {'Boat ~~~ ' if boat else '~~~ Boat '}Right: {right}"

# def reset_game():
#     st.session_state.state = (3, 3, 1)
#     st.session_state.moves = []
#     st.session_state.game_over = False
#     st.session_state.message = ""

# st.title("Missionaries and Cannibals Game")
# st.write("Get 3 missionaries (🧑) and 3 cannibals (👹) across the river safely.")

# st.subheader("Current State")
# st.text(display_state(st.session_state.state))

# if st.session_state.state == (0, 0, 0):
#     st.session_state.game_over = True
#     st.session_state.message = "You won! 🎉"

# if not st.session_state.game_over:
#     st.subheader("Choose a Move")
#     moves = [(1, 0, "🧑"), (2, 0, "🧑🧑"), (0, 1, "👹"), (0, 2, "👹👹"), (1, 1, "🧑👹")]
#     cols = st.columns(5)
#     for i, (dm, dc, label) in enumerate(moves):
#         with cols[i]:
#             if st.button(label):
#                 m, c, boat = st.session_state.state
#                 dir = -1 if boat else 1
#                 new_m = m + dir * dm
#                 new_c = c + dir * dc
#                 new_state = (new_m, new_c, 1 - boat)
#                 if 0 <= new_m <= 3 and 0 <= new_c <= 3 and is_valid(new_state):
#                     st.session_state.state = new_state
#                     st.session_state.moves.append((dm, dc, "right" if boat else "left"))
#                     st.session_state.message = f"Moved {label} to the {'right' if boat else 'left'}."
#                 else:
#                     st.session_state.message = "Invalid move! 😕"
#                 st.rerun()

# if st.session_state.message:
#     st.write(st.session_state.message)

# if st.session_state.moves:
#     st.subheader("Move History")
#     for i, (dm, dc, direction) in enumerate(st.session_state.moves, 1):
#         label = f"{'🧑' * dm}{'👹' * dc}"
#         st.write(f"Move {i}: Sent {label} to the {direction}")

# if st.button("Reset Game"):
#     reset_game()
#     st.rerun()

# if st.button("Show BFS Solution"):
#     solution = bfs()
#     if solution:
#         st.subheader("BFS Solution")
#         left_m, left_c, boat = (3, 3, 1)
#         for i, (dm, dc, direction) in enumerate(solution, 1):
#             left_m -= dm if direction == "right" else -dm
#             left_c -= dc if direction == "right" else -dc
#             label = f"{'🧑' * dm}{'👹' * dc}"
#             st.write(f"Move {i}: Send {label} to the {direction}")
#             st.write(f"Left: {left_m}🧑 {left_c}👹 | Right: {3-left_m}🧑 {3-left_c}👹 | Boat on {'left' if boat else 'right'}")
#             boat = 1 - boat

# with st.expander("How to Play"):
#     st.write("- Goal: All to the right side.\n- Rule: No outnumbering cannibals.\n- Click buttons to move.")

# app.py
# Streamlit app for Missionaries and Cannibals with Undo and animations

# app.py
# Streamlit app for Missionaries and Cannibals with Undo, animations, right-aligned Reset, and 2-column history

import streamlit as st
from main import is_valid, get_children, bfs  # Import from main.py (same dir)

# Initialize session state
if 'state' not in st.session_state:
    st.session_state.state = (3, 3, 1)  # (missionaries_left, cannibals_left, boat_on_left)
    st.session_state.moves = []  # Track moves
    st.session_state.history = [(3, 3, 1)]  # Track state history for Undo
    st.session_state.game_over = False
    st.session_state.message = ""

# Display state with emojis
def display_state(state):
    m_left, c_left, boat = state
    m_right = 3 - m_left
    c_right = 3 - c_left
    left = f"{'🧑' * m_left}{'👹' * c_left}" or "Empty"
    right = f"{'🧑' * m_right}{'👹' * c_right}" or "Empty"
    return f"Left: {left} | {'Boat ~~~ ' if boat else '~~~ Boat '}Right: {right}"

# Reset game
def reset_game():
    st.session_state.state = (3, 3, 1)
    st.session_state.moves = []
    st.session_state.history = [(3, 3, 1)]
    st.session_state.game_over = False
    st.session_state.message = ""

# Undo last move
def undo_move():
    if len(st.session_state.history) > 1:  # Ensure there's a previous state
        st.session_state.history.pop()  # Remove current state
        st.session_state.state = st.session_state.history[-1]  # Restore previous
        if st.session_state.moves:
            st.session_state.moves.pop()  # Remove last move
        st.session_state.message = "Undid last move."
        st.session_state.game_over = False
    else:
        st.session_state.message = "No moves to undo!"

# Main app
st.title("Missionaries and Cannibals Game")
st.write("Get 3 missionaries (🧑) and 3 cannibals (👹) across the river safely. Cannibals can't outnumber missionaries.")

# Display current state
st.subheader("Current State")
st.text(display_state(st.session_state.state))

# Check win condition
if st.session_state.state == (0, 0, 0):
    st.session_state.game_over = True
    st.session_state.message = "You won! 🎉"
    st.balloons()  # Winning animation

# Check game over (invalid state after move)
if not is_valid(st.session_state.state) and st.session_state.state != (0, 0, 0):
    st.session_state.game_over = True
    st.error("😢 Game Over! Cannibals outnumber missionaries.")

# Move buttons (only if not game over)
if not st.session_state.game_over:
    st.subheader("Choose a Move")
    moves = [(1, 0, "🧑"), (2, 0, "🧑🧑"), (0, 1, "👹"), (0, 2, "👹👹"), (1, 1, "🧑👹")]
    cols = st.columns(5)
    for i, (dm, dc, label) in enumerate(moves):
        with cols[i]:
            if st.button(label, key=f"move_{i}"):
                m, c, boat = st.session_state.state
                dir = -1 if boat else 1
                new_m = m + dir * dm
                new_c = c + dir * dc
                new_state = (new_m, new_c, 1 - boat)
                if 0 <= new_m <= 3 and 0 <= new_c <= 3:
                    st.session_state.state = new_state
                    st.session_state.history.append(new_state)
                    st.session_state.moves.append((dm, dc, "right" if boat else "left"))
                    st.session_state.message = f"Moved {label} to the {'right' if boat else 'left'}."
                else:
                    st.session_state.message = "Invalid move! 😕"
                st.rerun()

# Display message
if st.session_state.message:
    st.write(st.session_state.message)

# Move history in 2-column format
if st.session_state.moves:
    st.subheader("Move History")
    col1, col2 = st.columns([1, 3])  # 1:3 ratio for Move # and Description
    with col1:
        st.write("**Move #**")
    with col2:
        st.write("**Description**")
    for i, (dm, dc, direction) in enumerate(st.session_state.moves, 1):
        label = f"{'🧑' * dm}{'👹' * dc}"
        with col1:
            st.write(f"Move {i}")
        with col2:
            st.write(f"Sent {label} to the {direction}")

# Undo button
if st.session_state.moves and not st.session_state.game_over:
    if st.button("Undo Last Move"):
        undo_move()
        st.rerun()

# Reset button (right-aligned)
cols = st.columns([4, 1])  # 80% empty left, 20% right for button
with cols[1]:
    if st.button("Reset Game"):
        reset_game()
        st.rerun()

# BFS solution button
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

# Instructions
with st.expander("How to Play"):
    st.write("""
    - **Goal**: Move all 3 missionaries (🧑) and 3 cannibals (👹) from left to right.
    - **Boat**: Holds up to 2 people, needs at least 1 to move.
    - **Rule**: Cannibals can't outnumber missionaries on either side (unless no missionaries).
    - **Controls**: Click move buttons, use Undo to revert, Reset (right side) to start over, or Show BFS Solution for the answer.
    """)