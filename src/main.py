# main.py
# Solves the Missionaries and Cannibals Problem: Get 3 missionaries and 3 cannibals
# across a river using a boat that holds up to 2 people, without cannibals outnumbering
# missionaries on either side.

from collections import deque  # Used for the queue in BFS (like a line of tasks)

# Starting state: 3 missionaries (M), 3 cannibals (C) on left, boat on left
INITIAL = (3, 3, 1)  # (missionaries_left, cannibals_left, boat_on_left)
# Goal state: Everyone on right (nothing on left, boat on right)
GOAL = (0, 0, 0)

# Possible boat moves: (missionaries, cannibals) to send across
MOVES = [(1, 0), (2, 0), (0, 1), (0, 2), (1, 1)]  # e.g., (1,0) means 1 missionary

# Checks if a state is safe (cannibals don't outnumber missionaries)
def is_valid(state):
    m_left, c_left, boat = state  # Unpack state
    m_right = 3 - m_left  # Missionaries on right
    c_right = 3 - c_left  # Cannibals on right
    # Safe if: no missionaries OR cannibals <= missionaries on both sides
    if (m_left > 0 and c_left > m_left) or (m_right > 0 and c_right > m_right):
        return False  # Unsafe: too many cannibals
    return True  # Safe

# Finds all possible next states from current state
def get_children(state):
    m, c, boat = state  # Current number of M, C, and boat position
    children = []  # List to store next states
    # If boat on left (1), move to right (-); if on right (0), move to left (+)
    dir = -1 if boat else 1
    for dm, dc in MOVES:  # Try each possible move
        new_m = m + dir * dm  # Update missionaries
        new_c = c + dir * dc  # Update cannibals
        # Check if new counts are valid (between 0 and 3)
        if 0 <= new_m <= 3 and 0 <= new_c <= 3:
            new_state = (new_m, new_c, 1 - boat)  # New state with boat flipped
            if is_valid(new_state):  # Only add if safe
                children.append((new_state, (dm, dc, 'right' if boat else 'left')))
    return children

# Breadth-First Search to find shortest path
def bfs():
    queue = deque([(INITIAL, [])])  # (state, path_so_far)
    visited = set([INITIAL])  # Track seen states to avoid repeats
    while queue:  # While there are states to check
        state, path = queue.popleft()  # Get next state
        if state == GOAL:  # If we reached the goal, return the path
            return path
        for child, move in get_children(state):  # Try all possible moves
            if child not in visited:  # If we haven't seen this state
                visited.add(child)  # Mark it seen
                new_path = path + [move]  # Add move to path
                queue.append((child, new_path))  # Add to queue
    return None  # No solution found

# Run the program and print the solution
def main():
    solution = bfs()  # Find the solution
    if solution:
        print("Solution found in", len(solution), "moves:")
        left_m, left_c, boat = INITIAL  # Start with initial state
        for i, (dm, dc, direction) in enumerate(solution, 1):
            # Update counts based on move
            if direction == 'right':
                left_m -= dm
                left_c -= dc
            else:  # left
                left_m += dm
                left_c += dc
            # Print each step
            print(f"Move {i}: Send {dm} missionaries and {dc} cannibals to the {direction}.")
            print(f"Left: {left_m}M {left_c}C | Right: {3-left_m}M {3-left_c}C | Boat on {'left' if boat else 'right'}")
            boat = 1 - boat  # Flip boat for next move
    else:
        print("No solution found.")

if __name__ == "__main__":
    main()  # Run the program