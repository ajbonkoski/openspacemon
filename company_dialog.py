import pygtk
pygtk.require('2.0')
import gtk
from random import randint
from company import names as company_names
from util import *

class CompanyFrame(gtk.Frame):

    def __init__(self, controller, index):
	self.controller = controller
	self.index = index

	gtk.Frame.__init__(self)
	self.set_size_request(100, 300)

	self.vbox = gtk.VBox(False, 1)
	self.add(self.vbox)

	self.company_name = gtk.Label("COMPANY")
	self.vbox.pack_start(self.company_name)

	## Add info box
	self.info_table = gtk.Table(3, 2);
	self.vbox.pack_start(self.info_table)

	self.company_size_label = gtk.Label("Company Size:")
	self.company_size_label.set_justify(gtk.JUSTIFY_LEFT)
	self.info_table.attach(self.company_size_label, 0, 1, 0, 1)

	self.company_size_value = gtk.Label()
	self.company_size_value.set_justify(gtk.JUSTIFY_LEFT)
	self.info_table.attach(self.company_size_value, 1, 2, 0, 1)

	self.cost_of_shares = gtk.Label("Cost of Shares:")
	self.cost_of_shares.set_justify(gtk.JUSTIFY_LEFT)
	self.info_table.attach(self.cost_of_shares, 0, 1, 1, 2)

	self.cost_of_shares_value = gtk.Label()
	self.cost_of_shares_value.set_justify(gtk.JUSTIFY_LEFT)
	self.info_table.attach(self.cost_of_shares_value, 1, 2, 1, 2)

	self.major_shareholder = gtk.Label("Major Shareholder:")
	self.major_shareholder.set_justify(gtk.JUSTIFY_LEFT)
	self.info_table.attach(self.major_shareholder, 0, 1, 2, 3)

	self.major_shareholder_value = gtk.Label()
	self.major_shareholder_value.set_justify(gtk.JUSTIFY_LEFT)
	self.info_table.attach(self.major_shareholder_value, 1, 2, 2, 3)

    	self.vbox.pack_start(gtk.HSeparator())

	## Build "sell" section
	self.your_shares = gtk.Label("You have 2034 shares")
	self.vbox.pack_start(self.your_shares)

	self.sell_hbox = gtk.HBox(False, 10)
	self.vbox.pack_start(self.sell_hbox)

	self.sell_all_button = gtk.Button("Sell All")
	self.sell_hbox.pack_start(self.sell_all_button)

	self.sell_button = gtk.Button("Sell >>>")
	self.sell_hbox.pack_start(self.sell_button)

	self.sell_quantity = gtk.Entry()
	self.sell_hbox.pack_start(self.sell_quantity)


    	self.vbox.pack_start(gtk.HSeparator())

	## Build "sell" section
	self.you_can_buy = gtk.Label("You can buy 10 shares")
	self.vbox.pack_start(self.you_can_buy)

	self.buy_hbox = gtk.HBox(False, 10)
	self.vbox.pack_start(self.buy_hbox)

	self.buy_all_button = gtk.Button("Buy All")
	self.buy_hbox.pack_start(self.buy_all_button)

	self.buy_button = gtk.Button("Buy >>>")
	self.buy_hbox.pack_start(self.buy_button)

	self.buy_quantity = gtk.Entry()
	self.buy_hbox.pack_start(self.buy_quantity)

    def set_size(self, n):
	s = "{0} Square" if n == 1 else "{0} Squares"
	self.company_size_value.set_text(s.format(n))

    def set_price(self, n):
	self.cost_of_shares_value.set_text('$'+format_number(',', n))

    def set_largest_shareholder(self, name, n):
	is_valid = n != -1
	shares = '{0} share' if n == 1 else '{0} shares'
	n_fmt = format_number(',', n)
	s = '{0} with {1}.'.format(name, shares.format(n_fmt)) if is_valid else 'Nobody.'
	self.major_shareholder_value.set_text(s)

    def set_users_shares(self, n):
	shares = '{0} share' if n == 1 else '{0} shares'
	n_fmt = format_number(',', n)
	s = 'You have {0}.'.format(shares.format(n_fmt))
	self.your_shares.set_text(s)

    def update(self):
	company = self.controller.get_company(self.index)
	self.company_name.set_text(company.get_name())
	self.set_size(company.get_price())
	self.set_price(company.get_price())
	name, n = company.get_largest_shareholder()
	self.set_largest_shareholder(name, n)
	self.set_users_shares(company.get_users_shares('AJB'))

class CompanyWindow:

    def make_frame(self, controller, i):
	return CompanyFrame(controller, i)

    def __init__(self, parent, controller=None):
	self.controller = controller
	self.notebook = gtk.Notebook()
	self.notebook.set_tab_pos(gtk.POS_TOP)
	self.company_frames = []
	for i, name in enumerate(company_names):
            self.company_frames.append(self.make_frame(controller, i))
            self.notebook.append_page(self.company_frames[i], gtk.Label(name))
	self.notebook.show()
	self.dialog = gtk.Dialog("Company Dialog",
                 	parent,
                    	gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
                    	(gtk.STOCK_OK, gtk.RESPONSE_ACCEPT))

        self.dialog.vbox.pack_start(self.notebook)


    def run(self):
	self.update()
	self.dialog.show_all()
	response = self.dialog.run()
	self.dialog.hide_all()

    def set_company(self, n):
	self.notebook.set_current_page(n)

    def update(self):
	for frame in self.company_frames:
            frame.update()

if __name__ == '__main__':
    c = CompanyWindow()
    c.run()
