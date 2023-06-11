# Copyright 2016-2023 Peppy Player peppy.player@gmail.com
# 
# This file is part of Peppy Player.
# 
# Peppy Player is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# Peppy Player is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with Peppy Player. If not, see <http://www.gnu.org/licenses/>.

from ui.screen.menuscreen import MenuScreen
from ui.navigator.book import BookNavigator
from ui.menu.bookcyrillicmenu import BookCyrillicMenu, CHAR_ROWS, CHAR_COLUMNS
from util.keys import KEY_CHOOSE_AUTHOR, LABELS, KEY_PAGE_DOWN, KEY_PAGE_UP

class BookAbc(MenuScreen):
    """ Abc screen """
    
    def __init__(self, util, listeners, go_authors, d):
        """ Initializer
        
        :param util: utility object
        :param listeners: screen listeners
        :param go_authors: callback
        :param d: dictionary with menu button flags 
        """ 
        MenuScreen.__init__(self, util, listeners, CHAR_ROWS, CHAR_COLUMNS, d)

        self.navigator = BookNavigator(util, self.layout.BOTTOM, listeners, d[4])
        self.left_button = self.navigator.get_button_by_name(KEY_PAGE_DOWN)
        self.right_button = self.navigator.get_button_by_name(KEY_PAGE_UP)
        self.left_button.change_label(str(0))
        self.right_button.change_label(str(0))
        self.add_navigator(self.navigator)

        self.abc_menu = BookCyrillicMenu(self.util, go_authors, (0, 0, 0, 0), self.menu_layout)            
        self.screen_title.set_text(self.config[LABELS][KEY_CHOOSE_AUTHOR])
        self.set_menu(self.abc_menu)

        self.link_borders()
   
    def add_screen_observers(self, update_observer, redraw_observer):
        """ Add screen observers
        
        :param update_observer: observer for updating the screen
        :param redraw_observer: observer to redraw the whole screen
        """
        self.navigator.add_observers(update_observer, redraw_observer)
        self.abc_menu.add_menu_loaded_listener(redraw_observer)
        self.abc_menu.add_menu_observers(update_observer, redraw_observer, release=False)
        