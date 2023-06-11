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

from ui.screen.screen import Screen, PERCENT_TOP_HEIGHT
from ui.menu.homemenu import HomeMenu
from ui.screen.menuscreen import MenuScreen
from ui.navigator.home import HomeNavigator
from util.util import KEY_HOME
from util.keys import KEY_MODE

class HomeScreen(Screen):
    """ Home Screen """
    
    def __init__(self, util, listeners):
        """ Initializer
        
        :param util: utility object
        :param listener: screen menu event listener
        """
        Screen.__init__(self, util, KEY_HOME, PERCENT_TOP_HEIGHT)
        
        self.home_menu = HomeMenu(util, None, self.layout.CENTER)
        self.home_menu.add_listener(listeners[KEY_MODE]) 
        self.add_menu(self.home_menu)
        
        self.navigator = HomeNavigator(util, self.layout.BOTTOM, listeners)
        self.add_navigator(self.navigator)

        self.link_borders()

        if self.home_menu.get_selected_item() == None:
            length = len(self.navigator.components)
            if length > 0:
                b = self.navigator.components[length - 1]
                b.set_selected(True)

    def add_screen_observers(self, update_observer, redraw_observer):
        """ Add screen observers
        
        :param update_observer: observer for updating the screen
        :param redraw_observer: observer to redraw the whole screen
        """
        Screen.add_screen_observers(self, update_observer, redraw_observer)
        
        self.home_menu.add_menu_observers(update_observer, redraw_observer)
        self.navigator.add_observers(update_observer, redraw_observer)

    def handle_event(self, event):
        """ Handle screen event

        :param event: the event to handle
        """
        MenuScreen.handle_event_common(self, event)
