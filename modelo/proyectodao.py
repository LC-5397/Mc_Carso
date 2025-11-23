from modelo.proyecto import Proyecto
from modelo.conexionbd import ConexionBD

class ProyectoDAO:
    def __init__(self):
        self.bd = ConexionBD()
        self.proyecto= Proyecto()
        
    def listarProyectos(self):
        basedatos = ConexionBD()
        basedatos.establecerConexionBD()
        sp = "EXEC dbo.sp_listar_proyecto"
        cursor = basedatos.conexion.cursor()
        cursor.execute(sp)
        datos = cursor.fetchall()
        basedatos.cerrarConexionBD()
        return datos
    
    def guardarProyecto(self):
        basedatos = ConexionBD()
        basedatos.establecerConexionBD()
        sp = """EXEC dbo.sp_insertar_proyecto @nombre_cliente=?,@nombre_proyecto=?,@ubicacion=?, @presupuesto=?, @estado=?"""
        params = (self.proyecto.nombre_cliente,self.proyecto.nombre,self.proyecto.ubicacion,self.proyecto.presupuesto,self.proyecto.estado)
        cursor = basedatos.conexion.cursor()
        cursor.execute(sp, params)
        cursor.commit()
        basedatos.cerrarConexionBD()


    def actualizarProyecto(self):
        basedatos = ConexionBD()
        basedatos.establecerConexionBD()
        sp = """EXEC dbo.sp_actualizar_proyecto @nombre_cliente=?,@nombre_proyecto=?,@ubicacion=?, @presupuesto=?, @estado=?"""
        param = (self.proyecto.nombre_cliente,self.proyecto.nombre,self.proyecto.ubicacion,self.proyecto.presupuesto,self.proyecto.estado)
        cursor = basedatos.conexion.cursor()
        cursor.execute(sp, param)
        resultado = cursor.fetchone()
        cursor.commit()
        basedatos.cerrarConexionBD()
        return resultado
        
        
    def eliminarProyecto(self):
        basedatos= ConexionBD()
        basedatos.establecerConexionBD()
        #hacemos la conexion
        sp = 'exec [dbo].[sp_eliminar_proyecto] @nombre=?'   
        param = (self.proyecto.nombre)
        cursor = basedatos.conexion.cursor()
        cursor.execute(sp, param)     
        cursor.commit()
        
        #cerramos la conexion
        basedatos.cerrarConexionBD() 
   

    def buscarProyectoPorNombre(self, nombre):
        basedatos = ConexionBD()
        basedatos.establecerConexionBD()

        sp = "EXEC dbo.sp_buscar_proyecto_por_nombre @nombre=?"
        cursor = basedatos.conexion.cursor()
        cursor.execute(sp, (nombre,))

        row = cursor.fetchone()
        basedatos.cerrarConexionBD()

        if row is None:
            return None

        proyecto = Proyecto()

        proyecto.id_proyecto = row[0]
        proyecto.nombre = row[1]
        proyecto.ubicacion = row[2]
        proyecto.presupuesto = row[3]
        proyecto.estado = row[4]
        proyecto.nombre_cliente = row[5]  # <-- IMPORTANTE

        return proyecto

