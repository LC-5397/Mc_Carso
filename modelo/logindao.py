from modelo.conexionbd import ConexionBD
from modelo.login import Login

class LoginDAO:
    def __init__(self):
        self.usuario = Login()

    def verificar_usuario(self, username, password):
        basedatos = ConexionBD()
        basedatos.establecerConexionBD()
        if not basedatos.conexion:
            print("No se pudo conectar a la base de datos.")
            return False
        cursor = basedatos.conexion.cursor()
        cursor.execute("EXEC dbo.sp_verificar_usuario @username=?, @password=?", (username, password))
        resultado = cursor.fetchone()
        basedatos.cerrarConexionBD()
        print(f"Resultado del SP: {resultado}")

        if resultado and resultado[0] == 1:
            return True
        else:
            return False