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

	self.select_sqr = []

    def set_circles(self):
	self.randomize(1, 10, 'CIRCLE')

    def set_select(self):
	assert len(self.select_sqr) == 0
	self.randomize(5, 5, 'SELECT', lambda x,y: self.select_sqr.append((x,y)))

    def set_diamond(self, x, y):
	self.squares[y][x] = 'DIAMOND'

    def clear_select(self):
	for x,y in self.select_sqr:
	    if self.squares[y][x] == 'SELECT': ## still equal select?
            	self.squares[y][x] = 'NORMAL'
	self.select_sqr = []

    def randomize(self, min, max, type, notify_callback=None):
	num_circles = randint(min, max)
	for n in range(num_circles):
            while True:
            	x = randint(0, COLS-1)
            	y = randint(0, ROWS-1)
		if self.squares[y][x] != 'NORMAL':
                    continue
            	self.squares[y][x] = type
            	if notify_callback != None:
                    notify_callback(x, y)
		break

    def get_square(self, x, y):
	return self.squares[y][x]

