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


import pyfprint as FP

TIMEOUT=60
SERVERURL='https://google.com/&q='
# /questions /answers /comments /protests /tto
URLSUFFIX=''

import os.path
BROWSER=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'rechrome.sh')

from configuration import configuration
_cfg=configuration()
_conf=_cfg.get('FingerAuth')
SERVERURL=_conf.get('url', SERVERURL)
URLSUFFIX=_conf.get('urlsuffix', URLSUFFIX)
try:
    TIMEOUT=int(_conf.get('timeout', str(TIMEOUT)))
except ValueError:
    pass

BACKEND=_conf.get('fingerstore')


if 'MongoDB' == BACKEND:
    from FingerStoreMongoDB import FingerStoreMongoDB as FingerStore
elif 'MySQL' == BACKEND:
    from FingerStoreMySQL import FingerStoreMySQL as FingerStore
else:
    from FingerStore import FingerStore as FingerStore


FP.fp_init()
import atexit
atexit.register(FP.fp_exit)

class FingerAuth():
    def __init__(self, device=None, database=FingerStore()):
        """
        args:
         @arg: <device> identifier for the fingerprint reader
        """
        self.device=None
        devs=FP.discover_devices()
        if not devs:
            raise Exception("no devices found")
        if device is None:
            self.device=devs[0]
        elif FP.Device == type(device):
            self.device=device
        elif int == type(device):
            if device<len(devs):
                self.device=devs[device]
        elif FP.Fprint == type(device):
            self.device = devs.find_compatible(device)
        #TODO: string IDs
        if not self.device:
            raise Exception("invalid device")
        device=self.device
        device.close()
        device.open()

        if database is None:
            database=FingerStore()
        self.fingerprints = database

    def auth_or_add(self, defaultID=None):
        """
        will fetch the fingerprint from the sensor,
        and compare it to it's list of fingerprint database.
        if the fingerprint cannot be identified, it is added to the database
        using <defaultID> as ID.
        @returns: the ID matching the fingerprint is then returned.

        If <defaultID> is None, the fingerprint won't be added!
        """
        fps_raw=self.fingerprints.getTokens()
        fps=[FP.Fprint(x) for x in fps_raw]
        fps_count=len(fps)
        print("searching for fingerprint in %s known ones" % (fps_count))

        ## if identification fails, try again to avoid false negatives
        count=3
        while count>0:
            try:
                i,fp,img,state=self.device.identify_finger(fps)
            except FP.FprintException as e:
                print("unable to identify finger: %s" % (e))
                return None
            #print("#%s: (%s,%s,%s,%s)" % (count, i, fp, img, state))
            if state >= FP.VERIFY_RETRY:
                return None
            if FP.VERIFY_MATCH == state:
                break
            count-=1
        if not fp:
            print("not found in %s (%s); enrolling new finger" % (fps_count, state))
            fp,img=self.device.enroll_finger()
            if defaultID is not None:
                defaultID=self.fingerprints.addID(defaultID, bytes(fp.data()))
            return defaultID
        id=self.fingerprints.getID(fps_raw[i])
        return id

if '__main__' == __name__:
    import os
    import uuid
    import time
    import collections
    import hashlib
    import argparse
    parser=argparse.ArgumentParser()
    parser.add_argument('-t', '--timeout', type=int, default=TIMEOUT, help='timeout for re-authenticating the same user (default: %s)' % (TIMEOUT))
    parser.add_argument('-u', '--url', type=str, default=SERVERURL, help='base-url (default: %s)' % (SERVERURL))
    parser.add_argument('-s', '--suffix', type=str, default=URLSUFFIX, help='url-suffix (default: %s)' % (URLSUFFIX))
    parser.add_argument('-B', '--browser', type=str, default=BROWSER, help='browser used to launch pages (default: %s)' % (BROWSER))
    args=parser.parse_args()
    fa=FingerAuth()
    test=True
    test=False

    os.system("%s %s/" % (BROWSER, args.url))
    if not test:
        lastid=None
        lasttime=0
        try:
            while(True):
                ids=[]
                u=uuid.uuid4().bytes
                id=fa.auth_or_add(defaultID=u)
                if lastid == id:
                    ## filter-out duplicate login attempts
                    now=time.time()
                    if (now-lasttime) < args.timeout:
                        print("ignoring attempt to re-authenticate")
                        lasttime=now
                        continue
                if id:
                    lastid=id
                    lasttime=time.time()
                    print("ID: '%s'\t'%s'" % (type(id), id))
                    if type(id) == str:
                        id=bytes(id, 'utf-8')
                        print("ID: '%s'\t'%s'" % (type(id), id))
                    id5=hashlib.md5(id).hexdigest()
                    print("FingerPrint: %s [%s]" % (id, id5))
                    #print("data: %s" % (fa.fingerprints._store))
                    os.system("%s %s%s%s" % (BROWSER, args.url, id5, args.suffix))

                #time.sleep(2)
                #print("awake!")
        except KeyboardInterrupt:
            pass
    else:
        #fa.test()
        tokens=fa.fingerprints.getTokens()
        for t in tokens:
            print("Token: %s" % (type(t)))

    print("GoodBye")
