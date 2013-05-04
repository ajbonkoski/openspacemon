from random import randint
ROWS = 12
COLS = 16

class SpacemonBoard:

    def __init__(self):
	self.squares = []
	for y in range(ROWS):
            self.squares.append([])
            for x in range(COLS):
		self.squares[y].append('NORMAL')

    def randomize(self):
	num_circles = randint(1,10)
	for n in range(num_circles):
            x = randint(0, COLS-1)
            y = randint(0, ROWS-1)
            self.squares[y][x] = 'CIRCLE'

    def get_square(self, x, y):
	return self.squares[y][x]

