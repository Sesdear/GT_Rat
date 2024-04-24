import sys

from PyQt6.QtWidgets import QApplication, QFrame
from PyQt6 import uic
import tkinter as tk

class Window(QFrame):
    def __init__(self):
        super().__init__()
        self.ui = uic.loadUi("main_gui.ui", self)
        self.show()




if __name__ == '__main__':
    if __name__ == "__main__":
        app = QApplication(sys.argv)
        window = Window()
        window.show()
        sys.exit(app.exec())