#!/usr/bin/env python
# -*- coding: utf-8 -*-
# after content is downloaded, create a lookup json with required data

import os
import sys
from load_db import scrape_kiwix_catalog 
import MySQLdb
import MySQLdb.cursors
import g
import json

#GLOBALS
MENU_FILES = "/library/www/html/js-menu/menu-files"
MENU_DEFS = MENU_FILES + "/menu-defs"
ASSET_BASE = '/library/www/html//common/assets'
MI_LKUP = ASSET_BASE + '/menuitem-lkup.json'

def write_menuitem_json():
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
   outstr = '['
   sql = 'SELECT me.name,mo.name,mo.perma_ref,size,articleCount,mediaCount FROM modules as mo,menus as me WHERE  me.zim_name = mo.perma_ref'
   try:
      c.execute(sql)
      rv = c.fetchall()
      for row in rv:
         outstr += ' {"' + row['name'] + '":{\n'
         #outstr += '  "fileref":"' + row[p + '",\n'
         outstr += '  "size":"' + row['size'] + '",\n'
         outstr += '  "articleCount":"' + row['articleCount'] + '",\n'
         outstr += '  "mediaCount":"' + row['mediaCount'] + '"\n'
         outstr += '  }\n'
         outstr += ' },\n'
   except MySQLdb.Error as e:
      print str(e)
      print sql
   outstr = outstr[:-2] + '\n]'
   with open(MI_LKUP,'w') as outfile:
      outfile.write(outstr)
      outfile.close()
###########################################################
if __name__ == "__main__":
   scrape_kiwix_catalog()
   write_menuitem_json()
