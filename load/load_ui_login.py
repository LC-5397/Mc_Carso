# 1.- Importar librerías
import sys
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from modelo.logindao import LoginDAO  

# 2.- Clase principal para manejar el login
class Load_ui_login(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("ui/login.ui", self)

        # Configuración de ventana
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setWindowOpacity(1.0)

        # Páginas del stackedWidget
        self.page_login = self.findChild(QtWidgets.QWidget, "page_login")

        # Botones
        self.Button_login.clicked.connect(self.ingresar)
        #Cerrar ventana
        #self.boton_salir_login.clicked.connect(lambda: self.close())

    # LOGIN

    def ingresar(self):
        
        usuario=self.usuario_login.text().strip()
        contrasena=self.password_login.text().strip()
        login_dao = LoginDAO()
        valido = login_dao.verificar_usuario(usuario, contrasena)

        if valido:
            print("Login correcto. Abriendo menú...")
            self.abrir_menu()
        else:
            print("Usuario o contraseña incorrectos.")
            #self.stackedWidget.setCurrentWidget(self.page_error)


    def abrir_menu(self):
        self.close()
        from load.load_ui_proyectos import Load_ui_Proyecto
        self.empleados = Load_ui_Proyecto()
        self.empleados.show()


    # CERRAR SESIÓN
 
    def cerrar_sesion(self):
        print("Cerrando sesión...")
        self.usuario_login.clear()
        self.password_login.clear()
        self.stackedWidget.setCurrentWidget(self.page_login)
