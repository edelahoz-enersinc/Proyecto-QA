# 🧪 Proyecto QA - ETRM Enersinc

Suite de pruebas automatizadas para el aplicativo **ETRM de Enersinc** usando **Playwright + Python + Pytest**.

## 📁 Estructura del Proyecto

```
Proyecto-QA/
├── tests/
│   └── test_login_suite.py     # Suite de Login (8 casos)
├── pages/
│   ├── __init__.py
│   ├── base_page.py            # Clase base Page Object Model
│   └── login_page.py           # Page Object Model para Login
├── conftest.py                 # Configuración global + header antibot
├── pytest.ini                  # Configuración de pytest
├── requirements.txt            # Dependencias
└── PROJECT_INSTRUCTIONS.md    # Instrucciones centralizadas
```

## ⚙️ Instalación

```bash
# Instalar dependencias
pip install -r requirements.txt

# Instalar navegadores de Playwright
playwright install chromium
```

## 🚀 Ejecutar Pruebas

```bash
# Suite de Login
pytest tests/test_login_suite.py -v --html=reports/login_report.html --self-contained-html

# Todas las suites
pytest tests/ -v --html=reports/all_tests_report.html --self-contained-html
```

## 📊 Suites Disponibles

| Suite | Archivo | Casos | Estado |
|-------|---------|-------|--------|
| **Login** | `test_login_suite.py` | 8 | ✅ Activa |
| Registro | `test_registro_suite.py` | - | ⏳ Próxima |
| MDM | `test_mdm_suite.py` | - | ⏳ Próxima |

## 🔐 Configuración

El header antibot se configura automáticamente en `conftest.py`. Las credenciales de prueba se leen desde variables de entorno:

```bash
export ETRM_TEST_EMAIL="usuario@enersinc.com"
export ETRM_TEST_PASSWORD="contraseña"
```

## 🛡️ Reglas de Código

- **Locadores semánticos**: `getByRole`, `getByText`, `has-text()`
- **Sin CSS frágiles**: No usar selectores `.clase` o `#id`
- **Teardown**: Limpiar datos de prueba al finalizar
- **Reportes**: HTML con capturas de pantalla en fallos

## 📖 Documentación

Ver **PROJECT_INSTRUCTIONS.md** para instrucciones detalladas.

---

**Tecnología:** Playwright + Python 3.11 + Pytest  
**Aplicación:** https://etrm-qa.enersinc.com  
**Estado:** ✅ Activo
