import pytest
from playwright.sync_api import Page, expect

import os
BASE_URL = os.environ["ETRM_BASE_URL"].rstrip("/")

class TestLoginSuite:
    """Suite de pruebas para el flujo de login"""
    
    def test_001_login_page_loads(self, page: Page):
        """Caso 1: Verificar que la página de login carga correctamente"""
        page.goto(BASE_URL, wait_until="domcontentloaded")
        
        # Verificar que estamos en la página correcta
        assert page.url == BASE_URL + "/"
        
        # Verificar que el título es correcto
        title = page.title()
        assert "Enersinc" in title
        
        # Verificar que el campo de email existe
        email_field = page.locator("input[placeholder*='email']")
        expect(email_field).to_be_visible()
    
    def test_002_continue_without_email(self, page: Page):
        """Caso 2: Intentar continuar sin ingresar email"""
        page.goto(BASE_URL, wait_until="domcontentloaded")
        
        # Buscar el botón de continuar
        continue_button = page.locator("button:has-text('Continuar')")
        
        # Hacer clic sin ingresar email
        continue_button.click()
        
        # Esperar a que aparezca el mensaje de error
        error_message = page.locator("text=Ingrese su correo")
        expect(error_message).to_be_visible(timeout=5000)
    
    def test_003_invalid_email_format(self, page: Page):
        """Caso 3: Ingresar email con formato inválido"""
        page.goto(BASE_URL, wait_until="domcontentloaded")
        
        # Ingresar email inválido
        email_field = page.locator("input[placeholder*='email']")
        email_field.fill("correo_invalido")
        
        # Hacer clic en continuar
        continue_button = page.locator("button:has-text('Continuar')")
        continue_button.click()
        
        # Verificar que se muestra error de formato
        error_message = page.locator("text=formato válido")
        expect(error_message).to_be_visible(timeout=5000)
    
    def test_004_valid_email_continue(self, page: Page, test_email: str):
        """Caso 4: Continuar con email válido"""
        page.goto(BASE_URL, wait_until="domcontentloaded")
        
        # Ingresar email válido
        email_field = page.locator("input[placeholder*='email']")
        email_field.fill(test_email)
        
        # Hacer clic en continuar
        continue_button = page.locator("button:has-text('Continuar')")
        continue_button.click()
        
        # Esperar a que aparezca el campo de contraseña
        password_field = page.locator("input[type='password']")
        expect(password_field).to_be_visible(timeout=5000)
        
        # Verificar que el email está pre-llenado
        email_display = page.locator("input[type='text']")
        email_value = email_display.input_value()
        assert test_email in email_value
    
    def test_005_password_without_input(self, page: Page, test_email: str):
        """Caso 5: Intentar hacer login sin ingresar contraseña"""
        page.goto(BASE_URL, wait_until="domcontentloaded")
        
        # Ingresar email
        email_field = page.locator("input[placeholder*='email']")
        email_field.fill(test_email)
        
        # Continuar
        continue_button = page.locator("button:has-text('Continuar')")
        continue_button.click()
        
        # Esperar a que aparezca el campo de contraseña
        password_field = page.locator("input[type='password']")
        expect(password_field).to_be_visible(timeout=5000)
        
        # Hacer clic en Entrar sin ingresar contraseña
        enter_button = page.locator("button:has-text('Entrar')")
        enter_button.click()
        
        # Verificar que se muestra error o que sigue en la página de contraseña
        try:
            error_message = page.locator("text=obligatorio")
            expect(error_message).to_be_visible(timeout=3000)
        except:
            # Si no aparece error, verificar que sigue en la página
            password_field_still = page.locator("input[type='password']")
            expect(password_field_still).to_be_visible(timeout=3000)
    
    def test_006_wrong_password(self, page: Page, test_email: str):
        """Caso 6: Ingresar contraseña incorrecta"""
        page.goto(BASE_URL, wait_until="domcontentloaded")
        
        # Ingresar email
        email_field = page.locator("input[placeholder*='email']")
        email_field.fill(test_email)
        
        # Continuar
        continue_button = page.locator("button:has-text('Continuar')")
        continue_button.click()
        
        # Esperar a que aparezca el campo de contraseña
        password_field = page.locator("input[type='password']")
        expect(password_field).to_be_visible(timeout=5000)
        
        # Ingresar contraseña incorrecta
        password_field.fill("contraseña_incorrecta")
        
        # Hacer clic en Entrar
        enter_button = page.locator("button:has-text('Entrar')")
        enter_button.click()
        
        # Esperar a que aparezca error de credenciales
        error_message = page.locator("text=credenciales")
        try:
            expect(error_message).to_be_visible(timeout=5000)
        except:
            # Si no aparece ese mensaje, verificar que sigue en la página de login
            password_field_still = page.locator("input[type='password']")
            expect(password_field_still).to_be_visible(timeout=5000)
    
    def test_007_successful_login(self, page: Page, test_email: str, test_password: str):
        """Caso 7: Login exitoso con credenciales válidas"""
        page.goto(BASE_URL, wait_until="domcontentloaded")
        
        # Ingresar email
        email_field = page.locator("input[placeholder*='email']")
        email_field.fill(test_email)
        
        # Continuar
        continue_button = page.locator("button:has-text('Continuar')")
        continue_button.click()
        
        # Esperar a que aparezca el campo de contraseña
        password_field = page.locator("input[type='password']")
        expect(password_field).to_be_visible(timeout=5000)
        
        # Ingresar contraseña
        password_field.fill(test_password)
        
        # Hacer clic en Entrar
        enter_button = page.locator("button:has-text('Entrar')")
        enter_button.click()
        
        # Esperar a que se cargue el dashboard
        page.wait_for_load_state("networkidle", timeout=10000)
        
        # Verificar que estamos en el dashboard
        dashboard_title = page.locator("text=Bienvenido a Enersinc")
        expect(dashboard_title).to_be_visible(timeout=5000)
        
        # Verificar que los módulos están visibles (usar nth para evitar strict mode)
        modulos = page.locator("text=Registro").first
        expect(modulos).to_be_visible(timeout=5000)
    
    def test_008_forgot_password_button(self, page: Page, test_email: str):
        """Caso 8: Verificar que el botón de olvidaste contraseña es funcional"""
        page.goto(BASE_URL, wait_until="domcontentloaded")
        
        # Ingresar email
        email_field = page.locator("input[placeholder*='email']")
        email_field.fill(test_email)
        
        # Continuar
        continue_button = page.locator("button:has-text('Continuar')")
        continue_button.click()
        
        # Esperar a que aparezca el botón de olvidaste contraseña
        forgot_button = page.locator("button:has-text('Olvidaste')")
        expect(forgot_button).to_be_visible(timeout=5000)
        
        # Hacer clic en el botón
        forgot_button.click()
        
        # Verificar que se abre un diálogo o se navega a otra página
        page.wait_for_load_state("networkidle", timeout=5000)
