#! /usr/local/bin/python3
from keys import shift, rev, mult, summer, rep, add, sub, div, dir, pow, rotL, rotR, mirror
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
    elif token == "<":
        out = rotL()
    elif token == ">":
        out = rotR()
    elif token == "-":
        out = mult(-1)
    elif token == "+":
        out = summer()
    elif "=>" in token:
        old, new = token.split("=>")
        out = rep(old, new)
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

    out.__str__ = token
    return out


def search(start, target, tokens):
    transitions = [parse(token) for token in tokens]
    return bfs(start, target, transitions)


def main():
    start = input()
    target = input()
    tokens = input().split(" ")
    print(", ".join(func for func, state in search(start, target, tokens)))


def test(start, target, tokens):
    '''
    >>> test('1', '89', ['*9', '+2'])
    *9, *9, +2, +2, +2, +2
    '''
    print(", ".join(func for func, state in search(start, target, tokens)))


if __name__ == '__main__':
    # import doctest
    # doctest.testmod()
    main()
