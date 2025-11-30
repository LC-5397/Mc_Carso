import sys
from PyQt5 import QtCore
from PyQt5.QtCore import QPropertyAnimation
from PyQt5 import QtCore, QtGui, QtWidgets, uic  
from modelo.proyectodao import ProyectoDAO
#2.- Cargar archivo .ui
class Load_ui_Proyecto(QtWidgets.QMainWindow):
    def __init__(self, username, nombre, cargo, salario):
        super().__init__()
        uic.loadUi("ui/menu_proyectos.ui", self)

        # Guardamos los datos del usuario para poder regresarlos al menú
        self.username = username
        self.nombre = nombre
        self.cargo = cargo
        self.salario = salario

        self.boton_salir.clicked.connect(self.regresar_menu)

        self.proyectodao = ProyectoDAO() 
        self.menu_colapsado= False
        
        #3.- Configurar contenedores
        #eliminar barra y de titulo - opacidad
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setWindowOpacity(1)
        #Cerrar ventana
        #self.boton_salir.clicked.connect(self.volver_al_menu)
        
        # mover ventana
        self.frame_superior.mouseMoveEvent = self.mover_ventana
        #menu lateral
        self.boton_menu.clicked.connect(self.mover_menu)
        #Fijar ancho columnas
        self.tabla_proyectos.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        
        #4.- Conectar botones a funciones
        #Botones para cambiar de página
        self.boton_agregar.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.page_agregar))
        self.boton_proyectos.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.page_menu_proyectos))
        self.boton_actualizar.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.page_actualizar))
        self.boton_eliminar.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.page_eliminar))
        
                
        #Botones para guardar, buscar, actualizar, eliminar y salir
        self.boton_agregar_agregar.clicked.connect(self.guardar_proyecto)
        self.boton_actualizar_actualizar.clicked.connect(self.actualizar_proyecto)
        self.boton_eliminar_eliminar.clicked.connect(self.eliminar_proyecto)
        self.botonaccion_refrescar.clicked.connect(self.llenar_tabla)
        
        self.boton_buscar_actualizar.clicked.connect(self.buscar_actualizar)
        self.boton_buscar_eliminar.clicked.connect(self.buscar_eliminar)

        self.botonaccion_refrescar.clicked.connect(self.llenar_tabla)
        
    
#5.- Operaciones con el modelo de datos 

    def regresar_menu(self):
        from load.load_ui_menu import Load_ui_Menu
        self.close() 
        self.menu = Load_ui_Menu(
            username=self.username,
            nombre=self.nombre,
            cargo=self.cargo,
            salario=self.salario
        )
        self.menu.show()
            
            
    def llenar_tabla(self):
        self.tabla_proyectos.setRowCount(0)
        proyectos = self.proyectodao.listarProyectos()

        for proyecto in proyectos:
            fila = self.tabla_proyectos.rowCount()
            self.tabla_proyectos.insertRow(fila)

            self.tabla_proyectos.setItem(fila, 0, QtWidgets.QTableWidgetItem(str(proyecto.nombre)))
            self.tabla_proyectos.setItem(fila, 1, QtWidgets.QTableWidgetItem(str(proyecto.estado)))

            # --- BOTÓN DE DETALLE ---
            btn = QtWidgets.QPushButton()
            btn.setIcon(QtGui.QIcon("resources/imagenes/proyectos/cursor.png")) 
            btn.setIconSize(QtCore.QSize(32, 32))
            btn.setStyleSheet("border: none;")  

            # IMPORTANTE: guardar el id del proyecto
            btn.clicked.connect(lambda checked, nombre=proyecto.nombre: self.page_detalle(nombre))

            self.tabla_proyectos.setCellWidget(fila, 2, btn)

    def page_detalle(self, nombre):
        # Obtener el proyecto desde la BD
        proyecto = self.proyectodao.buscarProyectoPorNombre(nombre)

        if proyecto is None:
            print("Proyecto no encontrado")
            return

        # Cambiar página
        self.stackedWidget.setCurrentWidget(self.page_detalle_proyecto)

        # Rellenar tus line edit (o labels, lo que tengas)
        self.nombre_detalles.setText(proyecto.nombre)
        self.ubicacion_detalles.setText(proyecto.ubicacion)
        self.presupuesto_detalles.setText(str(proyecto.presupuesto))
        self.estado_detalles.setText(proyecto.estado)
        self.cliente_detalles.setText(proyecto.nombre_cliente)   

        
    def volver_al_menu(self):
        self.close()
        # Importar la clase correcta
        from load.load_ui_login import Load_ui_login
        
        # Crear nueva instancia del login
        self.login_dialog = Load_ui_login()
        self.login_dialog.show()
        self.login_dialog.stackedWidget.setCurrentWidget(self.login_dialog.page_proyectos)
        
    def guardar_proyecto(self):
        nombre = self.nombre_agregar.text()
        ubicacion = self.ubicacion_agregar.text()
        presupuesto = self.presupuesto_agregar.text()
        estado = self.estado_agregar.text()
        cliente = self.cliente_agregar.text()

        if not nombre:
            print("Debes ingresar el Nombre del proyecto.")
            return

        self.proyectodao.proyecto.nombre = nombre
        self.proyectodao.proyecto.ubicacion = ubicacion
        self.proyectodao.proyecto.presupuesto = presupuesto
        self.proyectodao.proyecto.estado = estado
        self.proyectodao.proyecto.nombre_cliente = cliente

        self.proyectodao.guardarProyecto()

        

    def actualizar_proyecto(self):
        nombre = self.nombre_actualizar.text()
        ubicacion = self.ubicacion_actualizar.text()
        presupuesto = self.presupuesto_actualizar.text()
        estado = self.estado_actualizar.text()
        cliente = self.cliente_actualizar.text()

        if not nombre:
            print("Debes ingresar el Nombre del proyecto.")
            return

        self.proyectodao.proyecto.nombre = nombre
        self.proyectodao.proyecto.ubicacion = ubicacion
        self.proyectodao.proyecto.presupuesto = presupuesto
        self.proyectodao.proyecto.estado = estado
        self.proyectodao.proyecto.nombre_cliente = cliente

        self.proyectodao.actualizarProyecto()

   
    def eliminar_proyecto(self):
        nombre= self.nombre_eliminar.text()
        if not nombre:
            print("Debes ingresar el Nombre del a eliminar.")
            return
        self.proyectodao.proyecto.nombre = nombre
        self.proyectodao.eliminarProyecto()


    def buscar_actualizar(self):
        nombre = self.nombre_actualizar.text().strip()
        if not nombre:
            print("Debes ingresar el Nombre del proyecto a buscar.")
            return
        self.proyectodao.proyecto.nombre = nombre
        proyecto = self.proyectodao.buscarProyectoPorNombre(nombre)
        if proyecto:
            self.ubicacion_actualizar.setText(str(proyecto.ubicacion))
            self.presupuesto_actualizar.setText(str(proyecto.presupuesto))  
            self.estado_actualizar.setText(str(proyecto.estado))
            self.cliente_actualizar.setText(str(proyecto.nombre_cliente))
            print("Proyecto encontrado.")
        else:
            print("No se encontró ningún proyecto con ese nombre.")
    
    def buscar_eliminar(self):
        nombre = self.nombre_eliminar.text().strip()
        if not nombre:
            print("Debes ingresar el SKU del producto a buscar.")
            return
        self.proyectodao.proyecto.nombre = nombre
        proyecto = self.proyectodao.buscarProyectoPorNombre(nombre)
        if proyecto:
            self.ubicacion_eliminar.setText(str(proyecto.ubicacion))
            self.presupuesto_eliminar.setText(str(proyecto.presupuesto))  
            self.estado_eliminar.setText(str(proyecto.estado))
            self.cliente_eliminar.setText(str(proyecto.nombre_cliente))
            print("Proyecto encontrado.")
        else:
            print("No se encontró ningún proyecto con ese nombre.")
    

    def mousePressEvent(self, event):
        self.clickPosition = event.globalPos()
    def mover_ventana(self, event):
        if self.isMaximized() == False:			
            if event.buttons() == QtCore.Qt.LeftButton:
                self.move(self.pos() + event.globalPos() - self.clickPosition)
                self.clickPosition = event.globalPos()
                event.accept()

        if event.globalPos().y() <=20:
            self.showMaximized()
        else:
            self.showNormal()
            

    #7.- Mover menú
    def mover_menu(self):
        # IMPORTANTE: permitir que el frame pueda bajar a 0
        self.frame_botones_menu.setMaximumWidth(self.frame_botones_menu.width())

        width = self.frame_botones_menu.maximumWidth()

        if self.menu_colapsado:
            new_width = 200   # abierto
        else:
            new_width = 0     # cerrado

        self.anim = QPropertyAnimation(self.frame_botones_menu, b"maximumWidth")
        self.anim.setDuration(300)
        self.anim.setStartValue(width)
        self.anim.setEndValue(new_width)
        self.anim.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
        self.anim.start()

        self.menu_colapsado = not self.menu_colapsado