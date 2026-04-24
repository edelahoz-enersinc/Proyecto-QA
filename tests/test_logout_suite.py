"""
Suite de pruebas: Cerrar Sesión (Logout)
Módulo: General / Transversales
Referencia ClickUp: https://app.clickup.com/t/86b2w88af

Objetivo (según tarea ClickUp):
    Asegurar que al cerrar sesión, el sistema termine la sesión del usuario
    correctamente, redirigiéndolo a la página de inicio o login y que el
    usuario ya no tenga acceso a las funcionalidades protegidas.

Precondición (según tarea ClickUp):
    Estar activo en el sistema (usuario autenticado).

Pasos definidos en ClickUp:
    1. Ubicarse en la parte superior derecha del aplicativo donde está el
       correo electrónico y dar clic.
    2. Seleccionar 'Salir' y darle clic.

Casos adicionales generados por el constructor QA:
    - Verificar que el menú de usuario es visible y accesible.
    - Verificar que la sesión no persiste tras el logout (acceso protegido denegado).
    - Verificar que el usuario puede volver a iniciar sesión tras el logout.
"""
import os
import pytest
from playwright.sync_api import Page, expect

BASE_URL = os.environ["ETRM_BASE_URL"].rstrip("/")


# ─────────────────────────────────────────────────────────────────────────────
# Helpers de navegación reutilizables
# ─────────────────────────────────────────────────────────────────────────────

def realizar_login(page: Page, email: str, password: str):
    """
    Ejecuta el flujo completo de login de dos pasos.
    Paso 1: email + botón 'Continuar'.
    Paso 2: contraseña + botón 'Entrar'.
    """
    page.goto(BASE_URL, wait_until="domcontentloaded", timeout=60000)
    page.get_by_placeholder("Ingresa tu email empresarial").fill(email)
    page.get_by_role("button", name="Continuar").click()
    page.locator("input[type='password']").wait_for(state="visible", timeout=15000)
    page.locator("input[type='password']").fill(password)
    page.get_by_role("button", name="Entrar").click()
    page.wait_for_load_state("networkidle", timeout=30000)


def abrir_menu_usuario(page: Page):
    """
    Hace clic en el correo electrónico del usuario en el header para abrir
    el menú desplegable (parte superior derecha del aplicativo).
    """
    page.locator("#user_name").click()
    page.get_by_text("Salir", exact=True).wait_for(state="visible", timeout=5000)


# ─────────────────────────────────────────────────────────────────────────────
# Suite de pruebas de Cierre de Sesión
# ─────────────────────────────────────────────────────────────────────────────

class TestLogoutSuite:
    """
    Suite de pruebas para el flujo de cierre de sesión del ETRM.
    Basada en la tarea ClickUp #86b2w88af (Cerrar Sesión).
    """

    def test_001_user_menu_visible_after_login(
        self, page: Page, test_email: str, test_password: str
    ):
        """
        Caso 001 – Verificar que el menú de usuario es visible tras el login.
        Criterio: El elemento con el correo electrónico del usuario es visible
        en la parte superior derecha del header tras autenticarse.
        """
        realizar_login(page, test_email, test_password)
        user_menu = page.locator("#user_name")
        expect(user_menu).to_be_visible(timeout=10000)
        # Verificar que muestra el correo del usuario autenticado
        expect(user_menu).to_contain_text(test_email.split("@")[0])

    def test_002_logout_option_visible_in_menu(
        self, page: Page, test_email: str, test_password: str
    ):
        """
        Caso 002 – Verificar que la opción 'Salir' aparece en el menú de usuario.
        Criterio: Al hacer clic en el correo electrónico (parte superior derecha),
        el menú desplegable muestra la opción 'Salir'.
        Pasos ClickUp: Paso 1 — Ubicarse en la parte superior derecha y dar clic.
        """
        realizar_login(page, test_email, test_password)
        abrir_menu_usuario(page)
        salir_option = page.get_by_text("Salir", exact=True)
        expect(salir_option).to_be_visible(timeout=5000)

    def test_003_logout_redirects_to_login(
        self, page: Page, test_email: str, test_password: str
    ):
        """
        Caso 003 – Verificar que al cerrar sesión se redirige a la página de login.
        Criterio: Tras hacer clic en 'Salir', el sistema muestra el formulario de
        login con el campo de correo electrónico visible.
        Pasos ClickUp: Paso 1 + Paso 2 (flujo completo de cierre de sesión).
        """
        realizar_login(page, test_email, test_password)
        abrir_menu_usuario(page)
        page.get_by_text("Salir", exact=True).click()
        # Verificar que la página de login es visible
        expect(
            page.get_by_placeholder("Ingresa tu email empresarial")
        ).to_be_visible(timeout=15000)

    def test_004_protected_route_inaccessible_after_logout(
        self, page: Page, test_email: str, test_password: str
    ):
        """
        Caso 004 – Verificar que las rutas protegidas no son accesibles tras el logout.
        Criterio: Tras cerrar sesión, si el usuario intenta acceder directamente a
        una URL protegida del aplicativo, el sistema lo redirige al login.
        Este caso valida el requisito de ClickUp: 'el usuario ya no tenga acceso
        a las funcionalidades protegidas'.
        """
        realizar_login(page, test_email, test_password)
        # Guardar la URL del dashboard autenticado
        dashboard_url = page.url

        # Ejecutar el cierre de sesión
        abrir_menu_usuario(page)
        page.get_by_text("Salir", exact=True).click()
        expect(
            page.get_by_placeholder("Ingresa tu email empresarial")
        ).to_be_visible(timeout=15000)

        # Intentar navegar directamente a la URL del dashboard
        page.goto(dashboard_url, wait_until="domcontentloaded", timeout=30000)

        # El sistema debe redirigir al login (no mostrar contenido protegido)
        expect(
            page.get_by_placeholder("Ingresa tu email empresarial")
        ).to_be_visible(timeout=10000)

    def test_005_user_can_login_again_after_logout(
        self, page: Page, test_email: str, test_password: str
    ):
        """
        Caso 005 – Verificar que el usuario puede volver a iniciar sesión tras el logout.
        Criterio: Tras cerrar sesión, el usuario puede autenticarse nuevamente
        con las mismas credenciales y acceder al sistema.
        """
        # Primer login
        realizar_login(page, test_email, test_password)
        expect(page.locator("#user_name")).to_be_visible(timeout=10000)

        # Cerrar sesión
        abrir_menu_usuario(page)
        page.get_by_text("Salir", exact=True).click()
        expect(
            page.get_by_placeholder("Ingresa tu email empresarial")
        ).to_be_visible(timeout=15000)

        # Segundo login con las mismas credenciales
        page.get_by_placeholder("Ingresa tu email empresarial").fill(test_email)
        page.get_by_role("button", name="Continuar").click()
        page.locator("input[type='password']").wait_for(state="visible", timeout=15000)
        page.locator("input[type='password']").fill(test_password)
        page.get_by_role("button", name="Entrar").click()
        page.wait_for_load_state("networkidle", timeout=30000)

        # Verificar que el usuario está autenticado nuevamente
        expect(page.locator("#user_name")).to_be_visible(timeout=10000)
