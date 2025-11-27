from modelo.clientes import Clientes
from modelo.conexionbd import ConexionBD

class ClientesDAO:
    def __init__(self):
        self.bd = ConexionBD()
        self.clientes= Clientes()

    def listarProyectos(self):
            basedatos = ConexionBD()
            basedatos.establecerConexionBD()
            sp = "EXEC dbo.sp_listar_clientes"
            cursor = basedatos.conexion.cursor()
            cursor.execute(sp)
            datos = cursor.fetchall()
            basedatos.cerrarConexionBD()
            return datos