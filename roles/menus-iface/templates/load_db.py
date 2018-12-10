#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Create a mysql database from separate json, and html files

import logging
from logging.handlers import RotatingFileHandler
import os
import sys
import MySQLdb
import MySQLdb.cursors
import re
import fnmatch
import json

#GLOBALS
#MENU_FILES = "{{ doc_root }}/js-menu/menu-files"
MENU_FILES = "/library/www/html/js-menu/menu-files"
MENU_DEFS = MENU_FILES + "/menu-defs"
ICON_BASE = MENU_FILES + "/images"
#ASSET_BASE = {{ doc_root }} + "/common/assets"
ASSET_BASE = '/library/www/html//common/assets'
KIWIX_CAT = ASSET_BASE + '/kiwix_catalog.json'
DOWNLOADED_ZIMS = ASSET_BASE + '/zim_version_idx.json'
DL_ZIMS = ASSET_BASE + '/trial_zim_version_idx.json'
MAPPING = ASSET_BASE + '/map2menu.json'
MI_LKUP = ASSET_BASE + '/menuitem-lkup.json'

zims ={}


def scrape_menu_defs():
   # put the values in menu-defs,images,extra_html,kixix-catalog
   #   into a mysql menus_db database
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
   os.chdir(MENU_DEFS)
   columns = ['menu_item_name','description','title','extra_html',
              'lang','zim_name','logo_url','intended_use','moddir',
              'start_url','apk_file','apk_file_size']


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
      conn.close()

###########################################################
def scrape_images():
   # Get the images
   conn = MySQLdb.connect(host="localhost",
                        cursorclass=MySQLdb.cursors.DictCursor, 
                        charset="utf8",
                        user="menus_user",
                        passwd="g0adm1n",
                        db="menus_db")
   if not conn:
          print("failed to open mysql database")
          sys.exit(1)

   # scan through the menus getting the list of icon names
   c = conn.cursor()
   os.chdir(ICON_BASE)
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

###########################################################
def add_row(cursor, tablename, rowdict):
    # XXX tablename not sanitized
    # XXX test for allowed keys is case-sensitive

    # filter out keys that are not column names
    cursor.execute("describe %s" % tablename)
    allowed_keys = set(row[0] for row in cursor.fetchall())
    keys = allowed_keys.intersection(rowdict)

    if len(rowdict) > len(keys):
        unknown_keys = set(rowdict) - allowed_keys
        #print >> sys.stderr, "skipping keys:", ", ".join(unknown_keys)

    columns = ", ".join(keys)
    values_template = ", ".join(["%s"] * len(keys))

    sql = "insert into %s (%s) values (%s)" % (
        tablename, columns, values_template)
    values = tuple(rowdict[key] for key in keys)
    cursor.execute(sql, values)

###########################################################
def scrape_kiwix_catalog():
   conn = MySQLdb.connect(host="localhost",
                        charset="utf8",
                        user="menus_user",
                        passwd="g0adm1n",
                        db="menus_db")
   if not conn:
          print("failed to open mysql database")
          sys.exit(1)
   # get mysql column names for kiwix catalog
   cursor = conn.cursor()

   # start loading the table with a fresh start                          
   cursor.execute('truncate modules')

   # Read the kiwix catalog
   with open(KIWIX_CAT, 'r') as kiwix_cat:
      json_data = kiwix_cat.read()
      download = json.loads(json_data)
      zims = download['zims']
      print('zims loaded')
      for uuid in zims.keys():
         try:
            add_row(cursor,"modules",zims[uuid])
            
         #except MySQLdb.Error as e:
         except Exception as e:
            print str(e)
   conn.commit()
   conn.close()

###########################################################
if __name__ == "__main__":
   scrape_menu_defs()
   scrape_images()
   scrape_kiwix_catalog()
