import company
import player
import board

class SpacemonController:

    def __init__(self):
	self.company_manager = company.CompanyManager()
	self.player_manager = player.PlayerManager()
	self.board = board.SpacemonBoard()
	self.board.set_circles()
	self.board.set_select(True)

    def get_company(self, i):
	return self.company_manager.get_by_index(i)

    def get_board(self):
	return self.board

    def get_current_player(self):
	return self.player_manager.get_current()

    def select_cell(self, x, y):
	if self.board.get_square(x, y) != 'SELECT':
            return False
	else:
            ## Do some selecting stuff!
            self.board.clear_select()
            self.board.set_diamond(x, y)
            result = self.resolve_new_diamond(x, y)
            return True

    def current_player_buy_all(self, company_index):
	company = self.get_company(company_index)
	player = self.get_current_player()
	price = company.get_price()
	can_buy = player.can_buy_shares(price)
	self.player_change_shares(player, company, can_buy)

    def current_player_sell_all(self, company_index):
	company = self.get_company(company_index)
	player = self.get_current_player()
	num_shares = company.get_users_shares(player)
	self.player_change_shares(player, company, -num_shares)

    def player_change_shares(self, player, company, amt):
	try:
            ## check if the transaction is valid
            price_per_share = company.get_price()
            cost = price_per_share * amt
            if not player.has_cash(cost):
		return False
            shares_owned = company.get_users_shares(player)
            if amt < 0 and -amt > shares_owned:  ## trying to sell more than have?
		return False

            ## do the transaction
            company.change_user_shares(player, amt)
            player.change_cash(-cost)

            return True

	except Exception:
            return False

    def resolve_new_diamond(self, x, y):
	companies = []
	diamonds = []
	circles = []

	squares = [(x-1, y), (x, y-1), (x+1, y), (x, y+1)]
	for xp, yp in squares:
            if self.board.is_diamond(xp, yp):
                diamonds.append((xp, yp))
            elif self.board.is_circle(xp, yp):
		circles.append((xp, yp))
            else:
            	c = self.board.is_company(xp, yp)
            	if c != False and c not in companies:
                    companies.append(c)

	if len(companies) >= 2:
            player = self.player_manager.get_current()
            squares = diamonds + [(x,y)]
            buyer_id = self.company_manager.handle_merger(companies, len(squares), len(circles), player)
            self.board.relabel_companies(buyer_id, companies)
            self.board.assign_to_company(buyer_id, squares)
            return True

	elif len(companies) == 1:
            company_id = companies[0]
            company = self.company_manager.get_by_id(company_id)
            squares = diamonds + [(x,y)]
            player = self.player_manager.get_current()
            company.grow(len(squares), len(circles), player)
            val = self.board.assign_to_company(company_id, squares)
            return True

	else:
            ## just a rando diamond?
            if len(diamonds) == 0 and len(circles) == 0:
		return False
            ## a new company!
            else:
		squares = diamonds + [(x,y)]
		player = self.player_manager.get_current()
		id = self.company_manager.create_new(len(squares), len(circles), player)
		val = self.board.assign_to_company(id, squares)
		return True

    def next_turn(self):
	self.player_manager.set_next_player()
	self.board.clear_select()
	self.board.set_select(self.company_manager.can_make_new())
