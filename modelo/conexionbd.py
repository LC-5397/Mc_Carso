import pyodbc

class ConexionBD:
    def __init__(self):
        self.conexion = ""
    
    def establecerConexionBD(self):
        try:
            self.conexion = pyodbc.connect(
            'DRIVER={ODBC Driver 17 for SQL Server};'
            'SERVER=LAPTOP-THRU65TD;'
            'DATABASE=gurpoCarso;'
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
            