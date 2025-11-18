# 1.- Importar librerías
import sys
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from modelo.logindao import LoginDAO  

# 2.- Clase principal para manejar el login
class Load_ui_login(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("ui/login.ui", self)

        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setWindowOpacity(1.0)

        # Páginas del stackedWidget
        self.page_login = self.findChild(QtWidgets.QWidget, "page_login")
        self.page_error = self.findChild(QtWidgets.QWidget, "page_password")

        self.stackedWidget.setCurrentWidget(self.page_login)

        # Botones
        self.Button_login.clicked.connect(self.ingresar)
        #Cerrar ventana
        #self.boton_salir_login.clicked.connect(lambda: self.close())
        
    # LOGIN

    def ingresar(self):
        usuario = "admin"
        contrasena = "admin"
        login_dao = LoginDAO()
        valido = login_dao.verificar_usuario(usuario, contrasena)

        if valido:
            print("Login correcto. Abriendo menú...")

            # Importación aquí para evitar ciclos entre módulos
            from load.load_ui_menu import Load_ui_menu
            self.ventana_menu = Load_ui_menu()  # GUARDA referencia
            self.ventana_menu.show()
            self.close()  # CERRAMOS login
        else:
            print("Usuario o contraseña incorrectos.")
            self.stackedWidget.setCurrentWidget(self.page_error)



    def abrir_menu(self):
        self.close()
        from load.load_ui_proyectos import Load_ui_proyectos
        self.empleados = Load_ui_proyectos()
        self.empleados.show()


    # CERRAR SESIÓN
 
    def cerrar_sesion(self):
        print("Cerrando sesión...")
        self.usuario_login.clear()
        self.password_login.clear()
        self.stackedWidget.setCurrentWidget(self.page_login)
