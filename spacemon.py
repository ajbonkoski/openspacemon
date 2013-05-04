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
	self.grid = SpacemonGrid(self.controller)
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

    def main(self):
        gtk.main()



class SpacemonGrid(gtk.Frame):

    def __init__(self, controller):
	self.controller = controller

	gtk.Frame.__init__(self)
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

	self.update()

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
	color = self.get_type_by_coords(x, y)
	name = 'block-{0}.png'.format(color)
	return image_resource(name)

    def circle_resource(self, x, y):
	color = self.get_type_by_coords(x, y)
	name = 'circle-{0}.png'.format(color)
	return image_resource(name)

    def change_grid_loc(self, x, y, resource_callback):
        self.table.remove(self.grid_cells[y][x])
	self.grid_cells[y][x] = resource_callback(x, y)
	self.table.attach(self.grid_cells[y][x], x, x+1, y, y+1)

    def update(self):
	resource_callbacks = \
		{'NORMAL':  self.block_resource,
		 'CIRCLE': self.circle_resource}

       	board = self.controller.get_board()
	xmax, ymax = 16, 12
	for y in range(ymax):
            for x in range(xmax):
		sqr = board.get_square(x, y)
		if sqr not in resource_callbacks:
                    print >> sys.stderr ("Error: Square type '{0}' not recognized".format(sqr))
		else:
                    resource = resource_callbacks[sqr]
                    self.change_grid_loc(x, y, resource)

def image_resource(fname):
    image = gtk.Image()
    image.set_from_file('resources/'+fname)
    return image

if __name__ == "__main__":
    try: main()
    except KeyboardInterrupt: pass
