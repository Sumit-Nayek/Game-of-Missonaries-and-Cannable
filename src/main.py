# Solves the Missionaries and Cannibals Problem using BFS.
from collections import deque

INITIAL = (3, 3, 1)  # (m_left, c_left, boat_left)
GOAL = (0, 0, 0)
MOVES = [(1, 0), (2, 0), (0, 1), (0, 2), (1, 1)]

def is_valid(state):
    m_left, c_left, boat = state
    m_right = 3 - m_left
    c_right = 3 - c_left
    if (m_left > 0 and c_left > m_left) or (m_right > 0 and c_right > m_right):
        return False
    return True

def get_children(state):
    m, c, boat = state
    children = []
    dir = -1 if boat else 1
    for dm, dc in MOVES:
        new_m = m + dir * dm
        new_c = c + dir * dc
        if 0 <= new_m <= 3 and 0 <= new_c <= 3:
            new_state = (new_m, new_c, 1 - boat)
            if is_valid(new_state):
                children.append((new_state, (dm, dc, 'right' if boat else 'left')))
    return children

def bfs():
    queue = deque([(INITIAL, [])])
    visited = set([INITIAL])
    while queue:
        state, path = queue.popleft()
        if state == GOAL:
            return path
        for child, move in get_children(state):
            if child not in visited:
                visited.add(child)
                new_path = path + [move]
                queue.append((child, new_path))
    return None