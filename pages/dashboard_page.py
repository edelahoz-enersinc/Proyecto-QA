from playwright.sync_api import Page, expect
from pages.base_page import BasePage


class DashboardPage(BasePage):
    """
    Page Object Model para el Dashboard del ETRM.

    Representa el estado del aplicativo tras un login exitoso.
    Proporciona métodos para verificar que el usuario está autenticado
    y para ejecutar el flujo de cierre de sesión.

    Flujo de cierre de sesión (según tarea ClickUp #86b2w88af):
    1. Hacer clic en el correo electrónico del usuario (parte superior derecha).
    2. En el menú desplegable, hacer clic en "Salir".
    3. Verificar que el sistema redirige al login y que el acceso protegido
       ya no está disponible.
    """

    def __init__(self, page: Page):
        super().__init__(page)

    # ── Locadores ────────────────────────────────────────────────────────────

    def get_user_menu_trigger(self):
        """
        Obtiene el elemento del correo electrónico en el header (disparador del menú).
        El aplicativo usa el id 'user_name' para este elemento.
        """
        return self.page.locator("#user_name")

    def get_logout_option(self):
        """
        Obtiene la opción 'Salir' del menú desplegable de usuario.
        Usa locador semántico por texto visible.
        """
        return self.page.get_by_text("Salir", exact=True)

    def get_email_field(self):
        """
        Obtiene el campo de email del paso 1 del login (confirma que se está en la página de login).
        """
        return self.page.get_by_placeholder("Ingresa tu email empresarial")

    # ── Acciones ─────────────────────────────────────────────────────────────

    def is_authenticated(self) -> bool:
        """
        Verifica si el usuario está autenticado comprobando que el menú de usuario
        (correo electrónico) es visible en el header.
        """
        try:
            self.get_user_menu_trigger().wait_for(state="visible", timeout=10000)
            return True
        except Exception:
            return False

    def logout(self):
        """
        Ejecuta el flujo de cierre de sesión:
        1. Hace clic en el correo electrónico (disparador del menú).
        2. Hace clic en 'Salir' en el menú desplegable.
        """
        self.get_user_menu_trigger().click()
        self.get_logout_option().wait_for(state="visible", timeout=5000)
        self.get_logout_option().click()

    def is_login_page_displayed(self, timeout: int = 10000) -> bool:
        """
        Verifica que la página de login se muestra tras el cierre de sesión.
        """
        try:
            self.get_email_field().wait_for(state="visible", timeout=timeout)
            return True
        except Exception:
            return False
