import pyodbc
from modelo.contacto import Contacto
from modelo.conexionbd import ConexionBD


class ContactoDAO:

    @staticmethod
    def obtener_contactos():
        conexion = ConexionBD()
        conexion.establecerConexionBD()

        lista = []

        try:
            cursor = conexion.conexion.cursor()
            cursor.execute("EXEC sp_obtener_contactos")

            for nombre, cargo in cursor.fetchall():
                correo_generado = (
                    nombre.lower()
                    .replace(" ", ".")
                    .replace("á", "a")
                    .replace("é", "e")
                    .replace("í", "i")
                    .replace("ó", "o")
                    .replace("ú", "u")
                    + "@grupocarso.com"
                )

                lista.append(Contacto(nombre, cargo, correo_generado))

        except Exception as e:
            print("Error cargando contactos:", e)

        finally:
            conexion.cerrarConexionBD()

        return lista
