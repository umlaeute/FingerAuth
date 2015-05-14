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

import mysql.connector
import FingerStore

from configuration import configuration
_cfg=configuration()
_credentials=_cfg.get('MySQL')


class FingerStoreMySQL(FingerStore.FingerStore):
    """
    base class for ID:token mapping (e.g. 'username:password', or 'UUID:fingerprint') storage.
    both <ID> and <token> must be unique.

    this class implements a simple RAM-based storage,
    but child classes might be persistent (e.g. filesystem),
    and/or distributed (e.g. database-server)
    """
    def __init__(self):
        print("MySQL cred: %s" % (_credentials))
        self._db=mysql.connector.connect(**_credentials)

    def addID(self, ID, token):
        """
        adds an authentication <token> for user <ID> to the database.
        returns the <ID> (might be different from the one requested)
        """
        Q=("INSERT INTO fingers VALUES(%s,%s) ON DUPLICATE KEY UPDATE finger=%s")
        cur=self._db.cursor()
        cur.execute(Q, (ID, token, token))
        self._db.commit()
        return ID
    def getID(self, token):
        """
        get <ID> associated with <token> (or None)
        """
        Q=("SELECT id FROM fingers WHERE finger=%s")

        self._db.commit()
        cur=self._db.cursor()
        cur.execute(Q, (token,))
        res=cur.fetchall()
        cur.close()
        if res:
            return res[0][0]
        return None
    def getToken(self, ID):
        """
        get <token> associated with <ID> (or None)
        """
        Q=("SELECT finger FROM fingers WHERE id=%s")

        self._db.commit()
        cur=self._db.cursor()
        cur.execute(Q, (ID,))
        res=cur.fetchall()
        cur.close()
        if res:
            return res[0][0]
        return None
    def getIDs(self):
        """
        gets a list of all <ID>s
        """
        Q=("SELECT id FROM fingers")

        self._db.commit()
        cur=self._db.cursor()
        cur.execute(Q)
        res=cur.fetchall()
        cur.close()
        if res:
            return [x[0] for x in res]
        return []
    def getTokens(self):
        """
        gets a list of all <token>s
        """
        Q=("SELECT finger FROM fingers")

        self._db.commit()
        cur=self._db.cursor()
        cur.execute(Q)
        res=cur.fetchall()
        cur.close()

        if res:
            return [x[0] for x in res]
        return []


if '__main__' == __name__:
    s=FingerStoreMySQL()
    def print_ids(store, id, token):
        print("IDs: %s" % (store.getIDs()))
        print("Tokens: %s" % (store.getTokens()))
        print("%s -> %s" % (id, store.getToken(id)))
        print("%s <- %s" % (token, store.getID(token)))
        #print("%s" % store._store)
        print("")
    s.addID('a'*16, 'A')
    print_ids(s, 'a'*16, 'A')
    s.addID('b'*16, 'B')
    print_ids(s, 'a'*16, 'B')

    s.addID('a'*16, 'C')
    print_ids(s, 'a'*16, 'A')

    s.addID('c'*16, 'C')
    print_ids(s, 'c'*16, 'C')
