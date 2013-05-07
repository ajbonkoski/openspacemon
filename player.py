
INITIAL_CASH = 6000

class PlayerNotFoundException(Exception): pass
class PlayerManager:

    def __init__(self):
	self.players = []
	self.players.append(Player("AJB"))
	self.current_player = 0

    def get_current(self):
	return self.players[self.current_player]

    def set_next_player(self):
	self.current_player += 1
	self.current_player %= len(self.players)

    def get_by_name(self, player_name):
	for player in self.players:
            if player.get_name() == player_name:
		return player
	raise PlayerNotFoundException()

class PlayerDoesntHaveEnoughCashError(Exception): pass
class Player:

    def __init__(self, name):
	self.name = name
	self.cash = INITIAL_CASH

    def has_cash(self, amt):
	return amt <= self.cash

    def change_cash(self, amt):
	if not self.has_cash(-amt):
            raise PlayerDoesntHaveEnoughCashError()
	self.cash += amt

    def get_cash(self):
	return self.cash

    def can_buy_shares(self, share_cost):
	return int(self.cash/share_cost)

    def get_name(self):
	return self.name

