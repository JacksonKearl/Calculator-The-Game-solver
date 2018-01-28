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


def str_in(func):
    '''
    use this to wrap any function which deals with state as a string
    >>> @str_in
    ... def rev(state):
    ...    return state[::-1]
    ...
    >>> rev('123')
    '321'
    >>> rev('1.2')
    '2.1'
    >>> rev('22.1') is None
    True
    '''
    def inner(state):
        if func(state) is None:
            return None
        out = str(func(state))
        if out == "" or out == "." or out == "-":
            out = "0"
        if len(out) > 7:
            return None
        return validate_num(num(out))
    return inner


def num_in(func):
    '''
    use this to wrap any function which deals with state as a number
    >>> @num_in
    ... def div7(num):
    ...    return num/7
    ...
    >>> div7(7)
    '1'
    >>> div7(49)
    '7'
    >>> div7(8) is None
    True
    '''
    @str_in
    def inner(state):
        return validate_num(func(num(state)))
    return inner


def handle_negatives(func):
    '''
    Wrapper to remove negatives from stringstates before
    passing to function, then reapply after
    '''
    def inner(state):
        if state[0] == "-":
            return "-" + func(state[1:])
        return func(state)
    return inner


if __name__ == "__main__":
    import doctest
    doctest.testmod()
