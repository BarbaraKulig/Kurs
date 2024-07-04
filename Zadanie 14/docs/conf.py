# docs/conf.py

import os
import sys
import sphinx_rtd_theme

# Dodanie ścieżki do modułu Pythona
sys.path.insert(0, os.path.abspath('../app'))

# Konfiguracja tematu Sphinx
html_theme = 'sphinx_rtd_theme'
html_theme_path = [sphinx_rtd_theme.get_html_theme_path()]

# Ustawienia projektu
project = 'Moja aplikacja REST API'
author = 'Twoje Imię i Nazwisko'

# Ustawienia Sphinx
extensions = [
    'sphinx.ext.autodoc',       # Automatyczna dokumentacja modułów
    'sphinx.ext.coverage',      # Raport pokrycia kodu
    'sphinx.ext.napoleon',      # Obsługa Google-style docstrings
    'sphinx.ext.viewcode',      # Linki do źródeł kodu
]

# Konfiguracja napoleon
napoleon_google_docstring = True
napoleon_numpy_docstring = False

# Plik źródłowy indeksu dokumentacji
master_doc = 'index'

# Dodatkowe ustawienia, np. temat, logo, strona startowa, itp.
