from modelo.contacto import Contacto
import reflex as rx

class ContactoState(rx.State):
    # Variable para saber si el usuario está logueado
    is_logged: bool = False
    
    # Lista de contactos tipada como Contacto
    lista_contactos: list[Contacto] = []

    