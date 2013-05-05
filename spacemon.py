#!/usr/bin/env python

# example helloworld.py

import pygtk
pygtk.require('2.0')
import gtk
import sys

from company_dialog import *
from company import names as company_names
from controller import *

def main():
    ctrl = SpacemonController()
    SpaceMonopoly(ctrl).main()

class SpaceMonopoly:

    def hello(self, widget, data=None):
        print "Hello World"

    ## Callbacks
    def delete_event(self, widget, event, data=None):
        return False

    def destroy(self, widget, data=None):
        gtk.main_quit()

    def print_hello(self, w, data):
        print "Hello, World!"

    ## Real Stuff
    def make_main_menu(self, window, menu_items):
        accel_group = gtk.AccelGroup()
        self.item_factory = gtk.ItemFactory(gtk.MenuBar, "<main>", accel_group)
        self.item_factory.create_items(menu_items)
        window.add_accel_group(accel_group)
        return self.item_factory.get_widget("<main>")

    def company_button_clicked(self, widget, data=None):
	self.company_window.set_company(data)
	self.company_window.run()

    def on_finish_turn(self, widget, data=None):
	self.controller.next_turn()
	self.update()

    def gridcell_callback(self, x, y):

	result = self.controller.select_cell(x, y)
	if result == False:
            print "Error: didnt click on Blue Select Square..."
	else: ## register click on the GUI
            self.update()

    def __init__(self, controller):
	self.controller = controller

        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.connect("delete_event", self.delete_event)
        self.window.connect("destroy", self.destroy)
        main_vbox = gtk.VBox(False, 1) ## use vbox
        self.window.add(main_vbox)

	## Set up some other stuff
	self.company_window = CompanyWindow(self.window, self.controller)

        self.menubar = self.make_main_menu(self.window, (
            ( "/_File",         None,         None, 0, "<Branch>" ),
            ( "/File/_New",     "<control>N", self.print_hello, 0, None ),
            ( "/File/_Open",    "<control>O", self.print_hello, 0, None ),
            ( "/File/_Save",    "<control>S", self.print_hello, 0, None ),
            ( "/File/Save _As", None,         None, 0, None ),
            ( "/File/sep1",     None,         None, 0, "<Separator>" ),
            ( "/File/Quit",     "<control>Q", gtk.main_quit, 0, None ),
            ( "/_Options",      None,         None, 0, "<Branch>" ),
            ( "/Options/Test",  None,         None, 0, None ),
            ( "/_Help",         None,         None, 0, "<LastBranch>" ),
            ( "/_Help/About",   None,         None, 0, None ),
            )
	)

	self.bodybox = gtk.HBox(False, 1)
	self.sidebar = gtk.VBox(False, 1)

        main_vbox.pack_start(self.menubar, False, True, 0)
	main_vbox.pack_start(self.bodybox, False, True, 0)

	### Build the GU'Is body
	self.grid = SpacemonGrid(self.controller, self.gridcell_callback)
	self.bodybox.pack_start(self.grid, False, True, 0)
	self.bodybox.pack_start(self.sidebar, False, True, 10)

	## uild the Side Bar
	self.sidebar.set_spacing(5)
	self.money_box = gtk.Label("CASH")
	self.company_buttons = []
        for i, name in enumerate(company_names):
            b = gtk.Button(name)
            b.connect("clicked", self.company_button_clicked, i)
            self.company_buttons.append(b)
	self.finish_turn = gtk.Button("Finish Turn")
    	self.finish_turn.connect("clicked", self.on_finish_turn)

	## add to the sidebar
	self.sidebar.pack_start(gtk.Label(None), False, True, 0)
	self.sidebar.pack_start(self.money_box, False, True, 0)
	self.sidebar.pack_start(gtk.Label(None), False, True, 0)
        for b in self.company_buttons:
            self.sidebar.pack_start(b, False, True, 0)
	self.sidebar.pack_start(gtk.Label(None), False, True, 0)
	self.sidebar.pack_start(self.finish_turn, False, True, 0)

	## show it all off!
        self.window.show_all()

    def update(self):
	self.grid.update()
	self.window.show_all()

    def main(self):
        gtk.main()


GRIDCELL_SIZEX = 37
GRIDCELL_SIZEY = 40
class SpacemonGrid(gtk.EventBox):

    def __init__(self, controller, gridcell_click_callback):
	self.controller = controller
	self.gridcell_click_callback = gridcell_click_callback

	gtk.EventBox.__init__(self)
	self.set_size_request(592, 481)

	xmax, ymax = 16, 12
	self.table = gtk.Table(xmax, ymax)
	self.add(self.table)

	self.grid_cells = [[] for i in range(ymax)]
	for y in range(ymax):
            for x in range(xmax):
		block_widget = self.block_resource(x, y)
		self.grid_cells[y].append(block_widget)
		self.table.attach(block_widget, x, x+1, y, y+1)

	## Attach click event-handler
	self.connect ('button-press-event', self.click_callback)

	self.update()

    def click_callback(self, widget, event):
	x, y = event.x, event.y
	cell_x, cell_y = int(x/GRIDCELL_SIZEX), int(y/GRIDCELL_SIZEY)
	self.gridcell_click_callback(cell_x, cell_y)

    def get_type_by_coords(self, x, y):
	if y%2 == 0:
            if x%2 == 0:
                return 'red'
            else:
                return 'blue'
        else:
            if x%2 == 0:
                return 'blue'
            else:
                return 'red'

    def block_resource(self, x, y):
	return self.color_resource_helper('block', x, y)

    def circle_resource(self, x, y):
	return self.color_resource_helper('circle', x, y)

    def diamond_resource(self, x, y):
	return self.color_resource_helper('diamond', x, y)

    def select_resource(self, x, y):
	name = 'sel-big.png'
	return image_resource(name)

    def company_resource(self, x, y, name):
	fname = 'company-{0}'.format(name)
	return self.color_resource_helper(fname, x, y)

    def color_resource_helper(self, fname, x, y):
	color = self.get_type_by_coords(x, y)
	name = '{0}-{1}.png'.format(fname, color)
	return image_resource(name)

    def change_grid_loc(self, x, y, resource_callback, data=''):
        self.table.remove(self.grid_cells[y][x])
	if data != ''	:
            resource = resource_callback(x, y, data)
	else:
            resource = resource_callback(x, y)
	self.grid_cells[y][x] = resource
	self.table.attach(self.grid_cells[y][x], x, x+1, y, y+1)

    def update(self):
	resource_callbacks = \
		{'NORMAL':  self.block_resource,
		 'CIRCLE': self.circle_resource,
		 'SELECT': self.select_resource,
		 'DIAMOND': self.diamond_resource,
		 'COMPANY': self.company_resource
		}

       	board = self.controller.get_board()
	xmax, ymax = 16, 12
	for y in range(ymax):
            for x in range(xmax):
		sqr = board.get_square(x, y)
		sqr_type = sqr.split('-')[0]
		sqr_val = '-'.join(sqr.split('-')[1:])
		if sqr_type not in resource_callbacks:
                    sys.stderr.write("Error: Square type '{0}' not recognized".format(sqr))
		else:
                    resource = resource_callbacks[sqr_type]
                    self.change_grid_loc(x, y, resource, sqr_val)

def image_resource(fname):
    image = gtk.Image()
    image.set_from_file('resources/'+fname)
    return image

if __name__ == "__main__":
    try: main()
    except KeyboardInterrupt: pass
