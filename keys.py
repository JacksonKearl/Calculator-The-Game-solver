'''Define functions which operate on state the same way the game keys do'''

from formatters import str_in, num_in, num, handle_negatives, unlock_state


def shift():
    '''
    >>> shift()(('1', 0, ()))
    ('0', 0, ())
    >>> shift()(('-1', 0, ()))
    ('0', 0, ())
    >>> shift()(('11', 0, ()))
    ('1', 0, ())
    >>> shift()(('-11', 0, ()))
    ('-1', 0, ())
    >>> shift()(('1.1', 0, ()))
    ('1', 0, ())
    '''
    @str_in
    @handle_negatives
    @unlock_state
    def inner(state):
        state[0] = state[0][:-1]
    return inner


def inc(num):
    '''
    >>> inc(1)(('1', 0, ()))
    ('1', 1, ())
    >>> inc(4)(('1', 1, ()))
    ('1', 5, ())
    '''
    @unlock_state
    def inner(state):
        state[1] = state[1] + num
    return inner


def rotL():
    '''
    >>> rotL()(('1', 0, ()))
    ('1', 0, ())
    >>> rotL()(('21', 0, ()))
    ('12', 0, ())
    >>> rotL()(('1234', 0, ()))
    ('2341', 0, ())
    >>> rotL()(('-1234', 0, ()))
    ('-2341', 0, ())
    '''
    @str_in
    @handle_negatives
    @unlock_state
    def inner(state):
        state[0] = state[0][1:] + state[0][0]
    return inner


def rotR():
    '''
    >>> rotR()(('1', 0, ()))
    ('1', 0, ())
    >>> rotR()(('21', 0, ()))
    ('12', 0, ())
    >>> rotR()(('1234', 0, ()))
    ('4123', 0, ())
    >>> rotR()(('-1234', 0, ()))
    ('-4123', 0, ())
    '''
    @str_in
    @handle_negatives
    @unlock_state
    def inner(state):
        state[0] = state[0][-1] + state[0][:-1]
    return inner


def rev():
    '''
    >>> rev()(('1', 0, ()))
    ('1', 0, ())
    >>> rev()(('-1', 0, ()))
    ('-1', 0, ())
    >>> rev()(('12', 0, ()))
    ('21', 0, ())
    >>> rev()(('-12', 0, ()))
    ('-21', 0, ())
    >>> rev()(('1.2', 0, ()))
    ('2.1', 0, ())
    >>> rev()(('-1.2', 0, ()))
    ('-2.1', 0, ())
    >>> rev()(('-11.2', 0, ())) is None
    True
    >>> rev()(('11.2', 0, ())) is None
    True
    '''
    @str_in
    @handle_negatives
    @unlock_state
    def inner(state):
        state[0] = str(num(state[0][::-1]))
    return inner


def rep(old, new):
    '''
    >>> rep(4,1)(('414', 0, ()))
    ('111', 0, ())
    >>> rep(3,1)(('3.1', 0, ()))
    ('1.1', 0, ())
    >>> rep(23, 45)(('23623', 0, ()))
    ('45645', 0, ())
    >>> rep(1, 45)(('1.6', 0, ()))
    ('45.6', 0, ())
    >>> rep(1, 45)(('1.1', 0, ())) is None
    True
    '''
    @str_in
    @unlock_state
    def inner(state):
        state[0] = state[0].replace(str(old), str(new))
    return inner


def dir(num):
    '''
    >>> dir(1)(('414', 0, ()))
    ('4141', 0, ())
    >>> dir(0)(('3', 0, ()))
    ('30', 0, ())
    >>> dir(7)(('3.1', 0, ())) is None
    True
    >>> dir(23)(('23623', 0, ()))
    ('2362323', 0, ())
    >>> dir(1)(('-2', 0, ()))
    ('-21', 0, ())
    '''
    @str_in
    @unlock_state
    def inner(state):
        state[0] = state[0] + str(num + state[1])
    inner.label = lambda state: str(int(num) + state[1])
    return inner


def summer():
    '''
    >>> summer()(('34', 0, ()))
    ('7', 0, ())
    >>> summer()(('-34', 0, ()))
    ('-7', 0, ())
    >>> summer()(('3.4', 0, ())) is None
    True
    '''
    @str_in
    @handle_negatives
    @unlock_state
    def inner(state):
        if "." in state[0]:
            state[0] = None
            return
        state[0] = str(sum(int(x) for x in state[0] if x in "01234556789"))
    return inner


def mult(num):
    '''
    >>> mult(-1)(('34', 0, ()))
    ('-34', 0, ())
    >>> mult(4)(('3.4', 0, ()))
    ('13.6', 0, ())
    '''
    @num_in
    @unlock_state
    def inner(state):
        state[0] = state[0] * (num + state[1])
    inner.label = lambda state: "*" + str(int(num) + state[1])
    return inner


def negate():
    '''
    >>> negate()(('34', 0, ()))
    ('-34', 0, ())
    >>> negate()(('-3.4', 0, ()))
    ('3.4', 0, ())
    '''
    @num_in
    @unlock_state
    def inner(state):
        state[0] = -state[0]
    return inner


def add(num):
    '''
    >>> add(-1)(('34', 0, ()))
    ('33', 0, ())
    >>> add(4)(('3.4', 0, ()))
    ('7.4', 0, ())
    '''
    @num_in
    @unlock_state
    def inner(state):
        state[0] = state[0] + (num + state[1])
    inner.label = lambda state: "+" + str(int(num) + state[1])
    return inner


def sub(num):
    '''
    >>> sub(-1)(('34', 0, ()))
    ('35', 0, ())
    >>> sub(4)(('3.4', 0, ()))
    ('-0.6', 0, ())
    '''
    @num_in
    @unlock_state
    def inner(state):
        state[0] = state[0] - (num + state[1])
    inner.label = lambda state: "-" + str(int(num) + state[1])
    return inner


def div(num):
    '''
    >>> div(10)(('34', 0, ()))
    ('3.4', 0, ())
    >>> div(-10)(('34', 0, ()))
    ('-3.4', 0, ())
    >>> div(7)(('7', 0, ()))
    ('1', 0, ())
    >>> div(7)(('8', 0, ())) is None
    True
    >>> div(7)(('14', 0, ()))
    ('2', 0, ())
    '''
    @num_in
    @unlock_state
    def inner(state):
        state[0] = state[0] / (num + state[1])
    inner.label = lambda state: "/" + str(int(num) + state[1])
    return inner


def pow(num):
    '''
    >>> pow(2)(('34', 0, ()))
    ('1156', 0, ())
    >>> pow(2)(('-1', 0, ()))
    ('1', 0, ())
    >>> pow(3)(('-7', 0, ()))
    ('-343', 0, ())
    >>> pow(2)(('1.5', 0, ())) is None
    True
    '''
    @num_in
    @unlock_state
    def inner(state):
        state[0] = state[0]**num
    return inner


def mirror():
    '''
    >>> mirror()(('91', 0, ()))
    ('9119', 0, ())
    >>> mirror()(('-34', 0, ()))
    ('-3443', 0, ())
    '''
    @str_in
    @handle_negatives
    @unlock_state
    def inner(state):
        if "." in state[0]:
            state[0] = None
        state[0] = state[0] + state[0][::-1]
    return inner


if __name__ == "__main__":
    import doctest
    doctest.testmod()
