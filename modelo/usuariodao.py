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
        
    def obtener_datos_usuario(self, username, password):
        basedatos = ConexionBD()
        basedatos.establecerConexionBD()

        cursor = basedatos.conexion.cursor()
        cursor.execute(
            "EXEC dbo.sp_login_info_completa @username=?, @password=?",
            (username, password)
        )

        fila = cursor.fetchone()
        basedatos.cerrarConexionBD()

        if fila:
            return {
                "nombre": fila[0],
                "cargo": fila[1],
                "salario": fila[2],
            }
        else:
            return None

