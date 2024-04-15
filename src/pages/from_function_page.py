# single_type_page.py
#
# Copyright 2023 Nokse
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# SPDX-License-Identifier: GPL-3.0-or-later

from gi.repository import Adw
from gi.repository import Gtk
from gi.repository import GLib
from gi.repository import Gio
from gi.repository import Gdk

import tidalapi
from tidalapi.page import PageItem, PageLink
from tidalapi.mix import Mix, MixType
from tidalapi.artist import Artist
from tidalapi.album import Album
from tidalapi.media import Track
from tidalapi.playlist import Playlist
from tidalapi.user import Favorites

from ..lib import utils

import threading
import requests
import random

from .page import Page

class fromFunctionPage(Page):
    __gtype_name__ = 'fromFunctionPage'

    """Used to display lists of albums/artists/mixes/playlists and tracks from a request function"""

    # TODO load only a fixed number of items at first then if the page is scrolled down load some more

    def __init__(self, _window, _function, _type):
        super().__init__(_window, _function, _type)

        self.type = _type
        self.function = _function

    def _load_page(self):
        if self.type == "track":
            self.add_tracks()
        elif self.type == "mix":
            self.add_mixes()
        elif self.type == "album":
            self.add_albums()
        elif self.type == "artist":
            self.add_artists()
        elif self.type == "playlist":
            self.add_playlists()

        self._page_loaded()

    def add_tracks(self):
        tracks_list_box = Gtk.ListBox(css_classes=["boxed-list"], margin_bottom=12, margin_start=12, margin_end=12, margin_top=12)
        self.page_content.append(tracks_list_box)

        tracks = self.function(limit=50)
        tracks_list_box.connect("row-activated", self.on_tracks_row_selected, favourite_tracks)

        for index, track in enumerate(favourite_tracks):
            listing = self.get_track_listing(track)
            listing.set_name(str(index))
            tracks_list_box.append(listing)

    def add_mixes(self):
        flow_box = Gtk.FlowBox(selection_mode=0)
        self.page_content.append(flow_box)

        mixes = self.function(limit=50)

        for index, mix in enumerate(mixes):
            card = self.get_mix_card(mix)
            flow_box.append(card)

    def add_artists(self):
        flow_box = Gtk.FlowBox(selection_mode=0)
        self.page_content.append(flow_box)

        artists = self.function(limit=50)

        for index, artist in enumerate(artists):
            card = self.get_artist_card(artist)
            flow_box.append(card)

    def add_playlists(self):
        flow_box = Gtk.FlowBox(selection_mode=0)
        self.page_content.append(flow_box)

        playlists = self.function(limit=50)

        for index, playlist in enumerate(playlists):
            card = self.get_playlist_card(playlist)
            flow_box.append(card)

    def add_albums(self):
        flow_box = Gtk.FlowBox(selection_mode=0)
        self.page_content.append(flow_box)

        albums = self.function(limit=50)

        for index, album in enumerate(albums):
            card = self.get_album_card(album)
            flow_box.append(card)

    def on_tracks_row_selected(self, list_box, row, favourite_tracks):
        index = int(row.get_name())

        self.window.player_object.current_mix_album_list = favourite_tracks
        track = favourite_tracks[index]
        print(track)
        self.window.player_object.song_album = track.album
        self.window.player_object.play_track(track)
        self.window.player_object.current_song_index = index