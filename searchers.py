'''This module provides path finding functions for the central logic of the app'''
from collections import deque


def bfs(start, target, transitions, end_condition_met=lambda state, target: state == target):
    '''
    perfrom a bfs from start until target, where possible next states
    from a state s are given by [t(s) for t in transitions if t(s) is not None]

    Thus to signify a transition is not applicable for a given input,
    simply return None.

    Set the __str__ attribute of functions in transitions to be able to easily 
    read back the path found.

    >>> add1 = lambda x: x+1
    >>> add1.label = lambda state: '+1'
    >>> bfs(1, 4, [add1])
    [('+1', 2), ('+1', 3), ('+1', 4)]
    >>> add1or2 = lambda x: [x+1, x+2]
    >>> add1or2.label = lambda state: str(state)
    >>> bfs(1, 4, [add1or2])
    [('2', 2), ('4', 4)]
    '''

    def flatten(list_of_list_or_val):
        '''
        given a next states list where some of the elements
        are lists themselves, flatten it out into a normal list,
        preserving labels. this needed for the Load op, which 
        can have a varaible number of outputs.
        '''
        flattened = []
        for state_or_states, label_gen in list_of_list_or_val:
            if isinstance(state_or_states, list):
                states = state_or_states
                flattened += [(state, label_gen(state)) for state in states]
            else:
                state = state_or_states
                flattened.append((state, label_gen(state)))
        return flattened

    to_visit = deque([start])
    backlinks = {start: None}
    while to_visit:
        current_state = to_visit.popleft()
        next_states_list = [(transition(current_state), transition.label)
                            for transition in transitions
                            if transition(current_state) is not None]

        all_next_states = flatten(next_states_list)
        next_states = [next_state
                       for next_state in all_next_states
                       if next_state[0] not in backlinks]

        for next_state, transition in next_states:
            backlinks[next_state] = ((transition, next_state), current_state)
            to_visit.append(next_state)
            if end_condition_met(next_state, target):
                path = deque()
                prev = backlinks[next_state]
                while prev:
                    path.appendleft(prev[0])
                    prev = backlinks[prev[1]]
                return list(path)
    return None


if __name__ == "__main__":
    import doctest
    doctest.testmod()
