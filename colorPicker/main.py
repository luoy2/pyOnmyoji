import sys
from PyQt5 import QtWidgets, QtGui, QtCore, uic
import pyautogui
import logging
import keyboard
import mouse

# let pyqt crash catch the exception
sys._excepthook = sys.excepthook


def my_exception_hook(exctype, value, traceback):
    # Print the error and traceback
    print(exctype, value, traceback)
    # Call the normal Exception hook after
    sys._excepthook(exctype, value, traceback)
    sys.exit(1)


sys.excepthook = my_exception_hook

# add all the logging handler
logging.basicConfig(level=0)


class ColorPickingThread(QtCore.QThread):
    keyboard_press_signal = QtCore.pyqtSignal(str)

    def __init__(self):
        super().__init__()

    def run(self):
        pass


class MainWindow(QtWidgets.QMainWindow, uic.loadUiType('main.ui')[0]):
    keyPressed = QtCore.pyqtSignal(int)

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.cords_dict = {}
        self.color_dict = {}
        self.region = [0, 0, 0, 0]
        self.tolerance = int(self.tolerance_edit.text())
        self.cords_edit_dict = {1: self.cords_1,
                                2: self.cords_2,
                                3: self.cords_3}
        self.color_edit_dict = {1: self.color_1,
                                2: self.color_2,
                                3: self.color_3}

        self.tolerance_edit.setValidator(QtGui.QIntValidator())
        self.cb = QtWidgets.QApplication.clipboard()
        keyboard.on_press_key('1', self.color_picked, suppress=False)
        keyboard.on_press_key('2', self.color_picked, suppress=False)
        keyboard.on_press_key('3', self.color_picked, suppress=False)
        keyboard.on_press_key('c', self.generate_button_shotcut, suppress=False)
        keyboard.on_press_key('s', self.region_start, suppress=False)
        keyboard.on_press_key('a', self.region_end, suppress=False)

    def color_picked(self, keyboard_event):
        key_pressed = int(keyboard_event.name)
        pos = mouse.get_position()
        self.cords_dict[key_pressed] = pos
        pixel = pyautogui.pixel(*pos)
        self.color_dict[key_pressed] = pixel
        self.cords_edit_dict[key_pressed].setText(str(pos)[1:-1])
        self.color_edit_dict[key_pressed].setText(str(pixel)[1:-1])
        if set(self.color_dict.keys()) == set([1, 2, 3]):
            self.generate_button.setEnabled(True)

    def region_start(self, keyboard_event):
        pos = mouse.get_position()
        self.region[0] = pos[0]
        self.region[1] = pos[1]
        self.region_edit.setText(str(self.region))

    def region_end(self, keyboard_event):
        pos = mouse.get_position()
        self.region[2] = pos[0]
        self.region[3] = pos[1]
        self.region_edit.setText(str(self.region))

    def generate_button_shotcut(self, keyboard_event):
        print('generate!')
        return self.generate_button.click()

    def on_generate_button_clicked(self):
        cords_offset = self.cords_dict[1]
        result_list = []
        first_result = [(0, 0), self.color_dict[1]]
        for i in range(1, 4):
            result = [(self.cords_dict[i][0] - cords_offset[0], self.cords_dict[i][1] - cords_offset[1]),
                      self.color_dict[i]]
            result_list.append(result)
        result_str = f'({self.region}, {result_list}, {self.tolerance})'
        self.cb.clear(mode=self.cb.Clipboard)
        self.cb.setText(result_str, mode=self.cb.Clipboard)
        self.textBrowser.setText(result_str)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mw = MainWindow()
    mw.show()
    sys.exit(app.exec_())
