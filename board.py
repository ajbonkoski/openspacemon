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

    def set_select(self, _allow_new_companies):
	assert len(self.select_sqr) == 0
	self.randomize(5, 5, 'SELECT',
		allow_new_companies=_allow_new_companies,
		notify_callback=lambda x,y: self.select_sqr.append((x,y)))

    def set_diamond(self, x, y):
	self.squares[y][x] = 'DIAMOND'

    def clear_select(self):
	for x,y in self.select_sqr:
	    if self.squares[y][x] == 'SELECT': ## still equal select?
            	self.squares[y][x] = 'NORMAL'
	self.select_sqr = []

    def is_adj_diamond(self, x, y):
	adj_cells = [(x-1, y), (x, y-1), (x+1, y), (x, y+1)]
	for xp, yp in adj_cells:
            if xp < 0 or xp >= COLS: continue
            if yp < 0 or yp >= ROWS: continue
            if self.squares[yp][xp] == 'DIAMOND':
		return True
	return False

    def is_adj_make_new_company(self, x, y):
	adj_cells = [(x-1, y), (x, y-1), (x+1, y), (x, y+1)]
	val = False
	for xp, yp in adj_cells:
            if xp < 0 or xp >= COLS: continue
            if yp < 0 or yp >= ROWS: continue
            if self.squares[yp][xp] == 'DIAMOND':
		val = True
            elif self.squares[yp][xp] == 'CIRCLE':
		val = True
            elif self.squares[yp][xp][:len('COMPANY')] == 'COMPANY':
		return False
	return val

    def randomize(self, min, max, type, allow_new_companies=True, notify_callback=None):
	num_circles = randint(min, max)
	for n in range(num_circles):
            while True:
            	x = randint(0, COLS-1)
            	y = randint(0, ROWS-1)
		if self.squares[y][x] != 'NORMAL':
                    continue
		if not allow_new_companies and self.is_adj_make_new_company(x, y):
                    continue
            	self.squares[y][x] = type
            	if notify_callback != None:
                    notify_callback(x, y)
		break

    def get_square(self, x, y):
	return self.squares[y][x]

    def assign_to_company(self, company_id, squares):
	val = 'COMPANY-{}'.format(company_id)
	for x,y in squares:
            self.squares[y][x] = val

    def relabel_companies(self, buyer_id, companies):
	companies_labels = ['COMPANY-{}'.format(c) for c in companies]
	buyer_label = 'COMPANY-{}'.format(buyer_id)
	for y in range(ROWS):
            for x in range(COLS):
		if self.squares[y][x] in companies_labels:
		    self.squares[y][x] = buyer_label

    def is_valid_square(self, x, y):
	return x >= 0 and x < COLS and y >= 0 and y < ROWS

    def is_some_type(self, x, y, type):
        if not self.is_valid_square(x, y):
            return False
        return self.squares[y][x] == type

    def is_diamond(self, x, y):
	return self.is_some_type(x, y, 'DIAMOND')

    def is_circle(self, x, y):
	return self.is_some_type(x, y, 'CIRCLE')

    def is_company(self, x, y):
        if not self.is_valid_square(x, y):
            return False
	sqr = self.squares[y][x]
	sqr_type = sqr.split('-')[0]
	sqr_rest = '-'.join(sqr.split('-')[1:])
        if sqr_type != 'COMPANY':
            return False
	## its a company! Extract the id
	return sqr_rest
