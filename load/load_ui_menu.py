import sys
from PyQt5 import QtWidgets, uic, QtCore, QtGui
from modelo.clientesdao import ClientesDAO
from modelo.empleadosdao import EmpleadosDAO
from modelo.usuariodao import UsuarioDAO
from modelo.proveedoresdao import ProveedoresDAO
from modelo.incidentesdao import IncidentesDAO

class Load_ui_Menu(QtWidgets.QMainWindow):
    def __init__(self, username, nombre, cargo, salario):
        super().__init__()
        uic.loadUi("ui/ui_menu.ui", self)

        # Guardar datos
        self.username = username
        self.nombre = nombre
        self.cargo = cargo
        self.salario = salario

        # Mostrar en los labels de page_usuario
        self.label_nombreusuario.setText(str(self.nombre))
        self.label_cargousuario.setText(str(self.cargo))
        self.label_salariousuario.setText(str(self.salario))

        # 2.- Configuración de Ventana (Sin bordes y transparencia)
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setWindowOpacity(1)
        
        self.usuario_dao = UsuarioDAO()
        self.cliente_dao = ClientesDAO()
        self.empleado_dao = EmpleadosDAO()
        self.proveedor_dao = ProveedoresDAO()
        self.incidente_dao = IncidentesDAO()

        # 4.- Configurar Interfaz Inicial
        self.stackedWidget.setCurrentWidget(self.page_usuario) # Página de inicio por defecto
        self.configurar_tablas()

        # 5.- Conectar Botones del Menú Lateral (Navegación)
        # boton_usuario
        self.boton_usuario.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.page_usuario))
        # boton_clientes
        self.boton_clientes.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.page_clientes))
        # boton_empleados
        self.boton_empleados.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.page_empleados))
        # boton_proveedores
        self.boton_proveedores.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.page_proveedores))
        # boton_proyectos
        self.boton_proyectos.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.page_proyectos))
        # boton_incidentes
        self.boton_incidentes.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.page_incidentes))

        # 6.- Conectar Botones de Acción (Actualizar, Salir, etc)
        # Botón Salida 
        #self.boton_salida.clicked.connect(self.close)
        
        # Botón Anterior (Podría usarse para minimizar o volver atrás) 
        self.boton_anterior.clicked.connect(self.showMinimized)

        # Botón "Ir a Proyectos" dentro de la página proyectos 
        self.pushButton.clicked.connect(self.abrir_modulo_proyectos)

        # Botones de "Actualizar" en cada página
        self.boton_actualizar_2.clicked.connect(self.llenar_tabla_clientes)
        self.boton_actualizar_3.clicked.connect(self.llenar_tabla_empleados)
        self.boton_actualizar.clicked.connect(self.llenar_tabla_proveedores)
        self.boton_actualizar_5.clicked.connect(self.llenar_tabla_incidentes)
        self.boton_actualizar_4.clicked.connect(self.llenar_tabla_usuario_proyectos)

        self.frame_superior.mouseMoveEvent = self.mover_ventana
        self.clickPosition = None

    # --- CONFIGURACIÓN VISUAL ---
    def configurar_tablas(self):
        """Estira las columnas de las tablas para ocupar todo el ancho"""
        header_style = QtWidgets.QHeaderView.Stretch
        
        # Page Empleados 
        self.tabla_empleados.horizontalHeader().setSectionResizeMode(header_style)
        
        # Page Clientes 
        self.tabla_clientes.horizontalHeader().setSectionResizeMode(header_style)
        
        # Page Proveedores (Nota: en el XML se llama 'tableWidget') 
        self.tableWidget.horizontalHeader().setSectionResizeMode(header_style)
        
        # Page Incidentes 
        self.tabla_incidentes.horizontalHeader().setSectionResizeMode(header_style)
        
        # Page Usuario (Tabla de proyectos del usuario) 
        self.tableWidget_2.horizontalHeader().setSectionResizeMode(header_style)

    # --- MÉTODOS PARA LLENAR TABLAS ---
    def llenar_tabla_clientes(self):
        datos = self.cliente_dao.listarClientes() 
        self.tabla_clientes.setRowCount(len(datos))
        fila = 0
        for item in datos:
            self.tabla_clientes.setItem(fila, 0, QtWidgets.QTableWidgetItem(str(item[0])))
            self.tabla_clientes.setItem(fila, 1, QtWidgets.QTableWidgetItem(str(item[1])))
            self.tabla_clientes.setItem(fila, 2, QtWidgets.QTableWidgetItem(str(item[2])))
            self.tabla_clientes.setItem(fila, 3, QtWidgets.QTableWidgetItem(str(item[3])))
            fila += 1

    def llenar_tabla_empleados(self):
        datos = self.empleado_dao.listarEmpleados()
        self.tabla_empleados.setRowCount(len(datos))
        fila = 0
        for item in datos:
            self.tabla_empleados.setItem(fila, 0, QtWidgets.QTableWidgetItem(str(item[0]))) # id
            self.tabla_empleados.setItem(fila, 1, QtWidgets.QTableWidgetItem(str(item[1]))) # Proyecto
            self.tabla_empleados.setItem(fila, 2, QtWidgets.QTableWidgetItem(str(item[2]))) # Nombre
            self.tabla_empleados.setItem(fila, 3, QtWidgets.QTableWidgetItem(str(item[3]))) # Salario
            fila += 1

    def llenar_tabla_proveedores(self):
        datos = self.proveedor_dao.listarProveedores()
        self.tableWidget.setRowCount(len(datos))
        fila = 0
        for item in datos:
            self.tableWidget.setItem(fila, 0, QtWidgets.QTableWidgetItem(str(item[1]))) # Nombre
            self.tableWidget.setItem(fila, 1, QtWidgets.QTableWidgetItem(str(item[2]))) # Contacto
            self.tableWidget.setItem(fila, 2, QtWidgets.QTableWidgetItem(str(item[3]))) # Direccion
            fila += 1

    def llenar_tabla_incidentes(self):
        datos = self.incidente_dao.listarIncidentes()
        self.tabla_incidentes.setRowCount(len(datos))
        fila = 0
        for item in datos:
            self.tabla_incidentes.setItem(fila, 0, QtWidgets.QTableWidgetItem(str(item[0]))) # id
            self.tabla_incidentes.setItem(fila, 1, QtWidgets.QTableWidgetItem(str(item[1]))) # Proyecto
            self.tabla_incidentes.setItem(fila, 2, QtWidgets.QTableWidgetItem(str(item[2]))) # Empleado
            self.tabla_incidentes.setItem(fila, 3, QtWidgets.QTableWidgetItem(str(item[3]))) # Fecha
            fila += 1

    def llenar_tabla_usuario_proyectos(self):
        datos = self.usuario_dao.listarUsuario()
        self.tableWidget_2.setRowCount(len(datos))
        fila = 0
        for item in datos:
            self.tableWidget_2.setItem(fila, 0, QtWidgets.QTableWidgetItem(str(item[1]))) # Usuario
            self.tableWidget_2.setItem(fila, 1, QtWidgets.QTableWidgetItem(str(item[2]))) # Password
            fila += 1

    def abrir_modulo_proyectos(self):  
        from load.load_ui_proyectos import Load_ui_Proyecto
        self.ventana_proyectos = Load_ui_Proyecto(
            self.username,
            self.nombre,
            self.cargo,
            self.salario
        )
        self.ventana_proyectos.show()
        self.close()

    # --- LÓGICA DE VENTANA (MOVER) ---
    def mousePressEvent(self, event):
        self.clickPosition = event.globalPos()

    def mover_ventana(self, event):
        if self.isMaximized() == False:
            if event.buttons() == QtCore.Qt.LeftButton:
                if self.clickPosition:
                    self.move(self.pos() + event.globalPos() - self.clickPosition)
                    self.clickPosition = event.globalPos()
                    event.accept()
        
        if event.globalPos().y() <= 20:
            self.showMaximized()
        else:
            self.showNormal()