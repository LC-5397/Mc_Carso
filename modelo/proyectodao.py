from modelo.proyecto import Proyecto
from modelo.conexionbd import ConexionBD

class ProyectoDAO:
    def __init__(self):
        self.bd = ConexionBD()
        self.proyecto= Proyecto()
        
    def listarProyectos(self):
        basedatos = ConexionBD()
        basedatos.establecerConexionBD()
        sp = "EXEC dbo.sp_listar_proyectos"
        cursor = basedatos.conexion.cursor()
        cursor.execute(sp)
        datos = cursor.fetchall()
        basedatos.cerrarConexionBD()
        return datos
    
    def guardarProyecto(self):
        basedatos= ConexionBD()
        basedatos.establecerConexionBD()
        #hacemos la conexion
        sp = 'exec [dbo].[sp_insertar_proyecto] @nombre=?,@ubicacion=?, @presupuesto=?, @estado=?,@nombre_cliente=?'   
        param = (self.proyecto.nombre,self.proyecto.ubicacion,self.proyecto.presupuesto,self.proyecto.estado,self.proyecto.nombre_cliente)
        cursor = basedatos.conexion.cursor()
        cursor.execute(sp, param)     
        cursor.commit()
                
        #cerramos la conexion
        basedatos.cerrarConexionBD()

    def actualizarProyecto(self):
        basedatos = ConexionBD()
        basedatos.establecerConexionBD()
        sp = ('exec [dbo].[sp_actualizar_proyecto] @nombre_cliente=?, @nombre=?,@ubicacion=?, @presupuesto=?, @estado=?')
        param = (self.proyecto.nombre_cliente,self.proyecto.nombre,self.proyecto.ubicacion,self.proyecto.presupuesto,self.proyecto.estado)
        cursor = basedatos.conexion.cursor()
        cursor.execute(sp, param)

        resultado = cursor.fetchone()
        cursor.commit()

        basedatos.cerrarConexionBD()
        return resultado

        
    def eliminarProducto(self):
        basedatos= ConexionBD()
        basedatos.establecerConexionBD()
        #hacemos la conexion
        sp = 'exec [dbo].[sp_eliminar_producto] @nombre=?'   
        param = (self.proyecto.nombre)
        cursor = basedatos.conexion.cursor()
        cursor.execute(sp, param)     
        cursor.commit()
        
        #cerramos la conexion
        basedatos.cerrarConexionBD() 
   

    def buscarProyectoPorNombre(self,nombre):
        basedatos = ConexionBD()
        basedatos.establecerConexionBD()

        sp = "EXEC dbo.sp_buscar_proyecto_por_nombre @nombre=?"
        cursor = basedatos.conexion.cursor()
        cursor.execute(sp, (nombre,))

        datos = cursor.fetchone()

        basedatos.cerrarConexionBD()
        return datos