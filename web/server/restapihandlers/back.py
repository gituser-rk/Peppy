# Copyright 2023 Peppy Player peppy.player@gmail.com
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

from tornado.web import RequestHandler
from ui.state import State
from util.keys import KEY_BACK

class BackHandler(RequestHandler):
    def initialize(self, peppy):
        self.util = peppy.util
        self.config = peppy.util.config
        self.peppy = peppy

    def put(self):
        try:
            state = State()
            state.source = KEY_BACK
            self.peppy.go_back(state)
            self.peppy.screensaver_dispatcher.cancel_screensaver()
        except:
            self.set_status(500)
            return self.finish()
