import sys
from PyQt5 import QtCore
from PyQt5.QtCore import QPropertyAnimation
from PyQt5 import QtCore, QtGui, QtWidgets, uic  
#2.- Cargar archivo .ui
class Load_ui_menu(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        # Cargar archivo .ui
        uic.loadUi("ui/ui_menu.ui", self)