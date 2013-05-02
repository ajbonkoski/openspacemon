import company

class CompanyIndexOutOfRangeError(Exception): pass

class SpacemonController:

    def __init__(self):
	self.companies = []
	for name in company.names:
            self.companies.append(company.Company(name))

    def get_company(self, i):
	if i >= len(self.companies):
            raise CompanyIndexOutOfRangeError()
	return self.companies[i]

