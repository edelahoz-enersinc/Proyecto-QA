from playwright.sync_api import Page, expect
from pages.base_page import BasePage


class LoginPage(BasePage):
    """
    Page Object Model para la página de Login del ETRM.
    Utiliza locadores semánticos (texto visible, placeholders, roles).
    
    Nota: El formulario de login es de dos pasos:
    1. Primer paso: Ingresa el email y hace clic en "Continuar"
    2. Segundo paso: Ingresa la contraseña (si es necesario)
    """
    
    def __init__(self, page: Page):
        super().__init__(page)
    
    def navigate_to_login(self):
        """Navega a la página de login."""
        self.navigate()
    
    def get_email_input(self):
        """
        Obtiene el campo de entrada de correo electrónico.
        Prioriza locadores semánticos por id, placeholder o label.
        """
        return self.page.locator("#email").or_(
            self.page.get_by_placeholder("Ingresa tu email empresarial")
        ).or_(
            self.page.get_by_placeholder("email", exact=False)
        ).or_(
            self.page.get_by_label("Correo electrónico", exact=False)
        )
    
    def get_password_input(self):
        """
        Obtiene el campo de entrada de contraseña.
        Prioriza locadores semánticos por id, placeholder o label.
        """
        return self.page.locator("#password").or_(
            self.page.get_by_placeholder("Contraseña", exact=False)
        ).or_(
            self.page.get_by_placeholder("Password", exact=False)
        ).or_(
            self.page.get_by_label("Contraseña", exact=False)
        )
    
    def get_continue_button(self):
        """
        Obtiene el botón de continuar (primer paso del formulario).
        Busca por rol y nombre visible.
        """
        return self.page.get_by_role("button", name="Continuar").or_(
            self.page.get_by_role("button", name="Continue")
        ).or_(
            self.page.locator("button[type='submit']")
        )
    
    def get_login_button(self):
        """
        Obtiene el botón de inicio de sesión (si existe en el segundo paso).
        Busca por rol y nombre visible.
        """
        return self.page.get_by_role("button", name="Iniciar sesión").or_(
            self.page.get_by_role("button", name="Login")
        ).or_(
            self.page.get_by_role("button", name="Sign in")
        )
    
    def fill_email(self, email: str):
        """Rellena el campo de correo electrónico."""
        email_input = self.get_email_input()
        email_input.fill(email)
    
    def fill_password(self, password: str):
        """Rellena el campo de contraseña."""
        password_input = self.get_password_input()
        password_input.fill(password)
    
    def click_continue_button(self):
        """Hace clic en el botón de continuar."""
        continue_button = self.get_continue_button()
        continue_button.click()
    
    def click_login_button(self):
        """Hace clic en el botón de inicio de sesión."""
        login_button = self.get_login_button()
        login_button.click()
    
    def login(self, email: str, password: str = None):
        """
        Ejecuta el flujo completo de login.
        
        Pasos:
        1. Navega a la página de login
        2. Ingresa el email
        3. Hace clic en "Continuar"
        4. Si se proporciona contraseña, ingresa la contraseña y hace clic en "Iniciar sesión"
        """
        self.navigate_to_login()
        self.fill_email(email)
        self.click_continue_button()
        
        # Esperar a que se cargue el siguiente paso (si existe)
        if password:
            self.page.wait_for_timeout(1000)  # Esperar a que se cargue el formulario
            self.fill_password(password)
            self.click_login_button()
    
    def is_login_page_displayed(self) -> bool:
        """
        Verifica si la página de login está visible.
        """
        try:
            # Verificar que el campo de email está visible
            email_input = self.get_email_input()
            return email_input.is_visible(timeout=5000)
        except:
            return False
    
    def get_error_message(self) -> str:
        """
        Obtiene el mensaje de error si existe.
        """
        error_locator = self.page.locator("[role='alert']").or_(
            self.page.locator(".error-message")
        ).or_(
            self.page.locator(".alert-danger")
        )
        try:
            return error_locator.text_content(timeout=5000)
        except:
            return ""
    
    def is_dashboard_loaded(self, timeout: int = 10000) -> bool:
        """
        Verifica si el dashboard se ha cargado correctamente después del login.
        """
        try:
            dashboard_heading = self.page.get_by_role("heading", name="Dashboard").or_(
                self.page.get_by_role("heading", name="Inicio")
            ).or_(
                self.page.locator("[data-testid='dashboard-title']")
            )
            dashboard_heading.wait_for(state="visible", timeout=timeout)
            return True
        except:
            return False
    
    def is_password_step_displayed(self, timeout: int = 5000) -> bool:
        """
        Verifica si el paso de contraseña está visible después de ingresar el email.
        """
        try:
            password_input = self.get_password_input()
            return password_input.is_visible(timeout=timeout)
        except:
            return False
    
    def wait_for_password_step(self, timeout: int = 10000) -> bool:
        """
        Espera a que el paso de contraseña sea visible.
        Retorna True si aparece, False si no.
        """
        try:
            password_input = self.get_password_input()
            password_input.wait_for(state="visible", timeout=timeout)
            return True
        except:
            return False
    
    def is_login_button_visible(self, timeout: int = 5000) -> bool:
        """
        Verifica si el botón de login está visible.
        """
        try:
            login_button = self.get_login_button()
            return login_button.is_visible(timeout=timeout)
        except:
            return False
    
    def get_current_url(self) -> str:
        """
        Obtiene la URL actual de la página.
        """
        return self.page.url
