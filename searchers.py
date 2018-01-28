'''This module provides path finding functions for the central logic of the app'''
from collections import deque


def bfs(start, target, transitions):
    '''
    perfrom a bfs from start until target, where possible next states
    from a state s are given by [t(s) for t in transitions if t(s) is not None]

    Thus to signify a transition is not applicable for a given input,
    simply return None.

    Set the __str__ attribute of functions in transitions to be able to easily 
    read back the path found.

    >>> add1 = lambda x: x+1
    >>> add1.__str__ = '+1'
    >>> bfs(1, 4, [add1])
    [('+1', 2), ('+1', 3), ('+1', 4)]
    '''
    to_visit = deque([start])
    backlinks = {start: None}
    while to_visit:
        current_state = to_visit.popleft()
        next_states = set([(transition(current_state), transition.__str__)
                           for transition in transitions
                           if (transition(current_state) is not None
                               and transition(current_state) not in backlinks)])

        for next_state, transition in next_states:
            backlinks[next_state] = ((transition, next_state), current_state)
            to_visit.append(next_state)
            if next_state == target:
                path = deque()
                prev = backlinks[target]
                while prev:
                    path.appendleft(prev[0])
                    prev = backlinks[prev[1]]
                return list(path)
    return None


if __name__ == "__main__":
    import doctest
    doctest.testmod()
