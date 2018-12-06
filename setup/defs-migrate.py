#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Create a sqlite database from separate json, and html file

import logging
from logging.handlers import RotatingFileHandler
import os
import sys
#import sqlite3
import MySQLdb
import MySQLdb.cursors
import re
import fnmatch
import json

MENU_BASE = "/library/www/html/js-menu/menu-files/menu-defs"
ICON_BASE = "/library/www/html/js-menu/menu-files/images"
os.chdir(MENU_BASE)

# Get the IIAB variables
sys.path.append('/etc/iiab/')
from iiab_env import get_iiab_env
doc_root = get_iiab_env("WWWROOT")

columns = ['menu_item_name','description','title','extra_html',
           'lang','zim_name','logo_url','intended_use','moddir',
           'start_url','apk_file','apk_file_size']

def makevisible(name):
    sql = 'SELECT name,id FROM menus WHERE name = %s'
    try:
      c.execute(sql,(name,))
      rv = c.fetchone()
    except Exception as e:
       print(e)
       print("name not found in menus:%s"%name)
       return
    if not rv:
       print("name not found in menus:%s"%name)
       return
    siterequest = 'default'
    menus_id = rv['id']
    # get the max of seq for the site
    sql = "SELECT max(seq) as max FROM menus as m, chosen as c " +\
          "WHERE c.menus_id = m.id AND c.site = %s GROUP by c.site" 
    c.execute(sql,(siterequest,))
    rv = c.fetchone()
    if rv and rv['max']:
         seq = rv['max'] + 1
    else:
         seq = 1
    sql = "INSERT INTO  chosen SET menus_id = %s, site = %s, seq = %s"
    try:
       c.execute(sql,(menus_id,siterequest,seq,))
       c.commit()
    except:
       return 1
    return 0

# ##########  scan for variable names #############
keys=[]
for filename in os.listdir('.'):
   if fnmatch.fnmatch(filename, '*.json'):
      with open(filename) as json_file:  
          data = json.load(json_file)
          for p in data.keys():
             # replace any blanks with underbar
             p = p.replace(" ","_")
             p = p.replace("-","_")
             if not p in keys:
                keys.append(p)

# ########## database operations ##############
conn = MySQLdb.connect(host="localhost",
                     cursorclass=MySQLdb.cursors.DictCursor, 
                     charset="utf8",
                     user="menus_user",
                     passwd="g0adm1n",
                     db="menus_db")
if not conn:
       print("failed to open mysql database")
       sys.exit(1)
c = conn.cursor()
c.execute('truncate menus')
#c.execute('flush tables')
# ########## Transfer the values  ##############

keys=[]
for filename in os.listdir('.'):
   if fnmatch.fnmatch(filename, '*.json'):
      nameval = filename[:-5]
      # skip over this file if it exists in database
      rows = c.execute("select name from menus where name = %s",(nameval,))
      if not rows:
         # make sure record exists
         sql = "INSERT IGNORE INTO menus SET name=%s"
         #print(sql)
         c.execute(sql,(nameval,)) 
         with open(filename) as json_file:  
             reads = json_file.read()
             data = json.loads(reads)
             for col in columns:
                if col in data.keys():
                   updstr = data[col].replace("'","''")
                   sql = "UPDATE menus set " + col + " = %s where name = %s"
                   try:
                     c.execute(sql,(updstr,nameval,))
                   except MySQLdb.Error as e:
                     print str(e)
                     print sql
                          
             instr = ''
             lines = reads.split('\n')
             for line in lines:
                line = line.rstrip('\n')
                line = line.rstrip('\r')
                line = line.rstrip('\n')
                line = line.lstrip(' ')
                instr += line
             updstr = instr.replace("'","''")
             #updstr = instr.replace('\\"','\\\\"')
             sql = "UPDATE menus set js = %s where name = %s"
             try:
               c.execute(sql,(updstr,nameval,))
             except MySQLdb.Error as e:
               print str(e)
               print sql
   if fnmatch.fnmatch(filename, '*.html'):
      nameval = filename[:-5]
      if True:
         with open(filename) as html_file:  
             reads = html_file.read()
             updstr = reads.replace("'","''")
             sql = "UPDATE menus set extra_html = %s where name = %s"
             try:
               c.execute(sql,(updstr,nameval))
             except MySQLdb.Error as e:
               print str(e)
               print sql
                          
   conn.commit()
# Get the images

os.chdir(ICON_BASE)
# scan through the menus getting the list of icon names
sql = "SELECT logo_url,name from menus"
num = c.execute(sql)
rows = c.fetchall()
for row in rows:
   if row and row['logo_url']:
      if os.path.isfile("./%s"%row['logo_url']):
         with open(row['logo_url']) as icon_file:  
            try:
               reads = icon_file.read()
               sql = "UPDATE menus SET icon = %s where name = %s"
               c.execute(sql,(reads,row['name'],))
            except Exception as e:
               print str(e)
               print("Logo_url error: %s"%row['logo_url'])
      else:
         print("logo_url file missing:%s"%row['logo_url'])
conn.commit()

############ look for a menuitems.json file  ##################
menujson_path = os.path.join(doc_root,"home/menuitems.json")
if os.path.exists(menujson_path):
   with open(menujson_path,"r") as json_file:
      lines = json_file.read().split('\n')
      for line in lines:
         line = line.strip()
         if line.find('//') != -1:
            continue
         if line.find('[') != -1:
            continue
         if line.find(']') != -1:
            continue
         if line.find('",') != -1:
            line = line[:-2]
         if line.find('"') != -1:
            line = line[1:]
         if line[-1:] == '"':
            line = line[:-1]
         if len(line) == 0:
            continue
         makevisible(line)         

conn.close()
