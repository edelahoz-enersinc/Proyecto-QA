import os
import pytest
from playwright.sync_api import Page, expect

BASE_URL = os.environ["ETRM_BASE_URL"].rstrip("/")

# ─────────────────────────────────────────────────────────────────────────────
# Helpers de navegación reutilizables
# ─────────────────────────────────────────────────────────────────────────────

def ir_a_login(page: Page):
    """Navega a la página de login y espera que el formulario esté listo."""
    page.goto(BASE_URL, wait_until="domcontentloaded")
    # El campo de email del paso 1 tiene un placeholder específico
    expect(page.get_by_placeholder("Ingresa tu email empresarial")).to_be_visible(timeout=8000)


def avanzar_a_paso_contrasena(page: Page, email: str):
    """
    Completa el paso 1 (email) y espera que aparezca el paso 2 (contraseña).
    En el paso 2 el formulario muestra el email como campo readonly Y el campo
    de contraseña; por eso usamos 'input[type=password]' como ancla del paso 2.
    """
    page.get_by_placeholder("Ingresa tu email empresarial").fill(email)
    page.get_by_role("button", name="Continuar").click()
    expect(page.locator("input[type='password']")).to_be_visible(timeout=8000)


# ─────────────────────────────────────────────────────────────────────────────
# Suite de pruebas de Login
# ─────────────────────────────────────────────────────────────────────────────

class TestLoginSuite:
    """Suite de pruebas para el flujo de inicio de sesión del ETRM."""

    # ── CASOS ORIENTADOS AL FALLO ─────────────────────────────────────────────

    def test_001_login_page_loads(self, page: Page):
        """
        Caso 001 – Verificar que la página de login carga correctamente.
        Criterio: El campo de email y el botón 'Continuar' son visibles.
        """
        ir_a_login(page)
        expect(page.get_by_role("button", name="Continuar")).to_be_visible()

    def test_002_continue_without_email(self, page: Page):
        """
        Caso 002 – Intentar continuar sin ingresar correo.
        Criterio: Se muestra un mensaje de error indicando que el campo es requerido.
        """
        ir_a_login(page)
        page.get_by_role("button", name="Continuar").click()
        expect(page.locator("text=Ingrese su correo")).to_be_visible(timeout=5000)

    def test_003_invalid_email_format(self, page: Page):
        """
        Caso 003 – Ingresar un correo con formato inválido.
        Criterio: Se muestra un mensaje de error de formato.
        """
        ir_a_login(page)
        page.get_by_placeholder("Ingresa tu email empresarial").fill("correo_invalido")
        page.get_by_role("button", name="Continuar").click()
        expect(page.locator("text=formato válido")).to_be_visible(timeout=5000)

    def test_004_valid_email_continue(self, page: Page, test_email: str):
        """
        Caso 004 – Continuar con correo válido.
        Criterio: El formulario avanza al paso 2 y muestra el campo de contraseña.
        """
        ir_a_login(page)
        avanzar_a_paso_contrasena(page, test_email)
        # En el paso 2 el email aparece como campo readonly; lo buscamos por valor
        email_readonly = page.locator(f"input[value='{test_email}']")
        expect(email_readonly).to_be_visible(timeout=5000)

    def test_005_password_without_input(self, page: Page, test_email: str):
        """
        Caso 005 – Intentar hacer login sin ingresar contraseña.
        Criterio: El botón 'Entrar' permanece deshabilitado mientras el campo de
        contraseña esté vacío, impidiendo el envío del formulario.
        """
        ir_a_login(page)
        avanzar_a_paso_contrasena(page, test_email)
        # La aplicación deshabilita el botón 'Entrar' cuando no hay contraseña ingresada.
        # Verificamos que el botón esté deshabilitado (not enabled) como protección de UI.
        entrar_button = page.get_by_role("button", name="Entrar")
        expect(entrar_button).to_be_visible(timeout=5000)
        expect(entrar_button).to_be_disabled()

    def test_006_wrong_password(self, page: Page, test_email: str):
        """
        Caso 006 – Ingresar correo válido y contraseña incorrecta.
        Criterio: Se muestra mensaje de error de credenciales o el usuario permanece en el paso 2.
        """
        ir_a_login(page)
        avanzar_a_paso_contrasena(page, test_email)
        page.locator("input[type='password']").fill("contraseña_incorrecta_123")
        page.get_by_role("button", name="Entrar").click()

        try:
            expect(page.locator("text=credenciales")).to_be_visible(timeout=6000)
        except Exception:
            expect(page.locator("input[type='password']")).to_be_visible(timeout=3000)

    # ── CASOS ORIENTADOS AL ÉXITO ─────────────────────────────────────────────

    def test_007_successful_login(self, page: Page, test_email: str, test_password: str):
        """
        Caso 007 – Login exitoso con credenciales válidas.
        Criterio: El usuario es redirigido al dashboard y se muestran los módulos.
        """
        ir_a_login(page)
        avanzar_a_paso_contrasena(page, test_email)
        page.locator("input[type='password']").fill(test_password)
        page.get_by_role("button", name="Entrar").click()

        page.wait_for_load_state("networkidle", timeout=15000)
        expect(page.get_by_text("Bienvenido a Enersinc")).to_be_visible(timeout=8000)

    def test_008_forgot_password_button(self, page: Page, test_email: str):
        """
        Caso 008 – Verificar que el botón '¿Olvidaste tu contraseña?' es funcional.
        Criterio: Al hacer clic, la aplicación muestra el formulario de recuperación
        de contraseña con el campo 'Email del usuario' y el botón 'Enviar'.
        """
        ir_a_login(page)
        avanzar_a_paso_contrasena(page, test_email)
        forgot_button = page.get_by_role("button", name="Olvidaste")
        expect(forgot_button).to_be_visible(timeout=5000)
        forgot_button.click()
        # La app muestra un formulario de recuperación (SPA, sin recarga completa)
        expect(page.get_by_placeholder("Email del usuario")).to_be_visible(timeout=8000)
        expect(page.get_by_role("button", name="Enviar")).to_be_visible(timeout=5000)
