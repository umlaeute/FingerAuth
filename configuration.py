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

try:
    import ConfigParser
except ImportError:
    import configparser as ConfigParser
import os.path

_configpaths=[
#    os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config'), ## built-in
#    os.path.join(getRoot(), 'etc', 'FINGERAUTH'),                            ## system-wide
#    os.path.join(os.path.expanduser('~'), '.config', 'iterations.esc.mur.at'),   ## per-user
    '.',                                                                ## local
    ]

class configuration:
    def __init__(self, file='FingerAuth.conf'):
        if os.path.isabs(file):
            configfiles=[file]
        else:
            configfiles=[os.path.join(path, file) for path in _configpaths]
        self.cfg = ConfigParser.ConfigParser()
        self.cfg.read(configfiles)
    def get(self, section):
        d=dict()
        if not self.cfg.has_section(section):
            self.cfg.add_section(section)
        for o in self.cfg.options(section):
            v=self.cfg.get(section, o)
            d[o]=v
        return d

if '__main__' == __name__:
    cfg=configuration('/tmp/foo/test.conf')
    def printcfg(cfg, section):
        d=cfg.get(section)
        print("%s: %s" % (section, d))
    printcfg(cfg, 'MySQL')
