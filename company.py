
names = ["Atlantis Ltd.", "Betelguese", "Cannon Inc.", "Debenese", "Eridnus Corp."]
company_ids = ["atlantis-ltd", "betelguese", "cannon-inc", "debenese", "eridnus-corp"]
company_map = {}
for i in range(len(names)): company_map[company_ids[i]] = names[i]

INITIAL_SHARES = 5

class CompanyIndexOutOfRangeError(Exception): pass
class CompanyNewNotFoundError(Exception): pass

class CompanyManager:

    def __init__(self):
	self.companies = []
	for id in company_ids:
            self.companies.append(Company(id))

    def get_by_id(self, id):
	if id not in company_ids:
            raise CompanyIndexOutOfRangeError()
	i = company_ids.index(id)
	return self.companies[i]

    def get_by_index(self, i):
	if i >= len(self.companies):
            raise CompanyIndexOutOfRangeError()
	return self.companies[i]

    def can_make_new(self):
	open = False
	for c in self.companies:
            open = open or (not c.is_open())
	return open

    def create_new(self, num_squares, num_circles, player):
	company = None
	i = 0
	for c in self.companies:
            if not c.is_open():
		company = c
		break
            i += 1
	if i >= len(self.companies):
            raise CompanyNewNotFoundError()

	company.create_new(num_squares, num_circles, player)
	return company.get_id()

    def handle_merger(self, companies, num_squares, num_circles, player):
	companies.sort()
	companies_obj = [self.get_by_id(c) for c in companies]

	buyer = self.get_merge_priority(companies_obj)
	for company in companies_obj:
            if buyer == company: continue
            company.liquidate()
            buyer.merge_in(company)
            company.set_invalid()

	buyer.grow_merge_ext(num_squares, num_circles)
	return buyer.get_id()

    def get_merge_priority(self, companies):
	buyer = None
	buyer_size = 0
	for c in companies:
            c_size = c.get_size()
            if c_size > buyer_size:
		buyer = c
		buyer_size = c_size
	return buyer

class Company:

    def __init__(self, id):
	self.id = id
	assert(self.id in company_ids)
	self.set_invalid()

    def merge_in(self, company):
	for player, num_shares in company.owners.items():
            self.change_user_shares(player, num_shares)
        self.size += company.size
        self.price += company.price

    def grow_merge_ext(self, num_squares, num_circles):
        added_price = (num_squares + 5*num_circles)*100
	self.price += added_price
	self.size += num_squares

    def set_invalid(self):
	self.size = 0
	self.price = 0
	self.owners = {}

    def create_new(self, num_squares, num_circles, player):
	assert(self.size == 0)
	self.size = num_squares
	self.price = (num_squares + 5*num_circles)*100
	self.change_user_shares(player, INITIAL_SHARES)
	player.change_cash(self.price)

    def liquidate(self):
	for player, num_shares in self.owners.items():
            player.change_cash(num_shares * self.price)

    def is_open(self):
	return self.size != 0

    def get_name(self):
	return company_map[self.id]

    def get_id(self):
	return self.id

    def get_size(self):
	return self.size

    def grow(self, num_squares, num_circles, player):
	self.size += num_squares
	growth = (num_squares + 5*num_circles)*100
	self.price += growth
        player.change_cash(growth * self.get_users_shares(player))

    def inc_size_by(self, n):
	self.size += n

    def get_price(self):
	return self.price

    def get_largest_shareholder(self):
	largest = ('', -1)
	for key, value in self.owners.items():
            if value > largest[1]:
		largest = (key.get_name(), value)
	return largest

    def get_users_shares(self, player):
	if player not in self.owners:
            return 0
	else:
            return self.owners[player]

    def change_user_shares(self, player, amt):
	if player not in self.owners:
            self.owners[player] = 0
	self.owners[player] += amt

