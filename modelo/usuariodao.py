from modelo.usuario import Usuario
from modelo.conexionbd import ConexionBD

class ProyectoDAO:
    def __init__(self):
        self.bd = ConexionBD()
        self.usuario= Usuario()

    def listarUsuario(self):
            basedatos = ConexionBD()
            basedatos.establecerConexionBD()
            sp = "EXEC dbo.sp_listar_usuarios"
            cursor = basedatos.conexion.cursor()
            cursor.execute(sp)
            datos = cursor.fetchall()
            basedatos.cerrarConexionBD()
            return datos