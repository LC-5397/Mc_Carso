from modelo.login import Login
from modelo.conexionbd import ConexionBD

class LoginDAO:
    def __init__(self):
        self.usuario = Login()

    # =============================
    # VALIDAR LOGIN (YA LO TIENES)
    # =============================
    def verificar_usuario(self, username, password):
        basedatos = ConexionBD()
        basedatos.establecerConexionBD()

        if not basedatos.conexion:
            print("No se pudo conectar a la base de datos.")
            return False

        cursor = basedatos.conexion.cursor()
        cursor.execute(
            "EXEC dbo.sp_verificar_usuario @username=?, @password=?",
            (username, password)
        )

        resultado = cursor.fetchone()
        basedatos.cerrarConexionBD()

        return resultado and resultado[0] == 1
        

    # ============================================
    # NUEVO: OBTENER DATOS DEL USUARIO POR USERNAME
    # ============================================
    def obtener_datos_usuario(self, username):
        basedatos = ConexionBD()
        basedatos.establecerConexionBD()

        if not basedatos.conexion:
            print("No se pudo conectar a la base de datos.")
            return None

        try:
            cursor = basedatos.conexion.cursor()

            # SUPONIENDO QUE TU SP RECIBE @username
            cursor.execute(
                "EXEC dbo.sp_datos_usuario @username=?",
                (username,)
            )

            fila = cursor.fetchone()

            if fila:
                # Ajusta los índices según lo que devuelva tu SP
                return {
                    "usuario": fila[0],
                    "nombre": fila[1],
                    "cargo": fila[2],
                    "salario": fila[3]
                }
            else:
                return None
        
        except Exception as e:
            print("ERROR al obtener datos del usuario:", e)
            return None

        finally:
            basedatos.cerrarConexionBD()
