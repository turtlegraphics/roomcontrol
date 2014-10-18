"""
logging

Module to log game events

Copyright (C) 2014 Bryan Clair (bryan@slu.edu)

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License along
with this program; if not, write to the Free Software Foundation, Inc.,
51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
"""
import time,os
import countdown

class Logger:
    def __init__(self):
        self.logfile = None

    def log(self,msg):
        """Write msg to the logfile for this run."""
        self.logfile.write(str(countdown.timer)+' '+msg+'\n')

    def open(self,dir):
        """Open a new logfile in the directory given by dir."""
        logfilename = 'roomlog'+time.strftime('%m-%d %H-%M.txt')
        self.logfile = open(os.path.join(dir,logfilename),'w')

    def close(self):
        self.logfile.close()

logger = Logger()
