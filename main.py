#! /usr/local/bin/python3
from keys import shift, rev, mult, summer, rep, add, sub, div, dir, pow, rotL, rotR, mirror, inc, negate, paste
from searchers import bfs


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


def search(start, target, tokens):
    '''
    >>> search('1', '83', ['*9', '+2'])
    [('*9', ('9', 0, ('1', '9'))), ('*9', ('81', 0, ('1', '9', '81'))), ('+2', ('83', 0, ('1', '9', '81', '83')))]
    >>> search('0', '6', ['+5', '[+]1'])
    [('[+]1', ('0', 1, ('0', '0'))), ('+6', ('6', 1, ('0', '0', '6')))]
    '''
    transitions = [parse(token) for token in tokens]
    return bfs((start, 0, (start,)),
               target,
               transitions,
               lambda state, target: state[0] == target)


def main():
    start = input()
    target = input()
    tokens = input().split(" ")
    print(", ".join(func for func, state in search(start, target, tokens)))


if __name__ == '__main__':
    import doctest
    doctest.testmod()
    main()
