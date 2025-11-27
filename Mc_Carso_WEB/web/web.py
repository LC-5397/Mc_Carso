import reflex as rx
from modelo.usuario_web import UsuarioWEB
from modelo.usuariodao_web import UsuarioDAO
from modelo.contacto import Contacto
from modelo.proyectodao import ProyectoDAO
from modelo.contactodao import ContactoDAO


class Contacto(rx.Base):
    nombre: str
    cargo: str
    correo: str


class State(rx.State):
    menu_open: bool = False
    current_user: str = ""

    @rx.var
    def is_logged(self) -> bool:
        return self.current_user != ""

    def toggle_menu(self):
        self.menu_open = not self.menu_open

    def set_user(self, username: str):
        self.current_user = username

    # Login
    def handle_login(self, form_data: dict):
        username = form_data.get("username", "")
        password = form_data.get("password", "")
        dao = UsuarioDAO()  # <-- crear instancia localmente
        if dao.verificar_usuario(username, password):
            self.current_user = username
            return rx.redirect("/")
        else:
            rx.toast.error("Usuario o contraseña incorrectos")

    # Registro
    def handle_register(self, form_data: dict):
        print("Datos recibidos del registro:", form_data)
        nuevo = UsuarioWEB(
            nombre=form_data.get("fullname", ""),
            correo=form_data.get("email", ""),
            clave=form_data.get("password", "")
        )
        dao = UsuarioDAO()  # <-- crear instancia localmente
        resultado = dao.registrar_usuario(nuevo)
        if resultado:
            return rx.window_alert("Usuario registrado correctamente")
        else:
            return rx.window_alert("No se pudo registrar el usuario")

class ContactoState(rx.State):
    lista_contactos: list[Contacto] = []

    def cargar_contactos(self):
        from modelo.contactodao import ContactoDAO

        dao = ContactoDAO()
        datos = dao.obtener_contactos()

        # datos YA es una lista de objetos Contacto
        self.lista_contactos = [
            Contacto(
                nombre=c.nombre,
                cargo=c.cargo,
                correo=c.correo
            )
            for c in datos
        ]


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
            rx.card(
                rx.vstack(
                    rx.heading(
                        "Iniciar Sesión",
                        size="6",
                        font_weight="bold",
                        color="#0A1A4A",
                        margin_bottom="1rem",
                    ),

                    rx.form(
                        rx.vstack(

                            # USUARIO
                            rx.text(
                                "NOMBRE",
                                font_weight="bold",
                                font_size="sm",
                                color="#0A1A4A",
                                align_self="start",
                            ),

                            rx.hstack(
                                rx.icon(tag="user", color="#0A1A4A", width="22px"),
                                rx.input(
                                    placeholder="Ingresa tu nombre de usuario",
                                    name="username",
                                    width="270px",
                                    border_radius="12px",
                                    border="1px solid rgba(255,255,255,0.4)",
                                    padding="0.9rem",
                                    bg="rgba(255,255,255,0.65)",
                                    color="black",
                                    _placeholder={"color": "black"},
                                    transition="all 0.25s ease",
                                    _focus={
                                        "border": "1px solid #3D6FE8",
                                        "bg": "white",
                                        "box_shadow": "0 0 10px rgba(93, 139, 255, 0.5)",
                                    },
                                ),
                                spacing="3",
                            ),

                            # PASSWORD
                            rx.text(
                                "CLAVE",
                                font_weight="bold",
                                font_size="sm",
                                color="#0A1A4A",
                                align_self="start",
                                margin_top="1rem",
                            ),

                            rx.hstack(
                                rx.icon(tag="lock", color="#0A1A4A", width="22px"),
                                rx.input(
                                    type="password",
                                    placeholder="Ingresa tu contraseña",
                                    name="password",
                                    width="270px",
                                    border_radius="12px",
                                    border="1px solid rgba(255,255,255,0.4)",
                                    padding="0.9rem",
                                    bg="rgba(255,255,255,0.65)",
                                    color="black",
                                    _placeholder={"color": "black"},
                                    transition="all 0.25s ease",
                                    _focus={
                                        "border": "1px solid #3D6FE8",
                                        "bg": "white",
                                        "box_shadow": "0 0 10px rgba(93, 139, 255, 0.5)",
                                    },
                                ),
                                spacing="3",
                            ),

                            # BOTONES
                            rx.hstack(
                                # BOTÓN LOGIN
                                rx.button(
                                    "Iniciar Sesión",
                                    type="submit",
                                    bg="#5A8DFF",
                                    color="white",
                                    border_radius="12px",
                                    padding_x="2.5rem",
                                    padding_y="0.9rem",
                                    font_weight="bold",
                                    transition="all 0.25s ease",
                                    _hover={
                                        "bg": "#3D6FE8",
                                        "transform": "scale(1.05)",
                                        "box_shadow": "0 8px 18px rgba(61,111,232,0.4)"
                                    },
                                ),

                                # BOTÓN REGISTRO
                                rx.link(
                                    rx.button(
                                        "Registrarse",
                                        bg="rgba(255,255,255,0.7)",
                                        color="#5A8DFF",
                                        border="2px solid #5A8DFF",
                                        border_radius="12px",
                                        padding_x="2.5rem",
                                        padding_y="0.9rem",
                                        font_weight="bold",
                                        transition="all 0.25s ease",
                                        _hover={
                                            "bg": "#eaf0ff",
                                            "transform": "scale(1.05)",
                                            "box_shadow": "0 8px 18px rgba(90,141,255,0.3)"
                                        },
                                    ),
                                    href="/registro",
                                ),

                                spacing="6",
                                margin_top="1.5rem",
                            ),

                            spacing="5",
                        ),

                        on_submit=State.handle_login,
                    ),
                ),

                # TARJETA GLASMORPHISM PREMIUM
                padding="3rem",
                border_radius="22px",
                width="440px",
                bg="rgba(255,255,255,0.28)",
                backdrop_filter="blur(18px)",
                box_shadow="0 12px 35px rgba(0,0,0,0.18)",
                border="1px solid rgba(255,255,255,0.4)",
            ),
        ),

        min_height="100vh",
        bg="#010C42",
        padding_top="120px",
    )


# ----- PÁGINA REGISTRO -----
def registro() -> rx.Component:
    return rx.box(
        navbar(),

        rx.center(
            rx.card(
                rx.vstack(
                    rx.heading(
                        "Crear Cuenta",
                        size="6",
                        font_weight="bold",
                        color="#0A1A4A",
                        margin_bottom="1rem",
                    ),

                    rx.form(
                        rx.vstack(

                            # ------------------- NOMBRE -------------------
                            rx.text(
                                "NOMBRE COMPLETO",
                                font_weight="bold",
                                font_size="sm",
                                color="#0A1A4A",
                                align_self="start",
                            ),

                            rx.hstack(
                                rx.icon(tag="user", color="#0A1A4A", width="22px"),
                                rx.input(
                                    type="text",
                                    placeholder="Ingresa tu nombre completo",
                                    name="fullname",
                                    width="270px",
                                    border_radius="12px",
                                    border="1px solid rgba(255,255,255,0.4)",
                                    padding="0.9rem",
                                    bg="rgba(255,255,255,0.65)",
                                    color="black",
                                    _placeholder={"color": "black"},
                                    transition="all 0.25s ease",
                                    _focus={
                                        "border": "1px solid #3D6FE8",
                                        "bg": "white",
                                        "box_shadow": "0 0 10px rgba(93, 139, 255, 0.5)",
                                    },
                                ),
                                spacing="3",
                            ),

                            # ------------------- CORREO -------------------
                            rx.text(
                                "CORREO ELECTRÓNICO",
                                font_weight="bold",
                                font_size="sm",
                                color="#0A1A4A",
                                align_self="start",
                                margin_top="1rem",
                            ),

                            rx.hstack(
                                rx.icon(tag="mail", color="#0A1A4A", width="22px"),
                                rx.input(
                                    type="text",   
                                    placeholder="Ingresa tu correo electrónico",
                                    name="email",
                                    width="270px",
                                    border_radius="12px",
                                    border="1px solid rgba(255,255,255,0.4)",
                                    padding="0.9rem",
                                    bg="rgba(255,255,255,0.65)",
                                    color="black",
                                    _placeholder={"color": "#6b7280"},
                                    transition="all 0.25s ease",
                                    _focus={
                                        "border": "1px solid #3D6FE8",
                                        "bg": "white",
                                        "box_shadow": "0 0 10px rgba(93, 139, 255, 0.5)",
                                    },
                                ),
                                spacing="3",
                            ),

                            # ------------------- CONTRASEÑA -------------------
                            rx.text(
                                "CLAVE",
                                font_weight="bold",
                                font_size="sm",
                                color="#0A1A4A",
                                align_self="start",
                                margin_top="1rem",
                            ),

                            rx.hstack(
                                rx.icon(tag="lock", color="#0A1A4A", width="22px"),
                                rx.input(
                                    type="password",
                                    placeholder="Crea tu contraseña",
                                    name="password",
                                    width="270px",
                                    border_radius="12px",
                                    border="1px solid rgba(255,255,255,0.4)",
                                    padding="0.9rem",
                                    bg="rgba(255,255,255,0.65)",
                                    color="black",
                                    _placeholder={"color": "black"},
                                    transition="all 0.25s ease",
                                    _focus={
                                        "border": "1px solid #3D6FE8",
                                        "bg": "white",
                                        "box_shadow": "0 0 10px rgba(93, 139, 255, 0.5)",
                                    },
                                ),
                                spacing="3",
                            ),

                            # ------------------- BOTÓN -------------------
                            rx.button(
                                "Crear Cuenta",
                                type="submit",
                                bg="#5A8DFF",
                                color="white",
                                border_radius="12px",
                                padding_x="2.5rem",
                                padding_y="0.9rem",
                                font_weight="bold",
                                margin_top="2rem",
                                transition="all 0.25s ease",
                                _hover={
                                    "bg": "#3D6FE8",
                                    "transform": "scale(1.05)",
                                    "box_shadow": "0 8px 18px rgba(61,111,232,0.4)",
                                },
                            ),

                            spacing="5",
                        ),

                        on_submit=State.handle_register,
                    ),
                ),

                padding="3rem",
                border_radius="22px",
                width="440px",
                bg="rgba(255,255,255,0.28)",
                backdrop_filter="blur(18px)",
                box_shadow="0 12px 35px rgba(0,0,0,0.18)",
                border="1px solid rgba(255,255,255,0.4)",
            ),
        ),

        min_height="100vh",
        bg="#010C42",
        padding_top="120px",
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

# ----- PÁGINA DE SERVICIOS -----
def servicios() -> rx.Component:
    return rx.box(
        navbar(),  # Navbar ya existente

        # ----- SECCIÓN PRINCIPAL (texto + imágenes) -----
        rx.box(
            rx.hstack(
                # ----- TEXTO (lado izquierdo) -----
                rx.box(
                    rx.text(
                        """
                        En Grupo Carso, nuestros servicios están diseñados para impulsar el crecimiento, 
                        la innovación y la eficiencia en sectores estratégicos para México y Latinoamérica. 
                        A través de nuestras distintas divisiones, ofrecemos soluciones integrales en energía, 
                        construcción, telecomunicaciones, infraestructura y servicios industriales, siempre con 
                        un enfoque en la calidad, la seguridad y el desarrollo sostenible.

                        Nuestro compromiso es brindar proyectos de alto impacto que generen valor social y 
                        económico, respaldados por equipos especializados, tecnología de vanguardia y décadas 
                        de experiencia operativa. Cada servicio que ofrecemos refleja nuestra visión de contribuir 
                        al progreso y al fortalecimiento de las comunidades donde operamos.
                        """,
                        font_size="20px",
                        color="#333",
                        text_align="justify",
                    ),
                    width="50%",
                    padding="20px",
                ),

                # ----- IMÁGENES (lado derecho) -----
                rx.box(
                    rx.vstack(
                        rx.image(
                            src="/servicios1.jpg",
                            width="100%",
                            height="200px",
                            object_fit="cover",
                            border_radius="12px",
                        ),
                        rx.image(
                            src="/servicios2.jpeg",
                            width="100%",
                            height="200px",
                            object_fit="cover",
                            border_radius="12px",
                        ),
                        rx.image(
                            src="/servicios3.webp",
                            width="100%",
                            height="200px",
                            object_fit="cover",
                            border_radius="12px",
                        ),
                        spacing="5",   # ← CORREGIDO
                        width="100%",
                    ),
                    width="50%",
                    padding="20px",
                ),

                align="center",
                justify="center",
                spacing="5",
                width="100%",
            ),

            padding="120px 20px",
            bg="white",
        ),

        # ----------- NUEVA SECCIÓN: SERVICIOS DE CONSTRUCCIÓN -----------
        rx.box(
            rx.vstack(
                rx.text(
                    "Servicios de la División de Construcción",
                    font_size="30px",
                    font_weight="bold",
                    color="#222",
                    margin_bottom="20px",
                ),

                rx.text(
                    "Nuestra división de construcción ofrece soluciones integrales con altos estándares técnicos y operativos:",
                    font_size="18px",
                    color="#444",
                    text_align="center",
                    width="85%",
                    margin_bottom="30px",
                ),

                # --- TARJETAS DE SERVICIOS ---
                rx.grid(
                    # Servicio 1
                    rx.box(
                        rx.vstack(
                            rx.text(
                                "• Construcción de Infraestructura",
                                font_size="20px",
                                font_weight="bold",
                                color="#222",
                                margin_bottom="10px",
                            ),
                            rx.text(
                                "Carreteras, puentes, túneles, presas y obras que impulsan la movilidad y el desarrollo regional.",
                                color="#555",
                                text_align="justify",
                            ),
                            spacing="3",
                        ),
                        padding="20px",
                        border_radius="12px",
                        border="1px solid #DDD",
                        bg="white",
                    ),

                    # Servicio 2
                    rx.box(
                        rx.vstack(
                            rx.text(
                                "• Construcción Industrial",
                                color="#222",
                                font_size="20px",
                                font_weight="bold",
                                margin_bottom="10px",
                            ),
                            rx.text(
                                "Plantas, parques industriales, naves y obras especializadas para sectores productivos.",
                                color="#555",
                                text_align="justify",
                            ),
                            spacing="3",
                        ),
                        padding="20px",
                        border_radius="12px",
                        border="1px solid #DDD",
                        bg="white",
                    ),

                    # Servicio 3
                    rx.box(
                        rx.vstack(
                            rx.text(
                                "• Urbanización y Obra Civil",
                                font_size="20px",
                                color="#222",
                                font_weight="bold",
                                margin_bottom="10px",
                            ),
                            rx.text(
                                "Desarrollo de fraccionamientos, cimentación, drenaje, pavimentación y servicios básicos.",
                                color="#555",
                                text_align="justify",
                            ),
                            spacing="3",
                        ),
                        padding="20px",
                        border_radius="12px",
                        border="1px solid #DDD",
                        bg="white",
                    ),

                    # Servicio 4
                    rx.box(
                        rx.vstack(
                            rx.text(
                                "• Supervisión y Gestión de Proyectos",
                                font_size="20px",
                                color="#222",
                                font_weight="bold",
                                margin_bottom="10px",
                            ),
                            rx.text(
                                "Administración, control de obra, evaluación técnica y aseguramiento de calidad.",
                                color="#555",
                                text_align="justify",
                            ),
                            spacing="3",
                        ),
                        padding="20px",
                        border_radius="12px",
                        border="1px solid #DDD",
                        bg="white",
                    ),

                    # Servicio 5
                    rx.box(
                        rx.vstack(
                            rx.text(
                                "• Instalaciones Eléctricas e Hidráulicas",
                                font_size="20px",
                                color="#222",
                                font_weight="bold",
                                margin_bottom="10px",
                            ),
                            rx.text(
                                "Montaje de redes, sistemas de agua potable, alcantarillado y cableado industrial.",
                                color="#555",
                                text_align="justify",
                            ),
                            spacing="3",
                        ),
                        padding="20px",
                        border_radius="12px",
                        border="1px solid #DDD",
                        bg="white",
                    ),

                    columns="2",
                    spacing="5",   # ← CORREGIDO
                    width="85%",
                    margin="0 auto",
                ),

                spacing="5",
                align="center",
                padding_bottom="40px",
            ),

            bg="#B7D1FF",
            padding="50px 20px",
        ),

        width="100%",
        height="100%",
        bg="#CFE7FC",
    )


# ----- PÁGINA DE PROYECTOS -----
def obtener_proyectos(limit=10):
    dao = ProyectoDAO()
    datos = dao.listarProyectos()
    return datos[:limit]

def proyectos() -> rx.Component:
    proyectos_bd = obtener_proyectos(10)  # Traemos 10 proyectos
    color_navbar = "#0D6EFD"  # Color azul de la navbar

    return rx.box(
        navbar(),  # Navbar ya existente

        rx.box(
            rx.vstack(
                # ----- TÍTULO ----- 
                rx.text(
                    "Proyectos Destacados",
                    font_size="32px",
                    font_weight="bold",
                    color="#222",
                    margin_bottom="20px",
                ),

                # ----- PÁRRAFO INTRODUCTORIO -----
                rx.text(
                    """
                    En Grupo Carso hemos desarrollado proyectos de gran escala que contribuyen al
                    crecimiento económico y social del país. Cada iniciativa combina innovación,
                    infraestructura sólida y un enfoque estratégico que garantiza resultados tangibles.
                    Estos proyectos reflejan nuestro compromiso con la calidad, la eficiencia y la
                    responsabilidad hacia las comunidades donde operamos.
                    """,
                    font_size="20px",
                    color="#333",
                    text_align="justify",
                    width="85%",
                ),

                spacing="4",
                align="center",
                padding_bottom="20px",
            ),

            # ----- GALERÍA DE PROYECTOS (3 COLUMNAS) -----
            rx.grid(
                rx.box(
                    rx.image(
                        src="/construccion_infraestructura.jpg",
                        width="100%",
                        height="220px",
                        object_fit="cover",
                        border_radius="12px",
                    ),
                    rx.text(
                        "Infraestructura y Construcción",
                        font_weight="bold",
                        margin_top="10px",
                        font_size="18px",
                        color="black",
                    ),
                    rx.text(
                        "Desarrollo de carreteras, puentes y obras que impulsan la conectividad nacional.",
                        text_align="justify",
                        color="black",
                    ),
                    padding="15px",
                ),
                rx.box(
                    rx.image(
                        src="/energia.png",
                        width="100%",
                        height="220px",
                        object_fit="cover",
                        border_radius="12px",
                    ),
                    rx.text(
                        "Energía y Telecomunicaciones",
                        font_weight="bold",
                        margin_top="10px",
                        font_size="18px",
                        color="black",
                    ),
                    rx.text(
                        "Implementación de soluciones que fortalecen la red energética y digital del país.",
                        text_align="justify",
                        color="black",
                    ),
                    padding="15px",
                ),
                rx.box(
                    rx.image(
                        src="/industrial.webp",
                        width="100%",
                        height="220px",
                        object_fit="cover",
                        border_radius="12px",
                    ),
                    rx.text(
                        "Desarrollo Industrial",
                        font_weight="bold",
                        margin_top="10px",
                        font_size="18px",
                        color="black",
                    ),
                    rx.text(
                        "Proyectos industriales eficientes que impulsan la competitividad y el crecimiento.",
                        text_align="justify",
                        color="black",
                    ),
                    padding="15px",
                ),

                columns="3",
                spacing="4",
                width="90%",
                margin="0 auto",
            ),

            # ----- TABLA SIMULADA DE PROYECTOS ----- 
            rx.vstack(
                rx.text(
                    "Otros Proyectos",
                    font_size="28px",
                    font_weight="bold",
                    color="#222",
                    margin_top="40px",
                    margin_bottom="20px",
                ),

                # Encabezado con barra azul
                rx.grid(
                    rx.text("Nombre del Proyecto", font_weight="bold", color="white"),
                    columns="1",
                    width="90%",
                    margin="0 auto",
                    bg=color_navbar,
                    padding="10px",
                    border_radius="6px 6px 0 0",
                ),

                # Filas de proyectos con texto negro
                *[
                    rx.grid(
                        rx.text(proyecto[2], color="black"),  # Nombre del proyecto en negro
                        columns="1",
                        width="90%",
                        margin="0 auto",
                        padding="8px",
                        border_bottom="1px solid #ccc",
                        bg="#f9f9f9",  # Fondo ligeramente gris para resaltar el texto
                    )
                    for proyecto in proyectos_bd
                ],
            ),

            padding="120px 20px",
            bg="white",
        ),

        width="100%",
        height="100%",
        bg="#CFE7FC",
    )

# --- PÁGINA DE CONTACTO ---
def contacto() -> rx.Component:
    return rx.vstack(
        pagina_contacto(),
        on_mount=ContactoState.cargar_contactos
    )


def pagina_contacto() -> rx.Component:
    return rx.box(
        navbar(),

        # ENCABEZADO
        rx.box(
            rx.vstack(
                rx.text(
                    "Contactos del Equipo Técnico",
                    font_size="32px",
                    font_weight="bold",
                    color="#222",
                    margin_bottom="10px",
                ),
                rx.text(
                    "Aquí encontrarás la lista del personal técnico disponible.",
                    font_size="18px",
                    color="#444",
                    text_align="center",
                    width="80%",
                ),
                spacing="7",
                align="center",
            ),
            padding="120px 20px 40px 20px",
            bg="white",
        ),

        # TARJETAS DE CONTACTOS
        rx.box(
            rx.vstack(
                rx.foreach(
                    ContactoState.lista_contactos,
                    lambda contacto: rx.box(
                        rx.vstack(
                            rx.text(contacto.nombre, font_size="20px", font_weight="bold"),
                            rx.text(contacto.cargo, font_size="16px", color="#555"),
                            rx.text(contacto.correo, font_size="15px", color="#2A6F97"),
                            spacing="3",
                            color="black",
                        ),
                        padding="20px",
                        border="1px solid #DDD",
                        border_radius="12px",
                        bg="#C4E4FF",
                        width="80%",
                        margin="0 auto",
                        colr="black",
                    )
                ),
                spacing="7",    
                width="100%",
                align="center",
            ),
            bg="#F5F5F5",
            padding="40px 0",
        ),

        width="100%",
        bg="#CFE7FC",
    )

# ----- APP -----
app = rx.App()
app.add_page(index, route="/")
app.add_page(login, route="/login")
app.add_page(registro, route="/registro")
app.add_page(servicios, route="/servicios")
app.add_page(proyectos, route="/proyectos")
app.add_page(contacto, route="/contacto")