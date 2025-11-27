from modelo.incidentes import Incidentes
from modelo.conexionbd import ConexionBD

class IncidentesDAO:
    def __init__(self):
        self.bd = ConexionBD()
        self.proyecto= Incidentes()

    def listarIncidentes(self):
            basedatos = ConexionBD()
            basedatos.establecerConexionBD()
            sp = "EXEC dbo.sp_listar_incidentes"
            cursor = basedatos.conexion.cursor()
            cursor.execute(sp)
            datos = cursor.fetchall()
            basedatos.cerrarConexionBD()
            return datos