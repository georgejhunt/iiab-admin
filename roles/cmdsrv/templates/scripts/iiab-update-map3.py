#!/usr/bin/env python3
# Scan the osm-vector-maps directory, update the osm-vector-maps-idx.json, add menu-defs

import json

import iiab.iiab_lib as iiab

try:
    import iiab.adm_lib as adm
    adm_cons_installed = True
except:
    adm_cons_installed = False
    pass

def main():
    map_catalog = adm.get_map_catalog()

    map_menu_def_list = adm.get_map_menu_defs()

    previous_idx = adm.read_vector_map_idx()

    installed_tiles = adm.get_installed_tiles()

    adm.write_vector_map_idx(installed_tiles)
    # For installed regions, check that a menu def exists, and it's on home page
    for fname in installed_tiles:
        map = map_catalog['maps'].get(fname,'')
        if map == '':
            print("Skipping unknown map " + fname)
            continue
        else:
            map_item = map_catalog['maps'][fname]
            menu_item_name = map_item['perma_ref']

            if not (menu_item_name in map_menu_def_list):
                print('Creating menu def for %s'%menu_item_name)
                adm.create_map_menu_def(region, menu_item_name, map_item)

        # if autoupdate allowed and this is a new region then add to home menu
        if adm.fetch_menu_json_value('autoupdate_menu') and menu_item_name not in previous_idx:
            print('Auto-update of menu items is enabled. Adding %s'%region)
            adm.update_menu_json(menu_item_name)
            # redirect from box/maps to an installed map rather than test page
            with open(adm.CONST.map_doc_root + '/index.html','w') as fp:
                outstr = """<head> \n<meta http-equiv="refresh" content="0; URL=/osm-vector-maps/en-osm-omt_%s " />\n</head>"""%fname
                fp.write(outstr)

    if len(installed_tiles) == 0: # it is the splash page, display only if no others
        menu_item_name = 'en-map_test'
        map_item = { "perma_ref" : menu_item_name }
        adm.update_menu_json(menu_item_name)
        return

if __name__ == '__main__':
   if adm_cons_installed:
      main()
