from pynput.mouse import Button, Controller
import json, os
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

def iterator(tab, rows, columns ):
    global locale 
    top = locale[tab]["top_left_corner"][1:-1].split(',')
    bottom = locale[tab]["bottom_right_corner"][1:-1].split(',')
    x_top = int(top[0])
    y_top = int(top[1])
    x_bottom = int(bottom[0])
    y_bottom = int(bottom[1])
    x_step = int( (x_bottom - x_top ) / columns )
    y_step = int( (y_bottom - y_top ) / rows )
    return [x_top, x_bottom, x_step], [y_top, y_bottom, y_step]


for i in locale.keys():
    print('\n\t\t',i)
    # for j in locale[i][0]:
    for j in locale[i]:
        input(j)
        # locale[i][0][j] = str(mouse.position)
        locale[i][j] = str(mouse.position)
        print(locale[i][j])
        # print(locale[i][0][j])

tab = 1
while 1:
    more = input("Would you like to add more tabs?\n")
    if more == 'n':
        break
    current_tab = "Tab " + str(tab)
    location = { 'Location': str(mouse.position) }
    locale[current_tab] = location
    print(current_tab, str(mouse.position))
    tab += 1


locale['Inventory']['Iterator'] = iterator("Inventory", 4, 11 ) 
locale['Default']['Iterator'] = iterator("Default", 11, 11) 

items = {
     'Seed': 'Tab 1'
}   
locale["Items"] = items

print(locale)
write_location = os.path.join(os.environ['USERPROFILE'], "Documents\My Games\Path of Exile\locations.json")
with open(write_location, "w") as outfile:
    json.dump(locale, outfile, indent=4)
