import company
import player
import board

class SpacemonController:

    def __init__(self):
	self.company_manager = company.CompanyManager()
	self.player_manager = player.PlayerManager()
	self.board = board.SpacemonBoard()
	self.board.set_circles()
	self.board.set_select()

    def get_company(self, i):
	return self.company_manager.get_by_index(i)

    def get_board(self):
	return self.board

    def select_cell(self, x, y):
	if self.board.get_square(x, y) != 'SELECT':
            return False
	else:
            ## Do some selecting stuff!
            self.board.clear_select()
            self.board.set_diamond(x, y)
            result = self.resolve_new_diamond(x, y)
            has_grown, company_id, growth_val = result
            return True

    def resolve_new_diamond(self, x, y):
	companies = []
	diamonds = []
	circles = []

	squares = [(x-1, y), (x, y-1), (x+1, y), (x, y+1)]
	for xp, yp in squares:
            print "x={}, y={}, xp={}, yp={}".format(x, y, xp, yp)
            if self.board.is_diamond(xp, yp):
                diamonds.append((xp, yp))
            elif self.board.is_circle(xp, yp):
		circles.append((xp, yp))
            else:
            	c = self.board.is_company(xp, yp)
            	if c != False and c not in companies:
                    companies.append(c)

	# print "In 'resolve_new_diamond'"
	# print "len(companies) = {}".format(len(companies))
	# print "len(diamonds) = {}".format(len(diamonds))
	# print "len(circles) = {}".format(len(circles))

	if len(companies) >= 2:
            return self.handle_merger(companies, circles, diamonds)

	elif len(companies) == 1:
            company_id = companies[0]
            company = self.company_manager.get_by_id(company_id)
            squares = diamonds + [(x,y)]
            company.grow(len(squares), len(circles))
            val = self.board.assign_to_company(company_id, squares)
            return True, company_id, val

	else:
            ## just a rando diamond?
            if len(diamonds) == 0 and len(circles) == 0:
		return (False, '', 0)
            ## a new company!
            else:
		squares = diamonds + [(x,y)]
		player = self.player_manager.get_current()
		id = self.company_manager.create_new(len(squares), len(circles), player)
		val = self.board.assign_to_company(id, squares)
		#self.company_manager.get_by_id(id).change_user_shares(player.get_name(), NEW_INITIAL_SHARES)
		#player.earn_cash(val)
		return True, id, val

    def handle_merger(self, companies, circles, diamonds):
	print "Error: Merger handling unimplemented"
	exit(-1)

    def next_turn(self):
	self.player_manager.set_next_player()
	self.board.clear_select()
	self.board.set_select()
