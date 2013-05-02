
names = ["Atlantis Ltd.", "Betelguese", "Cannon Inc.", "Debenese", "Eridnus Corp."]

class Company:

    def __init__(self, name):
	self.name = name
	self.set_invalid()

    def set_invalid(self):
	self.size = 0
	self.price = 0
	self.owners = {'AJB': 100, 'JKL': 10000}

    def get_name(self):
	return self.name

    def get_size(self):
	return self.size

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
