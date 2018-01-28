'''Define functions which operate on state the same way the game keys do'''

from formatters import str_in, num_in, num, handle_negatives


def shift():
    '''
    >>> shift()('1')
    '0'
    >>> shift()('-1')
    '0'
    >>> shift()('11')
    '1'
    >>> shift()('-11')
    '-1'
    >>> shift()('1.1')
    '1'
    '''
    @str_in
    @handle_negatives
    def inner(state):
        return state[:-1]
    return inner


def rotL():
    '''
    >>> rotL()('1')
    '1'
    >>> rotL()('21')
    '12'
    >>> rotL()('1234')
    '2341'
    >>> rotL()('-1234')
    '-2341'
    '''
    @str_in
    @handle_negatives
    def inner(state):
        return state[1:] + state[0]
    return inner


def rotR():
    '''
    >>> rotR()('1')
    '1'
    >>> rotR()('21')
    '12'
    >>> rotR()('1234')
    '4123'
    >>> rotR()('-1234')
    '-4123'
    '''
    @str_in
    @handle_negatives
    def inner(state):
        return state[-1] + state[:-1]
    return inner


def rev():
    '''
    >>> rev()('1')
    '1'
    >>> rev()('-1')
    '-1'
    >>> rev()('12')
    '21'
    >>> rev()('-12')
    '-21'
    >>> rev()('1.2')
    '2.1'
    >>> rev()('-1.2')
    '-2.1'
    >>> rev()('-11.2') is None
    True
    >>> rev()('11.2') is None
    True
    '''
    @str_in
    @handle_negatives
    def inner(state):
        return str(num(state[::-1]))
    return inner


def rep(old, new):
    '''
    >>> rep(4,1)('414')
    '111'
    >>> rep(3,1)('3.1')
    '1.1'
    >>> rep(23, 45)('23623')
    '45645'
    >>> rep(1, 45)('1.6')
    '45.6'
    >>> rep(1, 45)('1.1') is None
    True
    '''
    @str_in
    def inner(state):
        return state.replace(str(old), str(new))
    return inner


def dir(num):
    '''
    >>> dir(1)('414')
    '4141'
    >>> dir(0)('3')
    '30'
    >>> dir(7)('3.1') is None
    True
    >>> dir(23)('23623')
    '2362323'
    >>> dir(1)('-2')
    '-21'
    '''
    @str_in
    def inner(state):
        return state + str(num)
    return inner


def summer():
    '''
    >>> summer()('34')
    '7'
    >>> summer()('-34')
    '-7'
    >>> summer()('3.4') is None
    True
    '''
    @str_in
    @handle_negatives
    def inner(state):
        if "." in state:
            return None
        return str(sum(int(x) for x in state if x in "01234556789"))
    return inner


def mult(num):
    '''
    >>> mult(-1)('34')
    '-34'
    >>> mult(4)('3.4')
    '13.6'
    '''
    @num_in
    def inner(state):
        return state * num
    return inner


def add(num):
    '''
    >>> add(-1)('34')
    '33'
    >>> add(4)('3.4')
    '7.4'
    '''
    @num_in
    def inner(state):
        return state + num
    return inner


def sub(num):
    '''
    >>> sub(-1)('34')
    '35'
    >>> sub(4)('3.4')
    '-0.6'
    '''
    @num_in
    def inner(state):
        return state - num
    return inner


def div(num):
    '''
    >>> div(10)('34')
    '3.4'
    >>> div(-10)('34')
    '-3.4'
    >>> div(7)('7')
    '1'
    >>> div(7)('8') is None
    True
    >>> div(7)('14')
    '2'
    '''
    @num_in
    def inner(state):
        return state / num
    return inner


def pow(num):
    '''
    >>> pow(2)('34')
    '1156'
    >>> pow(2)('-1')
    '1'
    >>> pow(3)('-7')
    '-343'
    >>> pow(2)('1.5') is None
    True
    '''
    @num_in
    def inner(state):
        return state**num
    return inner


def mirror():
    '''
    >>> mirror()('91')
    '9119'
    >>> mirror()('-34')
    '-3443'
    '''
    @str_in
    @handle_negatives
    def inner(state):
        if "." in state:
            return None
        return state + state[::-1]
    return inner


if __name__ == "__main__":
    import doctest
    doctest.testmod()
