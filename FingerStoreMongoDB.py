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

import pymongo
import bson.objectid
import FingerStore
import time

from configuration import configuration
_cfg=configuration()
_credentials=_cfg.get('MongoDB')

def _debugDB(client, db, coll):
    print("MongoDB: %s" % (coll))
    print("DBs: %s" % (self._client.database_names()))
    print("cols: %s" % (self._db.collection_names()))

class FingerStoreMongoDB(FingerStore.FingerStore):
    """
    base class for ID:token mapping (e.g. 'username:password', or 'UUID:fingerprint') storage.
    both <ID> and <token> must be unique.

    this class implements a simple RAM-based storage,
    but child classes might be persistent (e.g. filesystem),
    and/or distributed (e.g. database-server)
    """
    def __init__(self):
        print("MongoDB cred: %s" % (_credentials))
        self._client = pymongo.MongoClient(**_credentials)
        time.sleep(0.1)
        if not self._client.nodes:
            raise(Exception("unable to connect to %s" % (self._client)))
        self._db = self._client.FingerAuth
        self._coll = self._db.FingerPrints
        self._debugDB()
    def _debugDB(self):
        _debugDB(self._client, self._db, self._coll)

    def addID(self, ID, token):
        """
        adds an authentication <token> for user <ID> to the database.
        returns the <ID> (might be different from the one requested)
        """
        ## we just forget about the ID for now
        print("addingID: '%s' (maybe)" % (ID))
        self._debugDB()
        ID = self._coll.insert_one({'fingerprint': token}).inserted_id
        return str(ID)
    def getID(self, token):
        """
        get <ID> associated with <token> (or None)
        """
        d=self._coll.find_one({'fingerprint': token})
        if d:
            return str(d['_id'])
        return None
    def getToken(self, ID):
        """
        get <token> associated with <ID> (or None)
        """
        d=self._coll.find_one({'_id': bson.objectid.ObjectId(ID)})
        if d:
            return d['fingerprint']
        return None
    def getIDs(self):
        """
        gets a list of all <ID>s
        """
        return [str(x['_id']) for x in self._coll.find({'fingerprint': { '$exists': True}}, {'_id':1})]
    def getTokens(self):
        """
        gets a list of all <token>s
        """
        return [x['fingerprint'] for x in self._coll.find({'fingerprint': { '$exists': True}}, {'_id':0, 'fingerprint':1})]

if '__main__' == __name__:
    s=FingerStoreMongoDB()
    def print_ids(store, id, token):
        print("IDs: %s" % (store.getIDs()))
        print("Tokens: %s" % (store.getTokens()))
        print("%s -> %s" % (id, store.getToken(id)))
        print("%s <- %s" % (token, store.getID(token)))
        #print("%s" % store._store)
        print("")
    a=s.addID('a'*16, 'A')
    print_ids(s, a, 'A')
    b=s.addID('b'*16, 'B')
    print_ids(s, a, 'B')

    a=s.addID(a, 'C')
    print_ids(s, a, 'A')

    c=s.addID('c'*16, 'C')
    print_ids(s, c, 'C')
