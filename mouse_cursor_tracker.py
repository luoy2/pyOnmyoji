from tkinter import *
import pyautogui, sys
import threading
import queue
import time




serialdata = []
data = True

class SensorThread(threading.Thread):
    def run(self):
        try:
            i = 0
            while True:
                pos = pyautogui.position()
                serialdata.append(f'{pos}..{pyautogui.pixel(*pos)}')
                i += 1
                time.sleep(1)
        except KeyboardInterrupt:
            exit()


class Gui(object):
    def __init__(self):
        self.root = Tk()
        self.lbl = Label(self.root, text="")
        self.readSensor()

    def run(self):
        self.lbl.pack()
        self.root.mainloop()


    def readSensor(self):
        self.lbl["text"] = serialdata[-1]
        self.root.update()
        self.root.after(100, self.readSensor)


if __name__ == "__main__":
    SensorThread().start()
    Gui().run()