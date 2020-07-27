from pynput.mouse import Controller as Mouse_Controller
from pynput.mouse import Button
from pynput.keyboard import Controller as Keyboard_Controller
from pynput.keyboard import Key, Listener
from pynput import keyboard as Keyboard
import time, sys, pyperclip, json, re, os
from PySide2.QtWidgets import (QApplication, QLabel, QPushButton, QVBoxLayout, QWidget)
from PySide2.QtCore import Slot, Qt

class MyWidget(QWidget):
    def __init__(self):
        QWidget.__init__(self)

        self.button1 = QPushButton("Store")
        self.button2 = QPushButton("Fill")

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.button1)
        self.layout.addWidget(self.button2)
        self.setLayout(self.layout)
        # Make window stay on top
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        # Git rid of minimize etc.. 
        # self.setWindowFlags(Qt.FramelessWindowHint)

        # Connecting the signal
        self.button1.clicked.connect(self.store)
        self.button2.clicked.connect(self.fill)

    @Slot()  
    def fill(self):
        fill_it()
    
    def store(self):
        store_it()



def click(x_axis, y_axis, times_to_click=1, seconds_after_moving_mouse=.01):
    mouse = Mouse_Controller()
    mouse.position = ( x_axis, y_axis )
    time.sleep( seconds_after_moving_mouse )
    if times_to_click != 0:
        mouse.click(Button.left, times_to_click)
        time.sleep( seconds_after_moving_mouse )

def on_press(key):
    if key == Key.up:
        # Stop listener
        return False

def fill_it():
    # switch('Default')
    with Listener( on_press=on_press ) as listener:
        keyboard = Keyboard_Controller()
        keyboard.press(Key.ctrl_l)
        i, j = data['Default']['Iterator']
        for x in range(i[0], i[1], i[2]):
            for y in range(j[0], j[1], j[2]):
                if not listener.running:
                    break
                click(x, y)
        keyboard.release(Key.ctrl)

def store_it():
    time.sleep(.08)
    switch('Default')
    global current_tab
    fragments = [
        "^Sacrifice at.*",
        ".*Splinter.*",
        "Divine Vessel",
        "Offering to the Goddess",
        ".*Scarab.*"
    ]
    reg_list = [re.compile(x) for x in fragments]
    with Listener( on_press=on_press ) as listener:
        keyboard.press(Key.ctrl)
        i, j = data['Inventory']['Iterator']
        for x in range(i[0], i[1], i[2]):
            for y in range(j[0], j[1], j[2]):
                if not listener.running:
                    break
                click(x, y, 0)
                pyperclip.copy('')
                print(x,y)
                keyboard.press('c')
                keyboard.release('c')
                time.sleep(.01)
                item = []
                if len(pyperclip.paste()) > 0:             
                    val = pyperclip.paste()
                    value = val[0:val.find("--------")]
                    item.append(pyperclip.paste().split('\n')[0])
                    item.append(pyperclip.paste().split('\n')[1])
                    # for ike in data["Items"]:
                    #     if ike in value:
                    #         print(ike)
                    if "Map" in value: 
                        desired_tab("Map")
                        click(x, y)
                    elif "Essence" in value:
                        desired_tab("Essence")
                        click(x, y)
                    elif "Card" in value:
                        desired_tab("Card")
                        click(x, y)
                    elif any( item in value for item in data["Items"] ):
                        # Double loop
                        save_it = [ item for item in data["Items"] if item in value]
                    elif any( reg.match(item[1]) for reg in reg_list):
                        desired_tab("Fragment")
                        click(x, y)
                    elif "Currency" in item[0] and "Seed" not in item[1]:
                        desired_tab("Currency")
                        click(x, y)
                    else:
                        desired_tab("Default")
                        print('yes')
                        click(x, y)
        keyboard.release(Key.ctrl)


def desired_tab(tab):
    global current_tab
    if current_tab != tab:
        current_tab = tab 
        switch(tab)
        print(tab)
        time.sleep(.1)

def location(tab, location="Location"):
    return data[tab][location][1:-1].split(',')

def switch(tab):
    i = location(tab)
    click(i[0], i[1])

if __name__ == "__main__":
    json_location = os.path.join(os.environ['USERPROFILE'], "Documents\My Games\Path of Exile\locations.json")
    with open(json_location) as json_file:
        data = json.load(json_file)

    keyboard = Keyboard_Controller()
    mouse = Mouse_Controller()
    current_tab = "Default"

    app = QApplication(sys.argv)

    widget = MyWidget()
    widget.resize(100, 50)
    widget.show()

    sys.exit(app.exec_())
