#!/usr/bin/env python

# example helloworld.py

import pygtk
pygtk.require('2.0')
import gtk
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
	self.grid = SpacemonGrid()
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

    def __init__(self):
	gtk.Frame.__init__(self)
	self.set_size_request(592, 481)

	block_blue = 'block-blue.png'
	block_red = 'block-red.png'
	self.circle = image_resource('circle.png')

	xmax, ymax = 16, 12
	self.table = gtk.Table(xmax, ymax)
	self.add(self.table)
	i = 0
	for y in range(ymax):
            for x in range(xmax):
		if y%2 == 0:
                    if x%2 == 0:
			block = block_red
                    else:
			block = block_blue
		else:
                    if x%2 == 0:
			block = block_blue
                    else:
			block = block_red
		self.set_grid_loc(x, y, block)

    def set_grid_loc(self, x, y, fname):
	self.table.attach(image_resource(fname), x, x+1, y, y+1)


def image_resource(fname):
    image = gtk.Image()
    image.set_from_file('resources/'+fname)
    return image

if __name__ == "__main__":
    try: main()
    except KeyboardInterrupt: pass
