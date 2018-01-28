'''Define functions which operate on state the same way the game keys do'''

from formatters import str_in, num_in, num, handle_negatives, unlock_state, general_state_management


def shift():
    '''
    >>> shift()(('1', 0, ()))
    ('0', 0, ('0',))
    >>> shift()(('-1', 0, ()))
    ('0', 0, ('0',))
    >>> shift()(('11', 0, ()))
    ('1', 0, ('1',))
    >>> shift()(('-11', 0, ()))
    ('-1', 0, ('-1',))
    >>> shift()(('1.1', 0, ()))
    ('1', 0, ('1',))
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
    ('1', 1, ('1',))
    >>> inc(4)(('1', 1, ('2',)))
    ('1', 5, ('2', '1'))
    '''
    @general_state_management
    @unlock_state
    def inner(state):
        state[1] = state[1] + num
    return inner


def paste():
    def is_valid_state_combination(state1, state2):
        if "." in state1:
            return False
        if "-" in state2:
            return False
        combination = state1 + state2

        if len(combination) > 6:
            return False

        return True

    def inner(state):
        return [(state[0] + restore_val,
                 state[1],
                 (restore_val, state[0] + restore_val))
                for restore_val in state[2]
                if is_valid_state_combination(state[0], restore_val)]
    inner.label = lambda state: 'RESTORE:' + state[2][0]
    return inner


def rotL():
    '''
    >>> rotL()(('1', 0, ()))
    ('1', 0, ('1',))
    >>> rotL()(('21', 0, ()))
    ('12', 0, ('12',))
    >>> rotL()(('1234', 0, ()))
    ('2341', 0, ('2341',))
    >>> rotL()(('-1234', 0, ()))
    ('-2341', 0, ('-2341',))
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
    ('1', 0, ('1',))
    >>> rotR()(('21', 0, ()))
    ('12', 0, ('12',))
    >>> rotR()(('1234', 0, ()))
    ('4123', 0, ('4123',))
    >>> rotR()(('-1234', 0, ()))
    ('-4123', 0, ('-4123',))
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
    ('1', 0, ('1',))
    >>> rev()(('-1', 0, ()))
    ('-1', 0, ('-1',))
    >>> rev()(('12', 0, ()))
    ('21', 0, ('21',))
    >>> rev()(('-12', 0, ()))
    ('-21', 0, ('-21',))
    >>> rev()(('1.2', 0, ()))
    ('2.1', 0, ('2.1',))
    >>> rev()(('-1.2', 0, ()))
    ('-2.1', 0, ('-2.1',))
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
    ('111', 0, ('111',))
    >>> rep(3,1)(('3.1', 0, ()))
    ('1.1', 0, ('1.1',))
    >>> rep(23, 45)(('23623', 0, ()))
    ('45645', 0, ('45645',))
    >>> rep(1, 45)(('1.6', 0, ()))
    ('45.6', 0, ('45.6',))
    >>> rep(1, 45)(('1.1', 0, ())) is None
    True
    '''
    @str_in
    @unlock_state
    def inner(state):
        state[0] = state[0].replace(str(old), str(new))
    return inner


def inv10():
    '''
    >>> inv10()(('123456', 0, ()))
    ('987654', 0, ('987654',))
    >>> inv10()(('789', 0, ()))
    ('321', 0, ('321',))
    >>> inv10()(('12.3', 0, ()))
    ('98.7', 0, ('98.7',))
    >>> inv10()(('-12.3', 0, ()))
    ('-98.7', 0, ('-98.7',))
    '''
    @str_in
    @handle_negatives
    @unlock_state
    def inner(state):
        invMap = {'0': '0', '1': '9', '2': '8', '3': '7', '4': '6',
                  '5': '5', '9': '1', '8': '2', '7': '3', '6': '4', '.': '.'}
        state[0] = "".join(invMap[char] for char in state[0])
    return inner


def dir(num):
    '''
    >>> dir(1)(('414', 0, ()))
    ('4141', 0, ('4141',))
    >>> dir(0)(('3', 0, ()))
    ('30', 0, ('30',))
    >>> dir(7)(('3.1', 0, ())) is None
    True
    >>> dir(23)(('623', 0, ()))
    ('62323', 0, ('62323',))
    >>> dir(1)(('-2', 0, ()))
    ('-21', 0, ('-21',))
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
    ('7', 0, ('7',))
    >>> summer()(('-34', 0, ()))
    ('-7', 0, ('-7',))
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
    ('-34', 0, ('-34',))
    >>> mult(4)(('3.4', 0, ()))
    ('13.6', 0, ('13.6',))
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
    ('-34', 0, ('-34',))
    >>> negate()(('-3.4', 0, ()))
    ('3.4', 0, ('3.4',))
    '''
    @num_in
    @unlock_state
    def inner(state):
        state[0] = -state[0]
    return inner


def add(num):
    '''
    >>> add(-1)(('34', 0, ()))
    ('33', 0, ('33',))
    >>> add(4)(('3.4', 0, ()))
    ('7.4', 0, ('7.4',))
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
    ('35', 0, ('35',))
    >>> sub(4)(('3.4', 0, ()))
    ('-0.6', 0, ('-0.6',))
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
    ('3.4', 0, ('3.4',))
    >>> div(-10)(('34', 0, ()))
    ('-3.4', 0, ('-3.4',))
    >>> div(7)(('7', 0, ()))
    ('1', 0, ('1',))
    >>> div(7)(('8', 0, ())) is None
    True
    >>> div(7)(('14', 0, ()))
    ('2', 0, ('2',))
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
    ('1156', 0, ('1156',))
    >>> pow(2)(('-1', 0, ()))
    ('1', 0, ('1',))
    >>> pow(3)(('-7', 0, ()))
    ('-343', 0, ('-343',))
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
    ('9119', 0, ('9119',))
    >>> mirror()(('-34', 0, ()))
    ('-3443', 0, ('-3443',))
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
