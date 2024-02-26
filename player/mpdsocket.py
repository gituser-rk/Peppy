# Copyright 2016-2024 Peppy Player peppy.player@gmail.com
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

import os
import threading
import logging
import time
import urllib

from player.baseplayer import BasePlayer
from player.mpdconnection import MpdConnection
from player.mpdcommands import CLEAR, ADD, PLAY, STOP, PAUSE, RESUME, \
    SET_VOLUME, GET_VOLUME, MUTE_2, STATUS, CURRENT_SONG, IDLE, SEEKCUR, EOL, COMMAND_LIST_BEGIN, COMMAND_LIST_END, UPDATE
from player.player import Player
from util.fileutil import FILE_PLAYLIST, FILE_AUDIO
from util.config import RADIO, AUDIO_FILES, AUDIOBOOKS, STREAM, PODCASTS, ARCHIVE, YA_STREAM, COLLECTION

class Mpdsocket(BasePlayer):
    """ This class extends base player and provides communication with MPD process using TCP/IP socket """
        
    def __init__(self):
        """ Initializer. Starts separate thread for listening MPD events """
        
        BasePlayer.__init__(self);  
        self.host = "localhost"
        self.port = 6600  # this is default MPD port. If it was changed in mpd.conf it should be changed here as well
        self.muted = False
        self.playing = True
        self.conn = None
        self.dont_parse_track_name = False
        self.current_volume_level = "-1"
        self.current_playlist_url = None
        self.current_file_url = None
    
    def set_proxy(self, proxy_process, proxy=None):
        """ mpd socket client doesn't use proxy """
        
        pass
    
    def start_client(self):
        """ Start client thread """
        
        self.conn = MpdConnection(self.host, self.port)
        self.conn.connect()
        thread = threading.Thread(target=self.mpd_event_listener)
        thread.start()
        self.conn.command(UPDATE + EOL)

    def stop_client(self):
        """ Stop thread """

        with self.lock:
            self.playing = False
       
    def mpd_event_listener(self):
        """ Starts the loop for listening MPD events """
        
        while self.playing:
            c = MpdConnection(self.host, self.port, reader_flags='r', encoding=None)
            c.connect()

            if not c.writer:
                continue
            
            c.writer.write(IDLE + "\n")
            c.writer.flush()
            
            line = None
            try:        
                line = c.reader.readline()  # blocking line
                logging.debug("line from idle: " + line) 
            except Exception as e:
                logging.debug(e)
            
            if line and "mixer" in line:
                volume = self.get_volume()
                self.notify_volume_listeners(volume)
                continue
            
            self.dispatch_callback(line)
            c.disconnect()
                
    def dispatch_callback(self, line):
        """ Callback dispatcher
        
        :line: line from idle command
        """
        streams = [RADIO, STREAM]
        timed_streams = [AUDIOBOOKS, PODCASTS, ARCHIVE, YA_STREAM]
        audio_files = [AUDIO_FILES, COLLECTION]

        if self.player_mode in streams:
            self.handle_radio_callback()
        elif self.player_mode in audio_files:
            self.handle_audiofiles_callback()
        elif self.player_mode in timed_streams:
            self.handle_audiobooks_callback(line)
    
    def handle_radio_callback(self):
        """ Radio callback handler """
        
        current = self.current()
        current_title = self.util.get_dictionary_value(current, "Title")
        if current_title == None:
            return
        
        current_title = current_title.strip()
        current["current_title"] = current_title
        current["state"] = self.util.get_dictionary_value(current, "state")
        current["source"] = "player"
        self.notify_player_listeners(current)        

    def handle_audiofiles_callback(self):
        """ Audiofiles callback handler """
        
        current = self.current()
        status = self.status()
        current_file = self.util.get_dictionary_value(current, "file")
        current_title = self.util.get_dictionary_value(current, "Title")
        current["current_track_id"] = self.util.get_dictionary_value(current, "Track")
            
        if not current_title:
            try:
                if not self.dont_parse_track_name:
                    current_title = current["file"]
                    tokens = current_title.split("/")
                    current_title = tokens[len(tokens) - 1]
            except:
                pass
            
        if current_title == None and current_file == None:
            self.notify_end_of_track_listeners()
            return
        elif current_title:
            current_title = current_title.strip()
            current["current_title"] = current_title
            current["Time"] = self.util.get_dictionary_value(status, Player.DURATION)
            current["state"] = self.util.get_dictionary_value(status, "state")
            current["source"] = "player"
            track_time = self.util.get_dictionary_value(status, "time")
            if track_time:
                current["seek_time"] = track_time.replace(":", ".")
            current["file_name"] = current_file[current_file.rfind("/") + 1:]
            self.notify_player_listeners(current)
    
    def handle_audiobooks_callback(self, line):
        """ Audiobooks callback handler
        
        :line: line from idle command
        """
        current = self.current()
        status = self.status()
        current_title = self.util.get_dictionary_value(current, "Title")
        current_file = self.util.get_dictionary_value(current, "file")
 
        if current_title == None and current_file == None and "player" in line:
            self.notify_end_of_track_listeners()
            return
         
        current_track_id = self.util.get_dictionary_value(current, "Track")
        current["current_track_id"] = current_track_id
        current["Time"] = self.util.get_dictionary_value(status, Player.DURATION)        
        current["current_title"] = current_file
        t = self.util.get_dictionary_value(status, "time")
        if t:
            track_time = t.replace(":", ".")
            current["seek_time"] = track_time
        current["state"] = self.util.get_dictionary_value(current, "state")
        current["source"] = "player"
        if current_file:
            current_title = current["file"]
            tokens = current_file.split("/")
            current_title = tokens[len(tokens) - 1]
            ct = urllib.parse.unquote(current_title)
            current["file_name"] = ct        
        
        self.notify_player_listeners(current)
        
    def play(self, state):
        """ Start playing specified track/station. First it cleans the playlist 
        then adds new track/station to the list and then starts playback
        
        :param state: button state which contains the track/station info
        """
        self.state = state
        s = getattr(state, "playback_mode", None)
        track_time = self.get_track_time(state)

        if hasattr(state, "file_name"):
            if self.current_file_url == state.file_name:
                return
            else:
                self.current_file_url = state.file_name

        if not s:
            self.current_file_url = None
            self.current_playlist_url = None  
        
        self.mode = FILE_AUDIO
        url = getattr(state, "url", None)
        if url == None: return
                
        file_name = getattr(state, "file_name", None)

        if file_name and getattr(state, "folder", None) and not url.startswith("http"):
            self.dont_parse_track_name = False
            if s and s == FILE_PLAYLIST:
                url = url[len(state.music_folder + os.sep) : ]
                url = url.replace("\\", "/")
                url = "\"" + url + "\""
            else:
                url = self.get_url(state)
        else:
            self.dont_parse_track_name = True
        
        v = getattr(state, "volume", None)
        if v and v != self.current_volume_level:
            self.current_volume_level = v
            self.set_volume(v)
        
        if url.startswith("http") or url.startswith("https"):
            url = self.encode_url(url)
            
        self.current_url = url
        batch = COMMAND_LIST_BEGIN + EOL
        batch += CLEAR + EOL
        batch += ADD + url + EOL
        batch += PLAY + '0' + EOL 
        batch += COMMAND_LIST_END + EOL
        self.conn.command(batch)
        
        attempts = 100
        attempt = 0
        duration = None
        while not self.player_mode != RADIO and not self.player_mode != STREAM and duration == None and attempt < attempts:
            time.sleep(0.1)
            duration = self.util.get_dictionary_value(self.status(), "duration")
            attempt += 1
            logging.debug("atempt " + str(attempt))

        if file_name and track_time != "0" and track_time != "0.0":
            time.sleep(0.05)
            self.seek(track_time)
            self.dispatch_callback("player")
            
        if getattr(state, "pause", None):
            self.pause()
            
    def get_track_time(self, state):
        """ Return track seek time
        
        :param state: state object
        :return: track seek time
        """
        track_time = getattr(state, "track_time", None)
        if track_time != None:
            track_time = str(track_time)
            if ":" in track_time:
                track_time = track_time.replace(":", ".")
        else:
            track_time = "0"
            
        return track_time
    
    def stop(self, state=None):
        """ Stop playback """
        
        if self.conn:
            self.conn.command(STOP)
    
    def seek(self, time):
        """ Jump to the specified position in the track
        
        :param time: time position in track
        """
        with self.lock:
            self.conn.command(SEEKCUR + time)
    
    def pause(self):
        """ Pause playback """

        self.conn.command(PAUSE)
    
    def play_pause(self, pause_flag=None):
        """ Play/Pause playback 
        
        :param pause_flag: play/pause flag
        """  
        if pause_flag:
            self.conn.command(PAUSE)
        else:
            self.conn.command(RESUME)
            
        with self.lock:    
            if self.muted:
                self.muted = False
                self.mute()
                self.muted = True
            else:
                self.conn.command(SET_VOLUME + str(self.current_volume_level))
    
    def set_volume(self, level):
        """ Set volume level
        
        :param level: new volume level
        """
        with self.lock:
            self.current_volume_level = level
            self.conn.command(SET_VOLUME + str(level))
            if self.muted:
                self.muted = False
                    
    def get_volume(self):
        """  Return current volume level 
        
        :return: volume level or -1 if not available
        """
        with self.lock:
            st = self.status()
            volume = '-1'
            
            try:
                volume = st[GET_VOLUME]
            except KeyError:
                pass
            
            if volume == "-1":
                with self.lock:
                    volume = self.current_volume_level
            
            return int(volume)
    
    def mute(self):
        """ Mute """
        
        with self.lock:
            self.muted = not self.muted
            
            if self.muted:
                v = self.get_volume()
                if v != 0:                
                    self.current_volume_level = v 
                self.conn.command(MUTE_2)
            else:
                self.conn.command(SET_VOLUME + " " + str(self.current_volume_level))
    
    def status(self):
        """ Return the result of the STATUS command """
        
        with self.lock:
            return self.conn.read_dictionary(STATUS)
        
    def current(self):
        """ Return the current song """
        
        with self.lock:
            return self.conn.read_dictionary(CURRENT_SONG)

    def shutdown(self):
        """ Shutdown the player """
        
        with self.lock:
            self.playing = False
        
    def get_current_track_time(self):
        """  Return current track time
        
        :return: current track time
        """
        s = self.status()
        t = None
        try:
            t = s[Player.DURATION]
        except:
            pass
        return t
    
    def get_current_playlist(self):
        """  Return current playlist
        
        :return: current playlist
        """
        return self.playlist
        
    def load_playlist(self, state, stop_player=True):
        """  Load new playlist
        command to list playlists: mpc listplaylists
        
        :param state: state object defining playlist location
        :param stop_player: True - stop player, False - don't stop player

        :return: new playlist
        """
        return super().load_playlist(state, False)
    
    def notify_end_of_track_listeners(self):
        """  Notify end of track listeners. Starts new thread to unblock player loop. """
        
        thread = threading.Thread(target=self.handle_eof)
        thread.start()
            
    def handle_eof(self):
        """  End of track notifier. Runs in separate thread. """ 
        
        for listener in self.end_of_track_listeners:
            listener()
    
    def update_mpd_database(self):
        """ Update database """
        
        self.conn.command(UPDATE + EOL)
