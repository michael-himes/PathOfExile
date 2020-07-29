from pynput.mouse import Button, Controller
import json, os, sys

def iterator(tab, rows, columns, locale ):
    top = locale[tab]["top_left_corner"][1:-1].split(',')
    bottom = locale[tab]["bottom_right_corner"][1:-1].split(',')
    x_top = int(top[0])
    y_top = int(top[1])
    x_bottom = int(bottom[0])
    y_bottom = int(bottom[1])
    x_step = int( (x_bottom - x_top ) / columns )
    y_step = int( (y_bottom - y_top ) / rows )
    return [x_top, x_bottom, x_step], [y_top, y_bottom, y_step]

def append(item):
    json_location = os.path.join(os.environ['USERPROFILE'], "Documents\My Games\Path of Exile\locations.json")
    with open(json_location) as json_file:
        data = json.load(json_file)
        json_file.close()
    if item == "tab":
        tab_count = 0
        for elements in data:
            if "Tab " in elements:
                tab_count += 1
        add_tabs(tab_count, data)
    else:
        a,b = item.split(':')
        data["Items"][a] = b 
    write_location = os.path.join(os.environ['USERPROFILE'], "Documents\My Games\Path of Exile\locations.json")
    with open(write_location, "w") as outfile:
        json.dump(data, outfile, indent=4)
    
def add_tabs(tab, locale):
    mouse = Controller()
    while 1:
        more = input("Would you like to add more tabs?\n")
        if more == 'n':
            break
        current_tab = "Tab " + str(tab+1)
        location = { 'Location': str(mouse.position) }
        locale[current_tab] = location
        print(current_tab, str(mouse.position))
        tab += 1

def inital():
    mouse = Controller()
    locale = {
        'Inventory': {
            'top_left_corner': '',
            'bottom_right_corner': ''
        },
        'Default': {
            'Location': '',
            'top_left_corner': '',
            'bottom_right_corner': ''
        },
        'Currency': {
            'Location': ''
        },
        'Fragment': {
            'Location': ''
        },
        'Card': {
            'Location': ''
        },
        'Essence': {
            'Location': ''
        },
        'Map': {
            'Location': ''
        }
    }

    for i in locale.keys():
        print('\n\t\t',i)
        for j in locale[i]:
            input(j)
            locale[i][j] = str(mouse.position)
            print(locale[i][j])

    add_tabs(0, locale)

    locale['Inventory']['Iterator'] = iterator("Inventory", 4, 11, locale ) 
    locale['Default']['Iterator'] = iterator("Default", 11, 11, locale) 

    items = {
        'Seed': 'Tab 1'
    }   
    locale["Items"] = items

    print(locale)
    write_location = os.path.join(os.environ['USERPROFILE'], "Documents\My Games\Path of Exile\locations.json")
    with open(write_location, "w") as outfile:
        json.dump(locale, outfile, indent=4)

if len(sys.argv) == 1:
    inital()
else:
    append(sys.argv[1])
