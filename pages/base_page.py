import os
from playwright.sync_api import Page


class BasePage:
    """
    Clase base para todas las páginas del aplicativo ETRM.
    Proporciona métodos comunes y configuración base.
    """
    
    BASE_URL = os.getenv("ETRM_BASE_URL", "https://etrm-qa.enersinc.com/login")
    
    def __init__(self, page: Page):
        self.page = page
    
    def navigate(self, path: str = ""):
        """Navega a una URL específica del aplicativo."""
        url = self.BASE_URL + path
        self.page.goto(url)
    
    def wait_for_element(self, locator, timeout: int = 10000):
        """Espera a que un elemento esté visible."""
        self.page.wait_for_selector(locator, timeout=timeout)
    
    def get_page_title(self) -> str:
        """Obtiene el título de la página."""
        return self.page.title()
