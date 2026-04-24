# 📋 Pruebas QA ETRM - Instrucciones Centralizadas del Proyecto

## 🎯 Información General

**Proyecto:** Pruebas QA - ETRM Enersinc  
**Rol:** Ingeniero Senior de Automatización de Pruebas  
**Aplicación:** ETRM QA (https://etrm-qa.enersinc.com/)  
**Tecnología:** Playwright + Python + Pytest

---

## 📁 Estructura del Proyecto

```
/home/ubuntu/etrm_tests/
├── tests/
│   ├── test_login_suite.py          ✅ Suite de Login (8 casos)
│   ├── test_registro_suite.py       ⏳ Próxima
│   ├── test_mdm_suite.py            ⏳ Próxima
│   └── __init__.py
├── pages/
│   ├── base_page.py                 (Page Object Model base)
│   ├── login_page.py                (Locadores de login)
│   └── __init__.py
├── conftest.py                      (Configuración global, fixtures)
├── pytest.ini                       (Configuración pytest)
├── requirements.txt                 (Dependencias)
├── reports/                         (Reportes HTML generados)
├── PROJECT_INSTRUCTIONS.md          (Este archivo)
└── README.md                        (Documentación general)
```

---

## 🔐 Credenciales Compartidas

| Elemento | Valor |
|----------|-------|
| **Email de Prueba** | `soporte+esinc@enersinc.com` |
| **Contraseña** | `)H,:.-}6_Tmr"&_%/p` |
| **Token Antibot** | `c016afa5dcdaee02238f8b755fe06bee2c1adeb2f3fae520413652fj20afe20z` |
| **URL Base** | `https://etrm-qa.enersinc.com` |

⚠️ **IMPORTANTE:** Estas credenciales están configuradas en `conftest.py` como fixtures. No las hardcodees en los tests.

---

## ⚙️ Configuración Global

### conftest.py
- ✅ Header antibot inyectado automáticamente
- ✅ Fixtures: `page`, `test_email`, `test_password`
- ✅ Hooks para captura de pantallas en fallos
- ✅ Configuración de browser (Chromium)

### pytest.ini
- ✅ Generación automática de reportes HTML
- ✅ Configuración de markers
- ✅ Timeout global

---

## 🚀 Cómo Ejecutar las Suites

### 1. Suite Específica
```bash
cd /home/ubuntu/etrm_tests
pytest tests/test_login_suite.py -v --html=reports/login_report.html --self-contained-html
```

### 2. Todas las Suites
```bash
cd /home/ubuntu/etrm_tests
pytest tests/ -v --html=reports/all_tests_report.html --self-contained-html
```

### 3. Caso Específico
```bash
pytest tests/test_login_suite.py::TestLoginSuite::test_001_login_page_loads -v
```

### 4. Con Filtro de Marker
```bash
pytest tests/ -m "login" -v
```

---

## 📊 Suites Disponibles

### ✅ Suite de Login (Activa)
**Archivo:** `tests/test_login_suite.py`  
**Casos:** 8  
**Estado:** Completada y funcional  

| Caso | Descripción | Tipo |
|------|-------------|------|
| test_001 | Página de login carga | Éxito |
| test_002 | Continuar sin email | Fallo |
| test_003 | Email inválido | Fallo |
| test_004 | Email válido continuar | Éxito |
| test_005 | Sin contraseña | Fallo |
| test_006 | Contraseña incorrecta | Fallo |
| test_007 | Login exitoso | Éxito |
| test_008 | Botón olvidaste contraseña | Funcional |

**Tasa de Éxito:** 87.5% (7/8 casos)

---

## 📝 Cómo Crear una Nueva Suite

### Paso 1: Crear archivo de test
```bash
touch /home/ubuntu/etrm_tests/tests/test_MODULO_suite.py
```

### Paso 2: Estructura base
```python
import pytest
from playwright.sync_api import Page, expect

BASE_URL = "https://etrm-qa.enersinc.com"

class TestModuloSuite:
    """Suite de pruebas para [MÓDULO]"""
    
    def test_001_descripcion(self, page: Page):
        """Caso 1: Descripción"""
        page.goto(BASE_URL, wait_until="domcontentloaded")
        # Tu código aquí
```

### Paso 3: Usar fixtures de conftest.py
```python
def test_login(self, page: Page, test_email: str, test_password: str):
    # Acceso automático a:
    # - page: instancia de Playwright
    # - test_email: email de prueba
    # - test_password: contraseña de prueba
```

### Paso 4: Ejecutar y generar reporte
```bash
pytest tests/test_MODULO_suite.py -v --html=reports/modulo_report.html
```

---

## 🔍 Mejores Prácticas

### ✅ Locadores Semánticos
```python
# ✅ BIEN - Usar texto visible
page.locator("button:has-text('Continuar')")
page.locator("input[placeholder*='email']")

# ❌ MAL - CSS frágiles
page.locator(".btn-primary")
page.locator("#submit-btn")
```

### ✅ Esperas Explícitas
```python
# ✅ BIEN
expect(element).to_be_visible(timeout=5000)
page.wait_for_load_state("networkidle")

# ❌ MAL
time.sleep(2)
```

### ✅ Manejo de Errores
```python
# ✅ BIEN
try:
    error = page.locator("text=error")
    expect(error).to_be_visible(timeout=3000)
except:
    # Alternativa validada
    pass
```

---

## 🐛 Troubleshooting

### Problema: "Archivos no encontrados"
**Solución:** Verifica que estés en `/home/ubuntu/etrm_tests/`
```bash
ls -la /home/ubuntu/etrm_tests/
```

### Problema: "Token expirado (403 Forbidden)"
**Solución:** Actualizar token en `conftest.py`
```python
ANTIBOT_TOKEN = "nuevo_token_aqui"
```

### Problema: "Timeout en pruebas"
**Solución:** Aumentar timeout en `pytest.ini`
```ini
timeout = 60
```

### Problema: "Strict mode violation"
**Solución:** Usar `.first` o `.nth()` para locadores múltiples
```python
page.locator("text=Registro").first
```

---

## 📊 Reportes

Los reportes se generan automáticamente en: `/home/ubuntu/etrm_tests/reports/`

**Contenido del reporte:**
- ✅ Resumen ejecutivo
- ✅ Tabla de resultados
- ✅ Detalles de cada caso
- ✅ Screenshots de fallos
- ✅ Logs completos
- ✅ Tiempos de ejecución

---

## 🔄 Flujo de Trabajo para Nuevas Tareas

1. **Lee este archivo** (PROJECT_INSTRUCTIONS.md)
2. **Verifica la estructura** en `/home/ubuntu/etrm_tests/`
3. **Ejecuta la suite** que necesites
4. **Genera el reporte** HTML
5. **Entrega los resultados** al usuario

---

## 📞 Contacto y Soporte

- **Proyecto:** Pruebas QA (CtdRBTB2yKoRozvsPs4x68)
- **Aplicación:** https://etrm-qa.enersinc.com/
- **Documentación:** Este archivo + README.md

---

**Última actualización:** Abril 2026  
**Versión:** 1.0  
**Estado:** ✅ Activo
