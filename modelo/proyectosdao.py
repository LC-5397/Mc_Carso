from modelo.proyecto import Proyecto
from modelo.conexionbd import ConexionBD

class ProyectoDAO:
    def __init__(self):
        self.bd = ConexionBD()
        self.proyecto= Proyecto()

