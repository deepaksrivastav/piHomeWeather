#!/usr/bin/python

from jabberbot import JabberBot, botcmd
import datetime
import sqlite3
import subprocess

dbname='/home/pi/piHomeWeather/weatherdb'

class SystemInfoJabberBot(JabberBot):
    @botcmd
    def serverinfo( self, mess, args):
        """Displays information about the server"""
        version = open('/proc/version').read().strip()
        loadavg = open('/proc/loadavg').read().strip()

        return '%s\n\n%s' % ( version, loadavg, )
    
    @botcmd
    def weather( self, mess, args):
        """Display weather conditions at home"""
        conn=sqlite3.connect(dbname)
        curs=conn.cursor()
        curs.execute("SELECT temperature, humidity,datetime(timestamp, 'localtime') FROM weatherdata order by timestamp desc limit 1")
        rowcur=curs.fetchone()
        rowstrcur="Recorded at: {2} | Temperature: {0:0.1f} *C | Humidity : {1:0.1f}%".format(rowcur[0],rowcur[1],str(rowcur[2]))
        return rowstrcur

    @botcmd
    def time( self, mess, args):
        """Displays current server time"""
        return str(datetime.datetime.now())

    @botcmd
    def cmd( self, mess, args):
        """Run a command"""
        args = args.strip().split(' ')
        proc = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = proc.communicate()
        return out + '\n' + err

username = 'username'
password = 'password'
bot = SystemInfoJabberBot(username,password)
bot.serve_forever()
