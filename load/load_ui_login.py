import sys
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from modelo.logindao import LoginDAO  
from modelo.usuariodao import UsuarioDAO

class Load_ui_login(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("ui/login.ui", self)

        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setWindowOpacity(1.0)

        self.Button_login.clicked.connect(self.ingresar)

    def ingresar(self):
        usuario = self.usuario_login.text().strip()
        contrasena = self.password_login.text().strip()

        login_dao = LoginDAO()
        usuario_dao = UsuarioDAO()

        valido = login_dao.verificar_usuario(usuario, contrasena)

        if not valido:
            print("Usuario o contraseña incorrectos.")
            return

        print("Login correcto... recuperando datos del usuario")

        datos = usuario_dao.obtener_datos_usuario(usuario, contrasena)

        if datos is None:
            print("No se encontraron datos asociados.")
            return

        nombre = datos["nombre"]
        cargo = datos["cargo"]
        salario = datos["salario"]

        # 3. Abrir menú enviando los datos
        self.abrir_menu(usuario, nombre, cargo, salario)


    def abrir_menu(self, username, nombre, cargo, salario):
        self.close()
        from load.load_ui_menu import Load_ui_Menu
        self.menu = Load_ui_Menu(username, nombre, cargo, salario)
        self.menu.show()
