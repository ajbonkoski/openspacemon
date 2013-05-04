import company
import board

class CompanyIndexOutOfRangeError(Exception): pass

class SpacemonController:

    def __init__(self):
	self.companies = []
	for name in company.names:
            self.companies.append(company.Company(name))

	self.board = board.SpacemonBoard()
	self.board.set_circles()
	self.board.set_select()

    def get_company(self, i):
	if i >= len(self.companies):
            raise CompanyIndexOutOfRangeError()
	return self.companies[i]

    def get_board(self):
	return self.board


    def select_cell(self, x, y):
	if self.board.get_square(x, y) != 'SELECT':
            return False
	else:
            ## Do some selecting stuff!
            self.board.clear_select()
            self.board.set_diamond(x, y)
            return True

    def next_turn(self):
	self.board.clear_select()
	self.board.set_select()
