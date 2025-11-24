import reflex as rx

class MenuState(rx.State):
    menu_open: bool = False

    def toggle_menu(self):
        self.menu_open = not self.menu_open
