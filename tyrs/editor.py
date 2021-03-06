# -*- coding: utf-8 -*-
# Copyright © 2011 Nicolas Paris <nicolas.caen@gmail.com>
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import tyrs
import curses
import curses.textpad

class Editor(object):

    confirm = False
    content = ''

    def __init__(self, data=None):
        self.conf = tyrs.container['conf']
        self.interface = tyrs.container['interface'] 
        self.data   = data
        self.init_win()

        self.start_edit()
        self.win.erase()
        curses.curs_set(0)

    def init_win(self):
        curses.curs_set(1)
        self.set_window_size()

        win = self.interface.screen.subwin(
                self.size['height'], self.size['width'],
                self.size['start_y'], self.size['start_x'])

        win.border(0)
        counter = self.count_chr()
        header = ' %s %s ' % (self.params['header'], str(counter))

        #TODO this doen't take bold
        win.addstr(0, 3, header.encode(self.interface.charset), curses.color_pair(self.conf.colors['header']['c']))
        self.win = win
        self.win.keypad(1)

    def set_window_size(self):
        maxyx = self.interface.screen.getmaxyx()

        # Set width
        if maxyx[1] > self.params['width']:
            width = self.params['width']
        else:
            width = maxyx[1] - 4 # 4: leave 2pix on every side at least

        # Set height
        height = int(self.params['char'] / width) + 4

        # Start of EditWin, display in the middle of the main screen
        start_y = maxyx[0]/2 - int(height/2)
        start_x = maxyx[1]/2 - int(width/2)
        self.sizeyx = (height, width)

        self.size = {
                'height': height, 'width': width,
                'start_y': start_y, 'start_x': start_x
        }


    def start_edit(self):

        self.interface.refresh_token = True
        if self.data:
            self.content = self.data.encode('utf-8')
            self.refresh()

        self.maxyx = self.win.getmaxyx()

        while True:
            ch = self.win.getch()
            if ch == curses.KEY_UP or ch == curses.KEY_DOWN \
                    or ch == curses.KEY_LEFT or ch == curses.KEY_RIGHT:
                continue

            elif ch == 10:          # ENTER: send the tweet
                self.confirm = True
                break

            elif ch == 27:        # ESC: abord
                self.content = None
                break

            elif ch == 127 or ch == curses.KEY_BACKSPACE:       # DEL
                if len(self.content) > 0:
                    self.content = self.content[:-1]
            else:
                self.content += chr(ch)

            self.refresh()
        self.interface.refresh_token = False

    def refresh(self):
        self.win.erase()
        self.init_win()
        self.display_content()
        self.win.refresh()

    def display_content(self):
        x = 2
        y = 2
        words = self.content.split(' ')
        max = self.win.getmaxyx()
        for w in words:
            if x+len(w) > max[1] - 4:
                y += 1
                x = 2
            self.win.addstr(y, x, w, self.interface.get_color('text'))
            x += len(w)+1


    def count_chr(self):
        i = 0
        token = False
        for ch in self.content:
            if not token:
                i += 1
                if not ord(ch) <= 128:
                    token = True
            else:
                token = False
        return i

class TweetEditor(Editor):
    params = {'char': 200, 'width': 80, 'header': _("What's up?")}

class NickEditor(Editor):
    params = {'char': 40, 'width': 40, 'header': _("Entry a name")}

class SearchEditor(Editor):
    params = {'char': 40, 'width': 40, 'header': _("Search for something?")}
