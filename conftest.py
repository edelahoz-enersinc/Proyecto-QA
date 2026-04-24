import os
import pytest
from pathlib import Path

# ─────────────────────────────────────────────────────────────────────────────
# Configuraciones base - todas las credenciales se leen desde variables de entorno
# Nunca hardcodear valores sensibles en este archivo.
# Ver .env.example para la lista de variables requeridas.
# ─────────────────────────────────────────────────────────────────────────────
BASE_URL      = os.environ["ETRM_BASE_URL"]
ANTIBOT_TOKEN = os.environ["ETRM_ANTIBOT_TOKEN"]


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    """
    Inyecta el header antibot en todas las solicitudes del contexto del navegador.
    Esta es la precondición técnica crítica para evitar bloqueos de sesión.
    """
    return {
        **browser_context_args,
        "extra_http_headers": {
            "X-QA-Bypass-Token": ANTIBOT_TOKEN
        }
    }


@pytest.fixture
def test_email():
    """Email de prueba - leído desde variable de entorno ETRM_TEST_EMAIL"""
    return os.environ["ETRM_TEST_EMAIL"]


@pytest.fixture
def test_password():
    """Contraseña de prueba - leída desde variable de entorno ETRM_TEST_PASSWORD"""
    return os.environ["ETRM_TEST_PASSWORD"]


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Hook para capturar pantallas en caso de fallo y adjuntarlas al reporte HTML.
    """
    pytest_html = item.config.pluginmanager.getplugin("html")
    outcome = yield
    report = outcome.get_result()
    extra = getattr(report, "extra", [])

    if report.when == "call" or report.when == "setup":
        xfail = hasattr(report, "wasxfail")
        if (report.skipped and xfail) or (report.failed and not xfail):
            page = item.funcargs.get("page")
            if page:
                screenshot_dir = Path("reports/screenshots")
                screenshot_dir.mkdir(parents=True, exist_ok=True)

                file_name = f"{item.name}.png"
                file_path = screenshot_dir / file_name

                page.screenshot(path=str(file_path))

                if file_path.exists() and pytest_html is not None:
                    html = (
                        f'<div><img src="screenshots/{file_name}" alt="screenshot" '
                        f'style="width:600px;height:auto;" onclick="window.open(this.src)" '
                        f'align="right"/></div>'
                    )
                    extra.append(pytest_html.extras.html(html))
    report.extra = extra
