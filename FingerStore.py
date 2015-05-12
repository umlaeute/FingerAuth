#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright © 2015, IOhannes m zmölnig, forum::für::umläute

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this file.  If not, see <http://www.gnu.org/licenses/>.

def print_keyanddict(KEY, DICT, length=10):
    print("get: '%s' from {" % (KEY[:length]))
    for k in DICT:
        print("\t%s: %s" % (k[:length], DICT[k][:length]))
    print("}")

class FingerStore():
    """
    base class for ID:token mapping (e.g. 'username:password', or 'UUID:fingerprint') storage.
    both <ID> and <token> must be unique.

    this class implements a simple RAM-based storage,
    but child classes might be persistent (e.g. filesystem),
    and/or distributed (e.g. database-server)
    """
    def __init__(self):
        self._store={}

    def addID(self, ID, token):
        """
        adds an authentication <token> for user <ID> to the database.
        returns the <ID> (might be different from the one requested)
        """
        self._store[ID]=token
        return ID
    def getID(self, token):
        """
        get <ID> associated with <token> (or None)
        """
        for k in self._store:
            if self._store[k] == token:
                return k
        return None
    def getToken(self, ID):
        """
        get <token> associated with <ID> (or None)
        """
        try:
            return self._store[ID]
        except KeyError:
            return None
    def getIDs(self):
        """
        gets a list of all <ID>s
        """
        return [x for x in self._store.keys()]
    def getTokens(self):
        """
        gets a list of all <token>s
        """
        return [x for x in self._store.values()]


if '__main__' == __name__:
    s=FingerStore()
    def print_ids(store, id, token):
        print("IDs: %s" % (store.getIDs()))
        print("Tokens: %s" % (store.getTokens()))
        print("%s -> %s" % (id, store.getToken(id)))
        print("%s <- %s" % (token, store.getID(token)))
        print("%s" % store._store)
        print("")
    s.addID('a', 'A')
    print_ids(s, 'a', 'A')
    s.addID('b', 'B')
    print_ids(s, 'a', 'B')

    s.addID('a', 'C')
    print_ids(s, 'a', 'A')

    s.addID('c', 'C')
    print_ids(s, 'c', 'C')
