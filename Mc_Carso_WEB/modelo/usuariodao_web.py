from modelo.usuario_web import UsuarioWEB
from modelo.conexionbd import ConexionBD

class UsuarioDAO:
    def __init__(self):
        pass  # no necesitamos self.usuario

    # Verificar login
    def verificar_usuario(self, nombre, clave):
        basedatos = ConexionBD()
        basedatos.establecerConexionBD()
        if not basedatos.conexion:
            print("No se pudo conectar a la base de datos.")
            return False

        cursor = basedatos.conexion.cursor()
        cursor.execute(
            "EXEC dbo.sp_verificar_usuario_WEB @nombre=?, @clave=?",
            (nombre, clave)
        )
        resultado = cursor.fetchone()
        basedatos.cerrarConexionBD()

        return bool(resultado and resultado[0] == 1)

    # Registrar usuario
    def registrar_usuario(self, usuario: UsuarioWEB):
        basedatos = ConexionBD()
        basedatos.establecerConexionBD()
        if not basedatos.conexion:
            print("No se pudo conectar a la base de datos.")
            return None

        cursor = basedatos.conexion.cursor()
        cursor.execute(
            "EXEC dbo.sp_registrar_usuario_WEB @nombre=?, @correo=?, @clave=?",
            (usuario.nombre, usuario.correo, usuario.clave)
        )
        resultado = cursor.fetchone()
        basedatos.conexion.commit()
        basedatos.cerrarConexionBD()
        return resultado[0] if resultado else None
