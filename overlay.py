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
        # Connecting the signal
        self.button1.clicked.connect(self.store)
        self.button2.clicked.connect(self.fill)

    @Slot()  
    def fill(self):
        fill_inventory()
    
    def store(self):
        global current_tab
        current_tab = "Default"
        store_in_stash()

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

def fill_inventory():
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

def store_in_stash():
    global current_tab
    switch('Default')
    time.sleep(.08)
    with Listener( on_press=on_press ) as listener:
        keyboard.press(Key.ctrl)
        i, j = data['Inventory']['Iterator']
        for x in range(i[0], i[1], i[2]):
            for y in range(j[0], j[1], j[2]):
                if not listener.running:
                    break
                click(x, y, 0)
                pyperclip.copy('')
                keyboard.press('c')
                keyboard.release('c')
                time.sleep(.01)
                if len(pyperclip.paste()) > 0:             
                    val = pyperclip.paste()
                    value = val[0:val.find("--------")]
                    print(value[0:-2])
                    if any( item in value for item in data["Items"] ):
                        # Double loop needs a better solution
                        save_it = [ item for item in data["Items"] if item in value][0]
                        desired_tab(data["Items"][save_it])
                        click(x,y)
                    else:
                        desired_tab("Default")
                        click(x, y)
        keyboard.release(Key.ctrl)

def switch(tab):
    x, y = location(tab)
    click(x, y)

def desired_tab(tab):
    global current_tab
    if current_tab != tab:
        current_tab = tab 
        switch(tab)
        time.sleep(.1)
    print(tab+"\n")

def location(tab, location="Location"):
    return data[tab][location][1:-1].split(',')



if __name__ == "__main__":
    json_location = os.path.join(os.environ['USERPROFILE'], "Documents\My Games\Path of Exile\locations.json")
    with open(json_location) as json_file:
        data = json.load(json_file)

    keyboard = Keyboard_Controller()
    mouse = Mouse_Controller()

    app = QApplication(sys.argv)

    widget = MyWidget()
    widget.resize(100, 50)
    widget.show()

    sys.exit(app.exec_())
