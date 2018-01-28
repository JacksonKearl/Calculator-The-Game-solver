#! /usr/local/bin/python3
from keys import shift, rev, mult, summer, rep, add, sub, div, dir, pow, rotL, rotR, mirror, inc, negate, paste, inv10
from searchers import bfs


def portal(down, up):
    def perform_portal(num, up, down):
        '''
        >>> perform_portal('1', 0, 1)
        '1'
        >>> perform_portal('10', 0, 1)
        '1'
        >>> perform_portal('123', 0, 2)
        '24'
        >>> perform_portal('123', 1, 2)
        '33'
        >>> perform_portal('123', 0, 1)
        '6'
        '''
        if len(num) < down + 1:
            return num
        else:
            chars = list(num)[::-1]
            drop = chars[down]
            del chars[down]
            num = int("".join(chars)[::-1])
            num += int(drop) * 10**up
            return perform_portal(str(num), up, down)

    def portal(func):
        def inner(state):
            next_state_or_states = func(state)
            if (next_state_or_states is None or
                    not isinstance(next_state_or_states, list) and "." in next_state_or_states[0]):
                return None
            if isinstance(next_state_or_states, list):
                next_states = next_state_or_states
                return [(perform_portal(next_state[0], up, down), next_state[1], next_state[2])
                        for next_state in next_states if "." not in next_state[0]]
            else:
                next_state = next_state_or_states
                return (perform_portal(next_state[0], up, down), next_state[1], next_state[2])
        inner.label = func.label
        return inner

    return portal


def parse(token):
    '''
    Given a token representing a key present in the game,
    return a function mimicing that key.
    '''
    out = None
    if token == "<<":
        out = shift()
    elif token == "R":
        out = rev()
    elif token == "M":
        out = mirror()
    elif token == "S":
        out = paste()
    elif token == "I":
        out = inv10()
    elif token == "<":
        out = rotL()
    elif token == ">":
        out = rotR()
    elif token == "-":
        out = negate()
    elif token == "+":
        out = summer()
    elif "=>" in token:
        old, new = token.split("=>")
        out = rep(old, new)
    elif "[+]" in token:
        _, num = token.split("[+]")
        out = inc(int(num))
    elif token[0] == "+":
        out = add(float(token[1:]))
    elif token[0] == "-":
        out = sub(float(token[1:]))
    elif token[0] == "^":
        out = pow(float(token[1:]))
    elif token[0] == "*":
        out = mult(float(token[1:]))
    elif token[0] == "/":
        out = div(float(token[1:]))
    else:
        out = dir(int(token))

    if not hasattr(out, 'label'):
        out.label = lambda state: token

    return out


def insert_store_locs(path):
    seek = None
    save = []
    index = len(path) - 1
    for trans, state in path[::-1]:
        if state[0] == seek:
            save.insert(0, index)
            seek = None

        if "RESTORE:" in trans:
            seek = trans.split("RESTORE:")[1]

        index -= 1

    if seek != None:
        save.insert(0, -1)

    for i, index in enumerate(save):
        i += index
        path.insert(i + 1, ('STORE', path[i][1]))
    return path


def search(start, target, tokens, portal_params=None):
    '''
    >>> search('1', '83', ['*9', '+2'])
    [('*9', ('9', 0, ('1', '9'))), ('*9', ('81', 0, ('1', '9', '81'))),
      ('+2', ('83', 0, ('1', '9', '81', '83')))]
    >>> search('0', '6', ['+5', '[+]1'])
    [('[+]1', ('0', 1, ('0', '0'))), ('+6', ('6', 1, ('0', '0', '6')))]
    '''
    portal_dec = portal(*portal_params) if portal_params else lambda x: x
    transitions = [portal_dec(parse(token)) for token in tokens]
    return bfs((start, 0, (start,)),
               target,
               transitions,
               lambda state, target: state[0] == target)


def main():
    start = input()
    target = input()
    tokens = input().split(" ")
    possible_portal_params = input().split(" ")
    portal_params = ((int(possible_portal_params[0]), int(possible_portal_params[1]))
                     if len(possible_portal_params) == 2
                     else None)

    print(", ".join(func
                    for func, state
                    in insert_store_locs(search(start, target, tokens, portal_params))))


if __name__ == '__main__':
    # import doctest
    # doctest.testmod()
    main()
