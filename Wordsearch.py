from getopt import getopt, GetoptError
from math import sqrt
from random import choice, randint
from sys import argv, exit, stderr

def show_grid(grid, words):
    grid_size = int(sqrt(len(grid)))

    for row in range(grid_size):
        for column in range(grid_size):
            print(grid[row * grid_size + column], ' ' , end = '')

        if row < len(words):
            print('        ', words[row], end = '')

        print()

def fill_grid(grid):
    for r in range(len(grid)):
        grid[r] = grid[r] == ' ' and chr(randint(ord('A'), ord('Z'))) or grid[r]

def try_word(grid, word, x, y, route):
    grid_size = int(sqrt(len(grid)))
    grid_copy = []

    for g in grid:
        grid_copy.append(g)

    for c in word:
        if grid_copy[y * grid_size + x] != ' ' and grid_copy[y * grid_size + x] != c:
            return False

        grid_copy[y * grid_size + x] = c
        x += route[0]
        y += route[1]

    for i in range(len(grid)):
        grid[i] = grid_copy[i]
    
    return True

def add_word_to_grid(grid, word):
    status = False
    count = 0   
    direction = [(0, 1), (0, -1), (1, 0), (-1, 0), (-1, 1), (1, -1), (1, 1), (-1, -1)]
    grid_size = int(sqrt(len(grid)))

    while not status and count < 100:
        route = choice(direction)

        if route == (0, 1): # n-s
            rand_x = randint(0, grid_size - 1)
            rand_y = randint(0, grid_size - len(word))
            status = try_word(grid, word, rand_x, rand_y, route)
        elif route == (0, -1): # s-n
            rand_x = randint(0, grid_size - 1)
            rand_y = randint(len(word), grid_size - 1)
            status = try_word(grid, word, rand_x, rand_y, route)
        elif route == (1, 0): # w-e
            rand_x = randint(0, grid_size - len(word))
            rand_y = randint(0, grid_size - 1)
            status = try_word(grid, word, rand_x, rand_y, route)
        elif route == (-1, 0): # e-w
            rand_x = randint(len(word), grid_size - 1)
            rand_y = randint(0, grid_size - 1)
            status = try_word(grid, word, rand_x, rand_y, route)
        elif route == (-1, 1): # ne-sw
            rand_x = randint(len(word), grid_size - 1)
            rand_y = randint(0, grid_size - len(word))
            status = try_word(grid, word, rand_x, rand_y, route)
        elif route == (1, -1): # sw-ne
            rand_x = randint(0, grid_size - len(word))
            rand_y = randint(len(word), grid_size - 1)
            status = try_word(grid, word, rand_x, rand_y, route)
        elif route == (1, 1): # nw-se
            rand_x = randint(0, grid_size - len(word))
            rand_y = randint(0, grid_size - len(word))
            status = try_word(grid, word, rand_x, rand_y, route)
        else: # se-nw
            rand_x = randint(len(word), grid_size - 1)
            rand_y = randint(len(word), grid_size - 1)
            status = try_word(grid, word, rand_x, rand_y, route)

        count += 1

    if count == 100:
        print(argv[0], ': Dropping word', word, "as can't fit in grid after trying 100 random positions. Try a larger grid.", file = stderr)
        return False

    return True

def read_words_file(filename):
    try:
        with open(filename, 'r') as words_file:
            return words_file.read().splitlines()
    except FileNotFoundError:
        print(argv[0], ': File', filename, 'not found. Quitting.', file = stderr)
        exit(1)

def main():
    if len(argv) < 2:
        print('Usage:', argv[0], '[-g GRID_SIZE] FILE', file = stderr)
        exit(2)
    
    try:
        opts, args = getopt(argv[1:], "g:")
    except GetoptError as err:
        print(argv[0], ':', err)
        exit(3)

    grid_size = 20

    for o, a in opts:
        if o == "-g":
            try:
                grid_size = int(a)
            except ValueError as err:
                print(argv[0], ':', a, "isn't a number.")
                exit(4)
        else:
            print(argv[0], ': Unknown option. Quitting.', file = stderr)
            exit(5)

    words = read_words_file(args[0])

    if grid_size < len(words):
        grid_size = len(words)
        print(argv[0], ': Increasing grid size to', grid_size, 'as there are too many words for current size.', file = stderr)

    grid =  [' '] * grid_size * grid_size
    words_to_remove = []

    for word in words:
        if len(word) >= grid_size:
            print(argv[0], ': Dropping word', word, "as it's too long.", file = stderr)
            words_to_remove.append(word)
        else:
            if not add_word_to_grid(grid, word):
                words_to_remove.append(word)

    for word in words_to_remove:
        words.remove(word)

    if (len(words) == 0):
        exit(0)

    fill_grid(grid)
    show_grid(grid, words)

if __name__ == "__main__":
    main()

