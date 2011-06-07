# -*- coding: utf-8 -*-
'''
@module     keys
@author     Nicolas Paris <nicolas.caen@gmail.com
@licence    GPLv3
'''
import tyrs
import curses
from help import Help

class Keys:
    '''
    This class handle the main keysbinding, as the main method contain every
    keybinding, every case match a key to a method call, there is no logical
    here
    '''
    def __init__ (self):
        self.conf       = tyrs.container['conf']
        self.interface  = tyrs.container['interface']
        self.api        = tyrs.container['api']

    def handleKeyBinding (self):
        '''Should have all keybinding handle here'''
        while True:

            ch = self.interface.screen.getch()

            if self.interface.resize_event:
                self.interface.resize_event()

            # Down and Up key must act as a menu, and should navigate
            # throught every tweets like an item.
            #

            # DOWN
            if ch == self.conf.keys['down'] or ch == curses.KEY_DOWN:
                self.interface.move_down()
            # UP
            elif ch == self.conf.keys['up'] or ch == curses.KEY_UP:
                self.interface.move_up()
            # LEFT
            elif ch == self.conf.keys['left'] or ch == curses.KEY_LEFT:
                self.interface.navigate_buffer(-1)
            # RIGHT
            elif ch == self.conf.keys['right'] or ch == curses.KEY_RIGHT:
                self.interface.navigate_buffer(+1)
            # TWEET
            elif ch == self.conf.keys['tweet']:
                self.api.tweet(None)
            # RETWEET
            elif ch == self.conf.keys['retweet']:
                self.api.retweet()
            # RETWEET AND EDIT
            elif ch == self.conf.keys['retweet_and_edit']:
                self.api.retweet_and_edit()
            # DELETE TwEET
            elif ch == self.conf.keys['delete']:
                self.api.delete()
            # MENTIONS
            elif ch == self.conf.keys['mentions']:
                self.interface.change_buffer('mentions')
            # HOME TIMELINE
            elif ch == self.conf.keys['home']:
                self.interface.change_buffer('home')
            # CLEAR
            elif ch == self.conf.keys['clear']:
                self.interface.clear_statuses()
            # UPDATE
            elif ch == self.conf.keys['update']:
                self.interface.update_timeline(self.interface.buffer)
            # FOLLOW SELECTED
            elif ch == self.conf.keys['follow_selected']:
                self.api.follow_selected()
            # UNFOLLOW SELECTED
            elif ch == self.conf.keys['unfollow_selected']:
                self.api.unfollow_selected()
            # FOLLOW
            elif ch == self.conf.keys['follow']:
                self.api.follow()
            # UNFOLLOW
            elif ch == self.conf.keys['unfollow']:
                self.api.unfollow()
            # OPENURL
            elif ch == self.conf.keys['openurl']:
                self.interface.openurl()
            # BACK ON TOP
            elif ch == self.conf.keys['back_on_top']:
                self.interface.change_buffer(self.interface.buffer)
            # BACK ON BOTTOM
            elif ch == self.conf.keys['back_on_bottom']:
                self.interface.back_on_bottom()
            # REPLY
            elif ch == self.conf.keys['reply']:
                self.api.reply()
            # GET DIRECT MESSAGE
            elif ch == self.conf.keys['getDM']:
                self.interface.change_buffer('direct')
            # SEND DIRECT MESSAGE
            elif ch == self.conf.keys['sendDM']:
                self.api.send_direct_message()
            # SEARCH
            elif ch == self.conf.keys['search']:
                self.api.search()
            # SEARCH USER
            elif ch == self.conf.keys['search_user']:
                self.api.user_timeline()
            # SEARCH MYSELF
            elif ch == self.conf.keys['search_myself']:
                self.api.user_timeline(True)
            # Redraw screen
            elif ch == self.conf.keys['redraw']:
                self.interface.display_redraw_screen()
            # Help
            elif ch == ord('?'):
                Help()
            # Create favorite
            elif ch == self.conf.keys['fav']:
                self.api.set_favorite()
            # Get favorite
            elif ch == self.conf.keys['get_fav']:
                self.api.get_favorites()
            # Destroy favorite
            elif ch == self.conf.keys['delete_fav']:
                self.api.destroy_favorite()
            # QUIT
            # 27 corresponding to the ESC, couldn't find a KEY_* corresponding
            elif ch == self.conf.keys['quit'] or ch == 27:
                break

            self.interface.display_timeline()