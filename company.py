
names = ["Atlantis Ltd.", "Betelguese", "Cannon Inc.", "Debenese", "Eridnus Corp."]
company_ids = ["atlantis-ltd", "betelguese", "cannon-inc", "debenese", "eridnus-corp"]
company_map = {}
for i in range(len(names)): company_map[company_ids[i]] = names[i]

class CompanyIndexOutOfRangeError(Exception): pass
class CompanyNewNotFound(Exception): pass

class CompanyManager:

    def __init__(self):
	self.companies = []
	for id in company_ids:
            self.companies.append(Company(id))

    def get_by_id(self, id):
	print "get_by_id: id={}".format(id)
	if id not in company_ids:
            raise CompanyIndexOutOfRangeError()
	i = company_ids.index(id)
	return self.companies[i]

    def get_by_index(self, i):
	if i >= len(self.companies):
            raise CompanyIndexOutOfRangeError()
	return self.companies[i]

    def create_new(self, num_squares, num_circles):
	company = None
	i = 0
	for c in self.companies:
            if not c.is_open():
		company = c
		break
            i += 1
	if i >= len(self.companies):
            raise CompanyNewNotFoundError()

	company.create_new(num_squares, num_circles)
	return company.get_id()

class Company:

    def __init__(self, id):
	self.id = id
	assert(self.id in company_ids)
	self.set_invalid()

    def set_invalid(self):
	self.size = 0
	self.price = 0
	self.owners = {}

    def create_new(self, num_squares, num_circles):
	assert(self.size == 0)
	self.size = num_squares
	self.price = (num_squares + 5*num_circles)*100

    def is_open(self):
	return self.size != 0

    def get_name(self):
	return company_map[self.id]

    def get_id(self):
	return self.id

    def get_size(self):
	return self.size

    def grow(self, num_squares, num_circles):
	self.size += num_squares
	self.price += (num_squares + 5*num_circles)*100

    def inc_size_by(self, n):
	self.size += n

    def get_price(self):
	return self.price

    def get_largest_shareholder(self):
	largest = ('', -1)
	for key, value in self.owners.items():
            if value > largest[1]:
		largest = (key, value)
	return largest

    def get_users_shares(self, name):
	if name not in self.owners:
            return 0
	else:
            return self.owners[name]
