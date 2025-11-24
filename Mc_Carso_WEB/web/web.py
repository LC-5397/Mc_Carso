import reflex as rx

# ----- STATE -----

class State(rx.State):
    menu_open: bool = False
    current_user: str = ""  # Nuevo estado para el usuario

    def toggle_menu(self):
        self.menu_open = not self.menu_open
    
    def set_user(self, username: str):
        """Función para establecer el usuario desde BD"""
        self.current_user = username
    
    def handle_login(self, form_data: dict):
        """Maneja el inicio de sesión"""
        username = form_data.get("username", "")
        password = form_data.get("password", "")
        
        # Aquí iría tu lógica de autenticación con la base de datos
        # Por ahora simulamos un login exitoso
        self.set_user(username)
        
        # Redirigir a la página principal después del login
        return rx.redirect("/")

# ----- COMPONENTES -----

def navbar() -> rx.Component:
    return rx.box(
        # Barra azul transparente
        rx.hstack(
            # Icono menú
            rx.image(
                src="/menu.png",       # imagen de menu
                width="50px",
                height="50px",
                cursor="pointer",
                on_click=State.toggle_menu,
            ),
            # Título centrado
            rx.spacer(),
            rx.text(
                "Mc Carso",
                font_size="40px",
                font_weight="bold",
                color="white",
            ),
            rx.spacer(),

            # Mostrar nombre de usuario si está logueado, sino botón de login
            rx.cond(
                State.current_user != "",
                # Usuario logueado - mostrar nombre en esquina
                rx.hstack(
                    rx.text(
                        f"Bienvenido, {State.current_user}",
                        color="white",
                        font_weight="bold",
                        font_size="16px",
                    ),
                    spacing="2",
                ),
                # Usuario no logueado - mostrar botón login
                rx.button(
                    "Login",
                    bg="#87B4FA",
                    color="black",
                    padding="10px 15px",
                    border_radius="8px",
                    on_click=lambda: rx.redirect("/login"),
                ),
            ),

            padding="15px",
            bg= "#000145",  # color de barra
            backdrop_filter="blur(4px)",
            align="center",
            position="fixed",
            top="0px",
            left="0px",
            right="0px",
            z_index="1000",
        ),

        # Menú desplegable
        rx.cond(
            State.menu_open,
            rx.box(
                rx.vstack(
                    rx.link("Inicio", href="/", color="white", font_size="20px"),
                    rx.link("Servicios", href="/servicios", color="white", font_size="20px"),
                    rx.link("Proyectos", href="/proyectos", color="white", font_size="20px"),
                    rx.link("Contacto", href="/contacto", color="white", font_size="20px"),
                    padding="20px",
                    style={"gap": "15px"},
                ),
                bg="#000145",
                position="fixed",
                top="70px",
                left="0px",
                width="200px",
                border_radius="0px 0px 8px 0px",
                z_index="900",
            )
        )
    )

# ----- PÁGINA LOGIN ACTUALIZADA -----

def login() -> rx.Component:
    return rx.box(
        navbar(),
        rx.center(
            rx.vstack(
                rx.heading(
                    "Iniciar Sesión",
                    size="4",
                    font_weight="bold",
                    margin_bottom="2rem",
                    color="#333",
                ),
                rx.form(
                    rx.vstack(
                        rx.text(
                            "NOMBRE",
                            font_weight="bold",
                            font_size="sm",
                            align_self="start",
                            color="#333",
                        ),
                        rx.input(
                            placeholder="Ingresa tu nombre de usuario",
                            name="username",
                            width="300px",
                            border_radius="8px",
                            border="1px solid #e2e8f0",
                            padding="0.75rem",
                            bg="white",
                        ),
                        rx.text(
                            "CLAVE",
                            font_weight="bold",
                            font_size="sm",
                            align_self="start",
                            margin_top="1rem",
                            color="#333",
                        ),
                        rx.input(
                            type="password",
                            placeholder="Ingresa tu contraseña",
                            name="password",
                            width="300px",
                            border_radius="8px",
                            border="1px solid #e2e8f0",
                            padding="0.75rem",
                            bg="white",
                        ),
                        rx.hstack(
                            rx.button(
                                "Iniciar Sesión",
                                type="submit",
                                bg="#87B4FA",
                                color="black",
                                border_radius="8px",
                                padding_x="2rem",
                                padding_y="0.75rem",
                                _hover={"bg": "#6a9de0"},
                            ),
                            rx.link(
                                rx.button(
                                    "Registrarse",
                                    bg="white",
                                    color="#87B4FA",
                                    border="1px solid #87B4FA",
                                    border_radius="8px",
                                    padding_x="2rem",
                                    padding_y="0.75rem",
                                    _hover={"bg": "#f0f4f8"},
                                ),
                                href="/registro",
                            ),
                            spacing="4",  # Cambiado de "1rem" a "4"
                            margin_top="2rem",
                        ),
                        spacing="2",  # Cambiado de "0.5rem" a "2"
                    ),
                    on_submit=State.handle_login,
                ),
                align="center",
            ),
            margin_top="120px",
            min_height="100vh",
            bg="#CFE7FC",
        ),
    )

# ----- PÁGINA REGISTRO -----

def registro() -> rx.Component:
    return rx.box(
        navbar(),
        rx.center(
            rx.vstack(
                rx.heading(
                    "Registrarse",
                    size="4",
                    font_weight="bold",
                    margin_bottom="2rem",
                    color="#333",
                ),
                rx.vstack(
                    rx.text(
                        "NOMBRE COMPLETO",
                        font_weight="bold",
                        font_size="sm",
                        align_self="start",
                        color="#333",
                    ),
                    rx.input(
                        placeholder="Ingresa tu nombre completo",
                        width="300px",
                        border_radius="8px",
                        border="1px solid #e2e8f0",
                        padding="0.75rem",
                        bg="white",
                    ),
                    rx.text(
                        "CORREO ELECTRÓNICO",
                        font_weight="bold",
                        font_size="sm",
                        align_self="start",
                        margin_top="1rem",
                        color="#333",
                    ),
                    rx.input(
                        placeholder="Ingresa tu correo electrónico",
                        width="300px",
                        border_radius="8px",
                        border="1px solid #e2e8f0",
                        padding="0.75rem",
                        bg="white",
                    ),
                    rx.text(
                        "CLAVE",
                        font_weight="bold",
                        font_size="sm",
                        align_self="start",
                        margin_top="1rem",
                        color="#333",
                    ),
                    rx.input(
                        type="password",
                        placeholder="Crea tu contraseña",
                        width="300px",
                        border_radius="8px",
                        border="1px solid #e2e8f0",
                        padding="0.75rem",
                        bg="white",
                    ),
                    rx.button(
                        "Crear Cuenta",
                        bg="#87B4FA",
                        color="black",
                        border_radius="8px",
                        padding_x="2rem",
                        padding_y="0.75rem",
                        _hover={"bg": "#6a9de0"},
                        margin_top="2rem",
                    ),
                    spacing="2",  # Cambiado de "0.5rem" a "2"
                ),
                align="center",
            ),
            margin_top="120px",
            min_height="100vh",
            bg="#CFE7FC",
        ),
    )

# ----- PÁGINA PRINCIPAL -----
def index() -> rx.Component:
    return rx.box(
        navbar(),  # navbar arriba

        rx.box(
            rx.hstack(
                # TEXTO — mitad izquierda
                rx.box(
                    rx.text(
                        """
                        Grupo Carso es uno de los conglomerados empresariales más grandes y diversificados de México y Latinoamérica.
                        A lo largo de su historia, ha destacado por su visión estratégica, su capacidad de innovación y su compromiso
                        con el desarrollo económico y social del país. El grupo participa en sectores clave como la industria, comercio,
                        construcción, energía, infraestructura y servicios, integrando empresas líderes en cada uno de estos ámbitos.

                        Su enfoque se basa en la eficiencia, la calidad y el crecimiento sostenible, impulsando proyectos que generan 
                        valor y oportunidades. Grupo Carso ha logrado consolidarse gracias a su disciplina empresarial, la solidez de 
                        sus operaciones y su capacidad para adaptarse a los cambios del mercado. Hoy en día, continúa siendo un referente 
                        por su impacto, su responsabilidad y su contribución al progreso de México.
                        """,
                        font_size="20px",
                        color="#333",
                        text_align="justify",

                    ),
                    width="50%",
                    padding="20px",
                ),

                # IMAGEN — mitad derecha
                rx.box(
                    rx.image(
                        src="/imagen_empresa.jpg",  
                        width="100%",
                        height="100%",
                        object_fit="cover",
                        border_radius="12px",
                    ),
                    width="50%",
                    padding="20px",
                ),

                align="center",
                justify="center",
                spacing="5",
                width="100%",
            ),

            padding="120px 20px",  # espacio para que no tape el navbar
            bg="white",
        ),

        width="100%",
        height="100%",
        bg="#CFE7FC",
    )

# ----- OTRAS PÁGINAS -----

def servicios() -> rx.Component:
    return rx.box(navbar(), rx.text("Servicios", margin_top="120px"))

def proyectos() -> rx.Component:
    return rx.box(navbar(), rx.text("Proyectos", margin_top="120px"))

def contacto() -> rx.Component:
    return rx.box(navbar(), rx.text("Contacto", margin_top="120px"))



app = rx.App()
app.add_page(index, route="/")
app.add_page(login, route="/login")
app.add_page(registro, route="/registro")
app.add_page(servicios, route="/servicios")
app.add_page(proyectos, route="/proyectos")
app.add_page(contacto, route="/contacto")