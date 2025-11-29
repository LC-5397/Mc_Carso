from modelo.usuario import Usuario
from modelo.conexionbd import ConexionBD

class UsuarioDAO:
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
    
    def validarLogin(self, username, password):
        basedatos = ConexionBD()
        basedatos.establecerConexionBD()
        # Llamamos al procedimiento almacenado
        sql = "EXEC dbo.sp_login_info_completa @username = ?, @password = ?"
        cursor = basedatos.conexion.cursor()
        cursor.execute(sql, (username, password))
        datos = cursor.fetchone() 
        basedatos.cerrarConexionBD()
        return datos # Retorna la info del empleado o None si falló