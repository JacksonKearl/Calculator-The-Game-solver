'''
This mudule provides data formatters and function wrappers built for
ensuring consistant representation of state with the game
'''


def num(to_convert):
    '''
    given a number as a string or number, make an int from it if possible,
    otherwise return it as a float
    >>> num(1)
    1
    >>> num('1')
    1
    >>> num(1.1)
    1.1
    >>> num('1.1')
    1.1
    '''
    try:
        return int(str(to_convert))
    except ValueError:
        return float(str(to_convert))


def int_if_possible(to_convert):
    '''
    Turn this numeric quantity into an integer, if doing so does not lose any precision
    >>> int_if_possible(1)
    1
    >>> int_if_possible(0)
    0
    >>> int_if_possible(1.0)
    1
    >>> int_if_possible(0.0)
    0
    >>> int_if_possible(1.5)
    1.5
    >>> int_if_possible('1')
    1
    >>> int_if_possible('1.0')
    1
    >>> int_if_possible('1.5')
    1.5
    '''
    string_val = str(to_convert)

    if string_val[-2:] == ".0":
        return int(string_val[:-2])
    elif "." not in string_val:
        return int(string_val)
    return float(string_val)


def validate_num(to_validate):
    '''
    Check if this float can conform to the rules of the game (i.e. only one decimal place),
    if so, return a string normalized verison of it, if not return None
    >>> validate_num(1.0)
    '1'
    >>> validate_num(1.1)
    '1.1'
    >>> validate_num(1.11) is None
    True
    '''
    if abs(round(to_validate, 1) - to_validate) < 0.001:
        return str(int_if_possible(round(to_validate, 1)))
    else:
        return None


def unlock_state(func):
    '''
    "unlocks" state into modifiable format to pass
    to a state-updating function, then locks back
    up the return value for passing to places where
    immutable state objects are needed (i.e. the BFS)
    '''
    def inner(state):
        unlocked = list(state)
        unlocked[2] = list(state[2])
        func(unlocked)  # func modifies unlocked directly
        unlocked[2] = tuple(unlocked[2])
        locked = tuple(unlocked)
        return locked
    return inner


def manage_history(func):
    '''
    wraps a function to manage the history component of state.
    Appends the state[0] output of the wrapped function to the state[2] 
    history log
    '''
    def inner(state):
        new_state = func(state)
        return (new_state[0], new_state[1], new_state[2] + (new_state[0],))
    return inner


def nullify_if_first_state_none(func):
    def inner(state):
        new_state = func(state)
        if new_state[0] is None:
            return None
        return new_state
    return inner


def general_state_management(func):
    return nullify_if_first_state_none(manage_history(func))


def str_in(func):
    '''
    use this to wrap any function which deals with state as a string
    >>> @str_in
    ... def rev(state):
    ...    return (state[0][::-1], state[1], state[2])
    ...
    >>> rev(('123', 0, ()))
    ('321', 0, ('321',))
    >>> rev(('1.2', 0, ()))
    ('2.1', 0, ('2.1',))
    >>> rev(('22.1', 0, ())) is None
    True
    '''
    @general_state_management
    def inner(state):
        new_state = func(state)
        if new_state[0] is None:
            return (None, state[1], state[2])

        out = str(new_state[0])
        if out == "" or out == "-":
            out = "0"
        if len(out) > 6:
            return (None, state[1], state[2])
        return (validate_num(num(out)), new_state[1], new_state[2])
    return inner


def num_in(func):
    '''
    use this to wrap any function which deals with state as a number
    >>> @num_in
    ... def div7(state):
    ...    return (state[0]/7, state[1], state[2])
    ...
    >>> div7((7, 0, ()))
    ('1', 0, ('1',))
    >>> div7((49, 0, ()))
    ('7', 0, ('7',))
    >>> div7((8, 0, ())) is None
    True
    '''
    @str_in
    def inner(state):
        num_state = (num(state[0]), state[1], state[2])
        new_state = func(num_state)
        if new_state[0] is None:
            return (None, state[1], state[2])
        return (validate_num(new_state[0]), new_state[1], new_state[2])
    return inner


def handle_negatives(func):
    '''
    Wrapper to remove negatives from stringstates before
    passing to function, then reapply after
    '''
    def inner(state):
        if state[0][0] == "-":
            new_state = func((state[0][1:], state[1], state[2]))
            return ("-" + new_state[0], new_state[1], new_state[2])
        return func(state)
    return inner


if __name__ == "__main__":
    import doctest
    doctest.testmod()
