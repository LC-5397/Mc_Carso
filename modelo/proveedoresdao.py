from modelo.proveedores import Proveedores
from modelo.conexionbd import ConexionBD

class ProyectoDAO:
    def __init__(self):
        self.bd = ConexionBD()
        self.proveedores= Proveedores()
    
    def listarProveedores(self):
            basedatos = ConexionBD()
            basedatos.establecerConexionBD()
            sp = "EXEC dbo.sp_listar_proveedores"
            cursor = basedatos.conexion.cursor()
            cursor.execute(sp)
            datos = cursor.fetchall()
            basedatos.cerrarConexionBD()
            return datos