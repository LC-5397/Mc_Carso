from modelo.empleados import Empleados
from modelo.conexionbd import ConexionBD

class ProyectoDAO:
    def __init__(self):
        self.bd = ConexionBD()
        self.empleados= Empleados()

    def listarEmpleados(self):
            basedatos = ConexionBD()
            basedatos.establecerConexionBD()
            sp = "EXEC dbo.sp_listar_empleados"
            cursor = basedatos.conexion.cursor()
            cursor.execute(sp)
            datos = cursor.fetchall()
            basedatos.cerrarConexionBD()
            return datos