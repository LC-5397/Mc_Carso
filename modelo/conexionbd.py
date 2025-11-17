import pyodbc

class ConexionBD:
    def __init__(self):
        self.conexion = ""
    
    def establecerConexionBD(self):
        try:
            self.conexion = pyodbc.connect(
            'DRIVER={SQL Server};'
            'SERVER=SALAF008-09\\SQLEXPRESS;'
            'DATABASE=grupoCarso;'
            'UID=sa;'
            'PWD=Password01;'
           
        )
            print("Conexión exitosa a la base de datos.")
        except Exception as e:
            print(f"Error al conectar a la base de datos: {e}")
            
    def cerrarConexionBD(self):
        if self.conexion:
            self.conexion.close()
            print("Conexión cerrada.")
            