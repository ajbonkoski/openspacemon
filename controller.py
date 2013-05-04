import company
import board

class CompanyIndexOutOfRangeError(Exception): pass

class SpacemonController:

    def __init__(self):
	self.companies = []
	for name in company.names:
            self.companies.append(company.Company(name))

	self.board = board.SpacemonBoard()
	self.board.randomize()

    def get_company(self, i):
	if i >= len(self.companies):
            raise CompanyIndexOutOfRangeError()
	return self.companies[i]

    def get_board(self):
	return self.board

