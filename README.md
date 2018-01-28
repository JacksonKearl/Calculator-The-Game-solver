## Solver for Calculator: The Game

Pathfinding solver for [Calculator: The Game](http://www.simplemachine.co/game/calculator-the-game/) by [Simple Machine](http://www.simplemachine.co).

Supports the enitre game's set of features (including memory, portals, and self-modifying buttons).
<img src="https://raw.githubusercontent.com/JacksonKearl/Calculator-The-Game-solver/master/Game.jpeg" width="200">
![Use](https://raw.githubusercontent.com/JacksonKearl/Calculator-The-Game-solver/master/Use.png)
### Use
From terminal:
```
$ python3 main.py
```

The script will then prompt you for your starting number, target number, keys available, and portal locations (if there are no portals, just leave the last line blank).

The syntax for keys is as follows:

(N and M represent arbitrary integers)

| Name             | Format             | Description                                                                                |
| ---------------- | ------------------ | ------------------------------------------------------------------------------------------ |
| Arithmetic       | *N, /N, +N, -N, ^N | Standard arithmetic                                                                        |
| Digit Entry      | N                  | Inserts new characters to the right of the screen                                          |
| Delete           | <<                 | Deletes the rightmost digit from the screen                                                |
| Sum              | +                  | Replaces the screen with the sum of each digit*                                            |
| Negate           | -                  | Perform a simple sign swap                                                                 |
| Reverse          | R                  | Replace the contents of the screen with themselves backwards*                              |
| Mirror           | M                  | Similar to Reverse, but right append the backwards contents                                |
| Load/Store       | S                  | Save the contents of screen to memory freely. Recall and append left for price of one turn |
| Invert           | I                  | Replace all numbers with their 10's complement (0 stays 0)                                 |
| Shift Left       | <                  | Rotate screen left (MSD becomes LSD, rest shift over)*                                     |
| Shift Right      | >                  | Rotate screen right (LSD becomes MSD, rest shift over)*                                    |
| Find and Replace | N=>M               | Replace all instances of N with M                                                          |
| Alter Buttons    | [+]N               | Increments the value of all Arithmetic and Digit Entry buttons by N each press             |

\*Limited in-game support for these operators when in "floating point" mode. I have attempted to replicate the game mechanics in these cases, at the expense of logic and sweet paths.

Additionally, for the later stages (round 180+), I provide the ability to enter the location of portals. These are entered as zero indexed integers, reading from the right of the screen. First enter the "bottom", followed by the "top".

### Technical Details
As much as possible I attempt to mirror the game mechanics exactly. This includes limiting all intermediary values to at most one decimal point (any more and the game throws an error), restricting the ability to call the Sum operator on decimals, and implementing various other limitations the game faces.

I rely heavily on decorators to help maintain coherent internal state. Each of the "key" functions in keys.py is wrapped with at least a few decorators, to do everything from maintain a proper history state list in the state objects, to normalizing all intermediary values and restricting all the values disallowed in the game (length over 6 characters, multiple decimal places, etc.), to allowing me to treat the state tuple as a mutable list for more convenient changes of individual items.

I try to make as much use of doctest's as possible. This was inconvinient at times when I needed to rewrite small components of state formatting and eneded up needing to change all the dectests, but they were in the end worthwhile for traking down bugs. 

The meat of the search itself takes place in searchers.py, where I implement a standard breadth first search. In this case, the nodes are state values of the form:
```
(screen_contents, number_of_[+]_button_increments, (states_since_last_load...,))
```
And edges are given by passing the node to an array of "key" functions, which simulate the pysical keys provided on the calculator.

The `number_of_[+]_button_increments` is modified whenever a `[+]` key is pressed, and changes the behavior and rendering of all the Arithmetic and Digit Entry buttons. 

`states_since_last_load` is a tuple of all the `screen_contents` that could possibly be stored in the memory at the time. This gets reset each time memory is used, as there may only be one item in memory at a time.

The largest rewrite needed by far was when implementing the `[+]` button, as I could no longer use a single string for state, but instead hat to switch to a tuple to keep track of all the different components of state. The automated testing via `doctest` helped ensure correctness in this change, but some mypy style typing would have been nice to have.

Handling of the Load button required the largest change to the script, as it meant that key functions could now not only return a singe state for each passed state,
but rather an entire list of them. This required modifications to the BFS algorithm to accommodate the variable transition function output formats.
