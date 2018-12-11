#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import MySQLdb
import MySQLdb.cursors
import json

MENU_JSON_DIR = '/library/www/html/home/'
MENU_JSON_NAME = 'menu.json'

def write_menu_json():
   with open(MENU_JSON_DIR + MENU_JSON_NAME,"r") as menu_fp:
      data = json.loads(menu_fp.read())
      data['menu_items_1'].append("new menu idem")
      print(str(data))
      print(json.dumps(data, indent=2, sort_keys=True))

###########################################################
if __name__ == "__main__":
   write_menu_json()
